#!/usr/bin/env python3
"""Collect podcast episode metadata from configured public RSS feeds."""

from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import math
import os
import re
import socket
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from functools import lru_cache
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

import feedparser
import yaml

import pending

DEFAULT_TIMEOUT_SECONDS = 20.0
DEFAULT_RETRIES = 2
DEFAULT_LOOKBACK_DAYS = 30
MAX_UNKNOWN_DATES_PER_SOURCE = 3
DESCRIPTION_LIMIT = 1000
ITEM_ID_HASH_LENGTH = 12
USER_AGENT = "EchoForge/0.1 podcast metadata collector"

PUBLIC_SCHEMES = {"http", "https"}
ALLOWED_STATUSES = {"pending", "processed", "ignored", "failed"}
TRANSCRIPT_REL = "https://podcastindex.org/namespace/1.0#transcript"
class CollectorError(Exception):
    """Raised for configuration, transport, or feed validation failures."""


class _PublicRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, new_url):  # type: ignore[no-untyped-def]
        candidate = public_url(new_url)
        if not candidate:
            raise CollectorError("feed redirected to a non-public URL")
        resolve_public_host(candidate)
        return super().redirect_request(request, fp, code, msg, headers, candidate)


class _TextExtractor(HTMLParser):
    BLOCK_TAGS = {
        "address",
        "article",
        "aside",
        "blockquote",
        "br",
        "div",
        "footer",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "header",
        "hr",
        "li",
        "main",
        "nav",
        "ol",
        "p",
        "pre",
        "section",
        "table",
        "tr",
        "ul",
    }
    IGNORED_TAGS = {"script", "style"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.ignored_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.IGNORED_TAGS:
            self.ignored_depth += 1
        elif tag in self.BLOCK_TAGS and not self.ignored_depth:
            self.parts.append(" ")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.IGNORED_TAGS and self.ignored_depth:
            self.ignored_depth -= 1
        elif tag in self.BLOCK_TAGS and not self.ignored_depth:
            self.parts.append(" ")

    def handle_data(self, data: str) -> None:
        if not self.ignored_depth:
            self.parts.append(data)


@dataclass(frozen=True)
class Source:
    source_id: str
    name: str
    url: str
    enabled: bool
    include_keywords: tuple[str, ...]
    exclude_keywords: tuple[str, ...]
    min_duration_minutes: float | None


@dataclass
class SourceSummary:
    source_id: str
    source_name: str
    status: str
    entries: int = 0
    new: int = 0
    existing: int = 0
    filtered: int = 0
    skipped: int = 0
    error: str | None = None


def clean_text(value: Any, limit: int | None = None) -> str:
    """Convert RSS HTML/text into compact plain text."""
    if value is None:
        return ""
    parser = _TextExtractor()
    try:
        parser.feed(str(value))
        parser.close()
        text = "".join(parser.parts)
    except Exception:
        text = re.sub(r"<[^>]*>", " ", str(value))
    text = " ".join(text.split())
    if limit is not None:
        text = text[:limit]
    return text


def public_url(value: Any) -> str | None:
    """Return a normalized public HTTP(S) URL or None."""
    if not isinstance(value, str):
        return None
    candidate = value.strip()
    try:
        parsed = urlparse(candidate)
        port = parsed.port
    except ValueError:
        return None
    if parsed.scheme.lower() not in PUBLIC_SCHEMES or not parsed.netloc or not parsed.hostname:
        return None
    if parsed.username is not None or parsed.password is not None:
        return None
    if port is not None and not 1 <= port <= 65535:
        return None
    hostname = parsed.hostname.rstrip(".").casefold()
    if hostname == "localhost" or hostname.endswith(".localhost") or hostname.endswith(".local"):
        return None
    try:
        address = ipaddress.ip_address(hostname)
    except ValueError:
        return candidate
    if not address.is_global:
        return None
    return candidate


def parse_duration(value: Any) -> int | None:
    """Parse podcast duration seconds or colon-delimited time."""
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        if not math.isfinite(value) or value < 0:
            return None
        return int(value)

    text = str(value).strip()
    if not text:
        return None
    if re.fullmatch(r"\d+(?:\.\d+)?", text):
        numeric = float(text)
        return int(numeric) if math.isfinite(numeric) else None

    parts = text.split(":")
    if len(parts) not in {2, 3} or not all(re.fullmatch(r"\d+(?:\.\d+)?", part) for part in parts):
        return None
    numbers = [float(part) for part in parts]
    if not all(math.isfinite(number) for number in numbers):
        return None
    if len(numbers) == 2:
        minutes, seconds = numbers
        if seconds >= 60:
            return None
        return int(minutes * 60 + seconds)
    hours, minutes, seconds = numbers
    if minutes >= 60 or seconds >= 60:
        return None
    return int(hours * 3600 + minutes * 60 + seconds)


def parse_feed_date(entry: Mapping[str, Any]) -> datetime | None:
    """Prefer published date, then updated date, normalized to UTC."""
    for prefix in ("published", "updated"):
        parsed = entry.get(f"{prefix}_parsed")
        if parsed:
            try:
                return datetime(*parsed[:6], tzinfo=timezone.utc)
            except (TypeError, ValueError, OverflowError):
                pass

        raw = entry.get(prefix)
        if not raw:
            continue
        try:
            value = parsedate_to_datetime(str(raw))
        except (TypeError, ValueError, OverflowError):
            try:
                value = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
            except (TypeError, ValueError, OverflowError):
                continue
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)
    return None


def utc_iso(value: datetime | None) -> str | None:
    if value is None:
        return None
    normalized = value.astimezone(timezone.utc).replace(microsecond=0)
    return normalized.isoformat().replace("+00:00", "Z")


def stable_item_id(source_id: str, guid: str | None, page_url: str | None) -> str | None:
    identity = guid.strip() if isinstance(guid, str) and guid.strip() else page_url
    if not identity:
        return None
    digest = hashlib.sha256(f"{source_id}:{identity}".encode("utf-8")).hexdigest()
    return f"{source_id}-{digest[:ITEM_ID_HASH_LENGTH]}"


def entry_guid(entry: Mapping[str, Any]) -> str | None:
    for key in ("id", "guid"):
        value = entry.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def entry_page_url(entry: Mapping[str, Any]) -> str | None:
    direct = public_url(entry.get("link"))
    if direct:
        return direct
    for link in entry.get("links") or []:
        if not isinstance(link, Mapping):
            continue
        rel = str(link.get("rel") or "alternate").lower()
        media_type = str(link.get("type") or "").lower()
        if rel in {"alternate", "canonical"} and not media_type.startswith("audio/"):
            candidate = public_url(link.get("href"))
            if candidate:
                return candidate
    return None


def entry_audio_url(entry: Mapping[str, Any]) -> str | None:
    for enclosure in entry.get("enclosures") or []:
        if not isinstance(enclosure, Mapping):
            continue
        media_type = str(enclosure.get("type") or "").lower()
        if media_type.startswith("audio/") or not media_type:
            candidate = public_url(enclosure.get("href") or enclosure.get("url"))
            if candidate:
                return candidate
    for link in entry.get("links") or []:
        if not isinstance(link, Mapping):
            continue
        rel = str(link.get("rel") or "").lower()
        media_type = str(link.get("type") or "").lower()
        if rel == "enclosure" and (media_type.startswith("audio/") or not media_type):
            candidate = public_url(link.get("href"))
            if candidate:
                return candidate
    return None


def _transcript_candidate(value: Any) -> str | None:
    if isinstance(value, str):
        return public_url(value)
    if isinstance(value, Mapping):
        return public_url(value.get("url") or value.get("href") or value.get("src"))
    if isinstance(value, Sequence):
        for item in value:
            candidate = _transcript_candidate(item)
            if candidate:
                return candidate
    return None


def entry_transcript_url(entry: Mapping[str, Any]) -> str | None:
    for key in (
        "podcast_transcript",
        "podcast_transcripts",
        "podcastindex_transcript",
        "transcript",
        "transcripts",
    ):
        candidate = _transcript_candidate(entry.get(key))
        if candidate:
            return candidate

    for link in entry.get("links") or []:
        if not isinstance(link, Mapping):
            continue
        rel = str(link.get("rel") or "").lower()
        media_type = str(link.get("type") or "").lower()
        if rel in {"transcript", TRANSCRIPT_REL}:
            candidate = public_url(link.get("href"))
            if candidate:
                return candidate
    return None


def entry_description(entry: Mapping[str, Any]) -> str:
    for key in ("summary", "description", "subtitle"):
        value = entry.get(key)
        if value:
            return clean_text(value, DESCRIPTION_LIMIT)
    content = entry.get("content") or []
    if isinstance(content, Sequence) and content:
        first = content[0]
        if isinstance(first, Mapping):
            return clean_text(first.get("value"), DESCRIPTION_LIMIT)
    return ""


@lru_cache(maxsize=None)
def keyword_pattern(keyword: str) -> re.Pattern[str]:
    """Case-insensitive whole-word pattern; allows a simple plural suffix."""
    return re.compile(r"(?<!\w)" + re.escape(keyword.casefold()) + r"(?:es|s)?(?!\w)")


def matches_keywords(text: str, source: Source) -> bool:
    searchable = text.casefold()
    if any(keyword_pattern(keyword).search(searchable) for keyword in source.exclude_keywords):
        return False
    if not source.include_keywords:
        return True
    return any(keyword_pattern(keyword).search(searchable) for keyword in source.include_keywords)


def build_item(entry: Mapping[str, Any], source: Source) -> tuple[dict[str, Any] | None, str | None]:
    title = clean_text(entry.get("title"))
    description = entry_description(entry)
    if not title:
        return None, "missing title"

    page_url = entry_page_url(entry)
    guid = entry_guid(entry)
    item_id = stable_item_id(source.source_id, guid, page_url)
    if not item_id:
        return None, "missing GUID and page URL"

    published = parse_feed_date(entry)
    duration = parse_duration(entry.get("itunes_duration") or entry.get("duration"))
    if duration is None:
        for enclosure in entry.get("enclosures") or []:
            if isinstance(enclosure, Mapping):
                duration = parse_duration(enclosure.get("duration") or enclosure.get("length_seconds"))
                if duration is not None:
                    break

    return {
        "item_id": item_id,
        "source_id": source.source_id,
        "source_name": source.name,
        "guid": guid,
        "title": title,
        "url": page_url,
        "published_at": utc_iso(published),
        "description": description,
        "audio_url": entry_audio_url(entry),
        "transcript_url": entry_transcript_url(entry),
        "duration_seconds": duration,
        "status": "pending",
        "reason": None,
    }, None


def keyword_list(value: Any, field: str) -> tuple[str, ...]:
    """Validate, normalize, and de-duplicate configured keyword strings."""
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise CollectorError(f"{field} must be a list of strings")
    return tuple(dict.fromkeys(item.strip() for item in value))


def load_sources(path: Path) -> list[Source]:
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise CollectorError(f"cannot read config {path}: {error}") from error
    except (UnicodeError, yaml.YAMLError) as error:
        raise CollectorError(f"invalid YAML in {path}: {error}") from error

    rows = raw.get("sources") if isinstance(raw, Mapping) else None
    if not isinstance(rows, list):
        raise CollectorError("config must contain a sources list")

    global_exclude_keywords = keyword_list(raw.get("global_exclude_keywords", []), "global_exclude_keywords")

    sources: list[Source] = []
    seen_ids: set[str] = set()
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, Mapping):
            raise CollectorError(f"source #{index} must be an object")
        source_id = row.get("id")
        name = row.get("name")
        url = public_url(row.get("url"))
        enabled = row.get("enabled", True)
        if not isinstance(source_id, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", source_id):
            raise CollectorError(f"source #{index} has invalid id")
        if source_id in seen_ids:
            raise CollectorError(f"duplicate source id: {source_id}")
        if not isinstance(name, str) or not name.strip():
            raise CollectorError(f"source {source_id} has invalid name")
        if not url:
            raise CollectorError(f"source {source_id} must use a public http(s) URL")
        if not isinstance(enabled, bool):
            raise CollectorError(f"source {source_id} enabled must be true or false")

        minimum = row.get("min_duration_minutes")
        if minimum is not None and (isinstance(minimum, bool) or not isinstance(minimum, (int, float)) or minimum < 0):
            raise CollectorError(f"source {source_id} min_duration_minutes must be null or non-negative")

        seen_ids.add(source_id)
        sources.append(
            Source(
                source_id=source_id,
                name=name.strip(),
                url=url,
                enabled=enabled,
                include_keywords=keyword_list(row.get("include_keywords", []), f"source {source_id} include_keywords"),
                exclude_keywords=global_exclude_keywords
                + keyword_list(row.get("exclude_keywords", []), f"source {source_id} exclude_keywords"),
                min_duration_minutes=float(minimum) if minimum is not None else None,
            )
        )
    return sources


def resolve_public_host(url: str) -> None:
    parsed = urlparse(url)
    hostname = parsed.hostname
    if not hostname:
        raise CollectorError("feed URL has no hostname")
    try:
        addresses = socket.getaddrinfo(hostname, parsed.port or (443 if parsed.scheme == "https" else 80), type=socket.SOCK_STREAM)
    except socket.gaierror as error:
        raise CollectorError(f"cannot resolve feed hostname: {error}") from error
    for result in addresses:
        address_text = result[4][0].split("%", 1)[0]
        try:
            address = ipaddress.ip_address(address_text)
        except ValueError as error:
            raise CollectorError(f"invalid resolved feed address: {address_text}") from error
        if not address.is_global:
            raise CollectorError(f"feed hostname resolves to non-public address: {address_text}")


def fetch_feed(url: str, timeout: float, retries: int) -> bytes:
    resolve_public_host(url)
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*;q=0.1"})
    opener = build_opener(_PublicRedirectHandler())
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with opener.open(request, timeout=timeout) as response:
                final_url = public_url(response.geturl())
                if not final_url:
                    raise CollectorError("feed redirected to a non-public URL")
                resolve_public_host(final_url)
                status = getattr(response, "status", 200)
                if status < 200 or status >= 300:
                    raise CollectorError(f"HTTP {status}")
                return response.read()
        except (HTTPError, URLError, TimeoutError, socket.timeout, OSError, CollectorError) as error:
            last_error = error
            if attempt < retries:
                time.sleep(0.5 * (2**attempt))
    raise CollectorError(f"request failed after {retries + 1} attempt(s): {last_error}")


def parse_feed(data: bytes) -> list[Mapping[str, Any]]:
    parsed = feedparser.parse(data)
    entries = [dict(entry) for entry in parsed.entries or []]
    if getattr(parsed, "bozo", False) and not entries:
        raise CollectorError(f"feed parse failed: {parsed.bozo_exception}")
    return entries


def write_item(output_dir: Path, item: Mapping[str, Any]) -> bool:
    path = output_dir / pending.item_relpath(item)
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(item, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    try:
        with path.open("x", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
    except FileExistsError:
        return False
    return True


def write_collection_stamp(stamp_file: Path, now: datetime) -> None:
    """Record the collection run time. The file lives outside the items directory
    (default: its parent), so data/items keeps its strict
    <source_id>/<year>/<item_id>.json layout; container runs pass --stamp-file
    because mounted output paths have no meaningful parent."""
    stamp = {"last_collected_at": utc_iso(now)}
    stamp_file.parent.mkdir(parents=True, exist_ok=True)
    stamp_file.write_text(json.dumps(stamp, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def collect_source(
    source: Source,
    output_dir: Path,
    now: datetime,
    timeout: float,
    retries: int,
    lookback_days: int,
    fetcher: Callable[[str, float, int], bytes],
) -> SourceSummary:
    summary = SourceSummary(source.source_id, source.name, "success")
    entries = parse_feed(fetcher(source.url, timeout, retries))
    summary.entries = len(entries)
    cutoff = now.astimezone(timezone.utc) - timedelta(days=lookback_days)
    unknown_date_accepted = 0

    for entry in entries:
        item, _ = build_item(entry, source)
        if item is None:
            summary.skipped += 1
            continue

        published = item["published_at"]
        if published is None:
            if unknown_date_accepted >= MAX_UNKNOWN_DATES_PER_SOURCE:
                summary.filtered += 1
                continue
        else:
            published_datetime = datetime.fromisoformat(published.replace("Z", "+00:00"))
            if published_datetime < cutoff:
                summary.filtered += 1
                continue

        search_text = clean_text(f"{item['title']} {item['description']}")
        if not matches_keywords(search_text, source):
            summary.filtered += 1
            continue

        duration = item["duration_seconds"]
        if source.min_duration_minutes is not None and duration is not None:
            if duration < source.min_duration_minutes * 60:
                summary.filtered += 1
                continue

        created = write_item(output_dir, item)
        if created and published is None:
            unknown_date_accepted += 1
        if created:
            summary.new += 1
        else:
            summary.existing += 1

    return summary


def pending_count(output_dir: Path) -> tuple[int, int]:
    pending = 0
    malformed = 0
    for path in sorted(
        output_dir.rglob("*.json"), key=lambda candidate: candidate.relative_to(output_dir).as_posix()
    ):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            malformed += 1
            continue
        if isinstance(value, Mapping) and value.get("status") == "pending":
            pending += 1
    return pending, malformed


def render_summary(summaries: Sequence[SourceSummary], output_dir: Path) -> str:
    pending, malformed = pending_count(output_dir)
    lines = [
        "## EchoForge podcast collection",
        "",
        "| Source | Result | Entries | New | Existing | Filtered | Skipped |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for summary in summaries:
        result = summary.status if not summary.error else f"error: {summary.error}"
        result = result.replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {summary.source_name} (`{summary.source_id}`) | {result} | {summary.entries} | "
            f"{summary.new} | {summary.existing} | {summary.filtered} | {summary.skipped} |"
        )
    successful = sum(summary.status == "success" for summary in summaries)
    failed = sum(summary.status == "error" for summary in summaries)
    added = sum(summary.new for summary in summaries)
    filtered = sum(summary.filtered for summary in summaries)
    skipped = sum(summary.skipped for summary in summaries)
    lines.extend(
        [
            "",
            f"- Enabled sources: {len(summaries)} ({successful} succeeded, {failed} failed)",
            f"- New items: {added}",
            f"- Filtered entries: {filtered}",
            f"- Skipped invalid entries: {skipped}",
            f"- Current pending items: {pending}",
        ]
    )
    if malformed:
        lines.append(f"- Existing malformed JSON files: {malformed}")
    return "\n".join(lines) + "\n"


def write_step_summary(text: str) -> None:
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if not path:
        return
    try:
        with open(path, "a", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
    except OSError as error:
        print(f"warning: could not write GITHUB_STEP_SUMMARY: {error}", file=sys.stderr)


def collect(
    config_path: Path,
    output_dir: Path,
    now: datetime,
    timeout: float = DEFAULT_TIMEOUT_SECONDS,
    retries: int = DEFAULT_RETRIES,
    lookback_days: int = DEFAULT_LOOKBACK_DAYS,
    fetcher: Callable[[str, float, int], bytes] = fetch_feed,
    stamp_file: Path | None = None,
) -> tuple[int, list[SourceSummary], str]:
    if timeout <= 0:
        raise CollectorError("timeout must be positive")
    if retries < 0:
        raise CollectorError("retries must be non-negative")
    if lookback_days < 1:
        raise CollectorError("lookback days must be at least 1")
    sources = [source for source in load_sources(config_path) if source.enabled]
    if not sources:
        raise CollectorError("config has no enabled sources")
    output_dir.mkdir(parents=True, exist_ok=True)
    if not output_dir.is_dir():
        raise CollectorError(f"output path is not a directory: {output_dir}")

    summaries: list[SourceSummary] = []
    for source in sources:
        try:
            summary = collect_source(source, output_dir, now, timeout, retries, lookback_days, fetcher)
        except Exception as error:
            summary = SourceSummary(source.source_id, source.name, "error", error=str(error))
        summaries.append(summary)

    write_collection_stamp(stamp_file if stamp_file is not None else output_dir.parent / "collected-at.json", now)
    text = render_summary(summaries, output_dir)
    return (1 if all(summary.status == "error" for summary in summaries) else 0), summaries, text


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("config/sources.yaml"))
    parser.add_argument("--output-dir", type=Path, default=Path("data/items"))
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--retries", type=int, default=DEFAULT_RETRIES)
    parser.add_argument(
        "--lookback-days",
        type=int,
        default=DEFAULT_LOOKBACK_DAYS,
        help="Intake window in days (default 30); raise it for local cold starts or outage backfill.",
    )
    parser.add_argument(
        "--stamp-file",
        type=Path,
        default=None,
        help="Where to write the collection run time (default: collected-at.json next to the output directory).",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        exit_code, _, summary = collect(
            args.config,
            args.output_dir,
            datetime.now(timezone.utc),
            timeout=args.timeout,
            retries=args.retries,
            lookback_days=args.lookback_days,
            stamp_file=args.stamp_file,
        )
    except CollectorError as error:
        summary = f"## EchoForge podcast collection\n\nCollection failed: {error}\n"
        print(summary, file=sys.stderr, end="")
        write_step_summary(summary)
        return 2

    print(summary, end="")
    write_step_summary(summary)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
