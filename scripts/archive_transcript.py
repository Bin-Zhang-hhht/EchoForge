#!/usr/bin/env python3
"""Archive a reviewed podcast transcript in the private local library."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import socket
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

import yaml

import collect
import pending

MAX_TRANSCRIPT_BYTES = 25 * 1024 * 1024
MAX_BATCH_ARTICLES = 3
MAX_BATCH_ASR_ITEMS = 1
MAX_BATCH_ASR_SECONDS = 120 * 60
USER_AGENT = "EchoForge/0.1 transcript resolver"
INPUT_TYPES = {"official_transcript", "video_agent_kit_asr"}
SOURCE_KINDS = {"rss", "publisher", "video_agent_kit"}
FORMATS = {"plain", "html", "vtt", "srt", "json"}
TIMESTAMP_COVERAGE = {"passed", "not_available", "not_applicable"}


class ArchiveError(Exception):
    """Raised when transcript input or archive metadata is invalid."""


class _PublicRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, new_url):  # type: ignore[no-untyped-def]
        candidate = collect.public_url(new_url)
        if not candidate:
            raise ArchiveError("transcript redirected to a non-public URL")
        collect.resolve_public_host(candidate)
        return super().redirect_request(request, fp, code, msg, headers, candidate)


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def validate_utc_timestamp(value: str) -> str:
    if not pending.UTC_ISO_PATTERN.fullmatch(value):
        raise ArchiveError("--retrieved-at must be UTC ISO-8601 ending in Z")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as error:
        raise ArchiveError("--retrieved-at is not a valid timestamp") from error
    return value


def load_item(items_dir: Path, item_id: str) -> dict[str, Any]:
    path = items_dir / f"{item_id}.json"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except OSError as error:
        raise ArchiveError(f"cannot read item metadata {path}: {error}") from error
    except (UnicodeError, json.JSONDecodeError) as error:
        raise ArchiveError(f"invalid item metadata {path}: {error}") from error

    errors = pending.validate_item(value, path)
    if errors:
        raise ArchiveError(f"invalid item metadata {path}: {'; '.join(errors)}")
    return dict(value)


def fetch_transcript(url: str, timeout: float, retries: int) -> tuple[bytes, str, str | None]:
    candidate = collect.public_url(url)
    if not candidate:
        raise ArchiveError("transcript URL must be a public http(s) URL")
    collect.resolve_public_host(candidate)
    request = Request(
        candidate,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/plain, text/vtt, application/json, text/html, application/xhtml+xml;q=0.8, */*;q=0.1",
        },
    )
    opener = build_opener(_PublicRedirectHandler())
    last_error: Exception | None = None

    for attempt in range(retries + 1):
        try:
            with opener.open(request, timeout=timeout) as response:
                final_url = collect.public_url(response.geturl())
                if not final_url:
                    raise ArchiveError("transcript redirected to a non-public URL")
                collect.resolve_public_host(final_url)
                status = getattr(response, "status", 200)
                if status < 200 or status >= 300:
                    raise ArchiveError(f"transcript request returned HTTP {status}")
                declared_length = response.headers.get("Content-Length")
                if declared_length and int(declared_length) > MAX_TRANSCRIPT_BYTES:
                    raise ArchiveError("transcript exceeds the 25 MiB limit")
                payload = response.read(MAX_TRANSCRIPT_BYTES + 1)
                if len(payload) > MAX_TRANSCRIPT_BYTES:
                    raise ArchiveError("transcript exceeds the 25 MiB limit")
                return payload, final_url, response.headers.get_content_type()
        except (HTTPError, URLError, TimeoutError, socket.timeout, OSError, ValueError, ArchiveError) as error:
            last_error = error
            if attempt < retries:
                continue
    raise ArchiveError(f"transcript request failed after {retries + 1} attempt(s): {last_error}")


def read_transcript_file(path: Path) -> bytes:
    try:
        size = path.stat().st_size
        if not path.is_file():
            raise ArchiveError(f"transcript input is not a file: {path}")
        if size > MAX_TRANSCRIPT_BYTES:
            raise ArchiveError("transcript exceeds the 25 MiB limit")
        return path.read_bytes()
    except OSError as error:
        raise ArchiveError(f"cannot read transcript input {path}: {error}") from error


def detect_format(explicit: str | None, source_name: str, content_type: str | None) -> str:
    if explicit:
        return explicit
    suffix = Path(urlparse(source_name).path).suffix.casefold()
    suffix_map = {
        ".txt": "plain",
        ".md": "plain",
        ".html": "html",
        ".htm": "html",
        ".vtt": "vtt",
        ".srt": "srt",
        ".json": "json",
    }
    if suffix in suffix_map:
        return suffix_map[suffix]
    media_type = (content_type or "").casefold()
    if media_type in {"text/html", "application/xhtml+xml"}:
        return "html"
    if media_type in {"text/vtt", "application/x-subrip"}:
        return "vtt" if media_type == "text/vtt" else "srt"
    if media_type in {"application/json", "application/ld+json"}:
        return "json"
    if media_type.startswith("text/"):
        return "plain"
    raise ArchiveError("cannot detect transcript format; pass --format")


def decode_text(payload: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-16", "utf-16-le", "utf-16-be"):
        try:
            return payload.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ArchiveError("transcript must use UTF-8 or UTF-16 text encoding")


def seconds_from_timestamp(value: str) -> float | None:
    normalized = value.strip().replace(",", ".")
    parts = normalized.split(":")
    if len(parts) == 2:
        parts.insert(0, "0")
    if len(parts) != 3:
        return None
    try:
        hours, minutes, seconds = int(parts[0]), int(parts[1]), float(parts[2])
    except ValueError:
        return None
    if hours < 0 or minutes not in range(60) or not 0 <= seconds < 60:
        return None
    return hours * 3600 + minutes * 60 + seconds


def normalize_timestamp(value: Any) -> str | None:
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        seconds = float(value)
    else:
        parsed = seconds_from_timestamp(str(value))
        if parsed is None:
            return None
        seconds = parsed
    if not math.isfinite(seconds) or seconds < 0:
        return None
    whole = int(seconds)
    hours, remainder = divmod(whole, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def parse_timed_text(text: str, source_format: str) -> tuple[str, bool]:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    blocks = re.split(r"\n\s*\n", normalized)
    lines: list[str] = []
    timing_pattern = re.compile(
        r"(?P<start>\d{1,2}:\d{2}(?::\d{2})?[.,]\d{3})\s+-->\s+(?P<end>\d{1,2}:\d{2}(?::\d{2})?[.,]\d{3})"
    )
    for block in blocks:
        block_lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not block_lines or block_lines[0].upper().startswith("WEBVTT"):
            continue
        timing_index = next((index for index, line in enumerate(block_lines) if timing_pattern.search(line)), None)
        if timing_index is None:
            continue
        match = timing_pattern.search(block_lines[timing_index])
        assert match is not None
        timestamp = normalize_timestamp(match.group("start"))
        cue = collect.clean_text(" ".join(block_lines[timing_index + 1 :]))
        if timestamp and cue:
            lines.append(f"[{timestamp}] {cue}")
    if not lines:
        raise ArchiveError(f"{source_format.upper()} input contains no readable timed cues")
    return "\n\n".join(lines), True


def json_segments(value: Any) -> list[Mapping[str, Any]]:
    if isinstance(value, list):
        return [segment for segment in value if isinstance(segment, Mapping)]
    if not isinstance(value, Mapping):
        return []
    for key in ("segments", "transcript", "utterances", "results"):
        candidate = value.get(key)
        if isinstance(candidate, list):
            return [segment for segment in candidate if isinstance(segment, Mapping)]
    return []


def parse_json_transcript(text: str) -> tuple[str, bool]:
    try:
        value = json.loads(text)
    except json.JSONDecodeError as error:
        raise ArchiveError(f"invalid transcript JSON at line {error.lineno}, column {error.colno}") from error

    segments = json_segments(value)
    lines: list[str] = []
    has_timestamps = False
    for segment in segments:
        content = collect.clean_text(segment.get("text") or segment.get("content") or segment.get("transcript"))
        if not content:
            continue
        start_value = segment.get("start")
        if start_value is None:
            start_value = segment.get("start_time")
        if start_value is None:
            start_value = segment.get("offset")
        timestamp = normalize_timestamp(start_value)
        if start_value is not None and timestamp is None:
            raise ArchiveError("transcript JSON contains an invalid timestamp")
        speaker = collect.clean_text(segment.get("speaker") or segment.get("speaker_name"))
        prefix_parts: list[str] = []
        if timestamp:
            prefix_parts.append(f"[{timestamp}]")
            has_timestamps = True
        if speaker:
            prefix_parts.append(f"{speaker}:")
        prefix = " ".join(prefix_parts)
        lines.append(f"{prefix} {content}".strip())

    if not lines and isinstance(value, Mapping):
        content = value.get("text") or value.get("content")
        if isinstance(content, str) and content.strip():
            lines.append(content.strip())
    if not lines:
        raise ArchiveError("transcript JSON contains no readable transcript text")
    return "\n\n".join(lines), has_timestamps


def convert_transcript(payload: bytes, source_format: str) -> tuple[str, bool, str | None]:
    text = decode_text(payload)
    raw_name: str | None = None
    if source_format == "plain":
        transcript = text.replace("\r\n", "\n").replace("\r", "\n").strip()
        has_timestamps = False
    elif source_format == "html":
        transcript = collect.clean_text(text)
        has_timestamps = False
    elif source_format in {"vtt", "srt"}:
        transcript, has_timestamps = parse_timed_text(text, source_format)
        raw_name = f"transcript.{source_format}"
    elif source_format == "json":
        transcript, has_timestamps = parse_json_transcript(text)
        raw_name = "transcript.json"
    else:
        raise ArchiveError(f"unsupported transcript format: {source_format}")

    if len(transcript) < 200:
        raise ArchiveError("transcript is too short to archive; confirm that the source is a full transcript")
    return transcript, has_timestamps, raw_name


def validate_review(args: argparse.Namespace, item: Mapping[str, Any], has_timestamps: bool) -> None:
    missing = [
        flag
        for flag, present in (
            ("--identity-confirmed", args.identity_confirmed),
            ("--transcript-confirmed", args.transcript_confirmed),
            ("--complete", args.complete),
            ("--readable", args.readable),
        )
        if not present
    ]
    if missing:
        raise ArchiveError(f"review confirmation required: {', '.join(missing)}")
    if not args.notes or not args.notes.strip():
        raise ArchiveError("--notes must record the material usability conclusion")
    if args.input_type == "official_transcript" and args.source_kind not in {"rss", "publisher"}:
        raise ArchiveError("official transcript source kind must be rss or publisher")
    if args.input_type == "video_agent_kit_asr":
        if args.source_kind != "video_agent_kit":
            raise ArchiveError("ASR source kind must be video_agent_kit")
        duration = item.get("duration_seconds")
        if duration is None:
            raise ArchiveError("ASR requires a known episode duration before budget approval")
        if args.batch_asr_count >= MAX_BATCH_ASR_ITEMS:
            raise ArchiveError("batch ASR item limit exceeded (maximum 1)")
        if args.batch_asr_seconds + duration > MAX_BATCH_ASR_SECONDS:
            raise ArchiveError("batch ASR duration limit exceeded (maximum 120 minutes)")
        if not args.listening_resolved:
            raise ArchiveError("ASR archive requires --listening-resolved after required spot checks")
    if has_timestamps:
        expected = "passed" if item.get("duration_seconds") is not None else "not_available"
        if args.timestamp_coverage != expected:
            raise ArchiveError(
                "timed transcript coverage must be passed for known duration or not_available when duration is unknown"
            )
    elif args.timestamp_coverage != "not_applicable":
        raise ArchiveError("untimed transcript must use --timestamp-coverage not_applicable")


def render_transcript(item: Mapping[str, Any], transcript: str, input_type: str, source_url: str) -> str:
    return (
        f"# {item['title']}\n\n"
        f"- Item ID: `{item['item_id']}`\n"
        f"- Source: {item['source_name']}\n"
        f"- Acquisition: `{input_type}`\n"
        f"- Transcript source: {source_url}\n\n"
        "## 完整逐字稿\n\n"
        f"{transcript.strip()}\n"
    )


def validate_existing_archive(
    *,
    target: Path,
    item: Mapping[str, Any],
    payload: bytes,
    transcript: str,
    raw_name: str | None,
    source_format: str,
    source_url: str,
    input_type: str,
    source_kind: str,
    timestamp_coverage: str,
) -> None:
    metadata_path = target / "metadata.yaml"
    try:
        existing = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise ArchiveError(f"existing archive cannot be validated: {error}") from error
    if not isinstance(existing, Mapping):
        raise ArchiveError("existing archive cannot be validated: metadata must be a mapping")

    expected_values = {
        "item_id": item["item_id"],
        "source_id": item["source_id"],
        "title": item["title"],
        "input_type": input_type,
        "source_kind": source_kind,
        "source_url": source_url,
        "source_format": source_format,
        "content_sha256": hashlib.sha256(payload).hexdigest(),
        "asset_files": ["transcript.md"] + ([raw_name] if raw_name else []),
    }
    mismatches = [key for key, expected in expected_values.items() if existing.get(key) != expected]
    if mismatches:
        raise ArchiveError(
            f"existing archive has different content or provenance: {', '.join(mismatches)}"
        )

    retrieved_at = existing.get("retrieved_at")
    if not isinstance(retrieved_at, str):
        raise ArchiveError("existing archive cannot be validated: missing retrieved_at")
    validate_utc_timestamp(retrieved_at)

    checks = existing.get("content_checks")
    if not isinstance(checks, Mapping):
        raise ArchiveError("existing archive cannot be validated: missing content_checks")
    required_checks: dict[str, Any] = {
        "episode_identity": "passed",
        "transcript_kind": "passed",
        "completeness": "passed",
        "readability": "passed",
        "timestamp_coverage": timestamp_coverage,
        "required_listening_questions_resolved": True if input_type == "video_agent_kit_asr" else "not_applicable",
        "checked_by": "zcode",
    }
    invalid_checks = [key for key, expected in required_checks.items() if checks.get(key) != expected]
    if invalid_checks or not isinstance(checks.get("notes"), str) or not checks["notes"].strip():
        details = invalid_checks + ([] if isinstance(checks.get("notes"), str) and checks["notes"].strip() else ["notes"])
        raise ArchiveError(
            f"existing archive cannot be validated: invalid content checks: {', '.join(details)}"
        )

    transcript_path = target / "transcript.md"
    expected_transcript = render_transcript(item, transcript, input_type, source_url)
    try:
        if transcript_path.read_text(encoding="utf-8") != expected_transcript:
            raise ArchiveError("existing archive has different or corrupted transcript.md")
        if raw_name and (target / raw_name).read_bytes() != payload:
            raise ArchiveError(f"existing archive has different or corrupted {raw_name}")
    except OSError as error:
        raise ArchiveError(f"existing archive cannot be validated: {error}") from error
    except UnicodeError as error:
        raise ArchiveError(f"existing archive cannot be validated: invalid transcript UTF-8: {error}") from error


def archive_transcript(
    *,
    item: Mapping[str, Any],
    payload: bytes,
    source_format: str,
    source_url: str,
    input_type: str,
    source_kind: str,
    retrieved_at: str,
    timestamp_coverage: str,
    listening_resolved: bool,
    notes: str,
    library_dir: Path,
) -> tuple[Path, bool]:
    transcript, has_timestamps, raw_name = convert_transcript(payload, source_format)
    target = library_dir / str(item["source_id"]) / str(item["item_id"])
    digest = hashlib.sha256(payload).hexdigest()

    if target.exists():
        validate_existing_archive(
            target=target,
            item=item,
            payload=payload,
            transcript=transcript,
            raw_name=raw_name,
            source_format=source_format,
            source_url=source_url,
            input_type=input_type,
            source_kind=source_kind,
            timestamp_coverage=timestamp_coverage,
        )
        return target, False

    metadata = {
        "item_id": item["item_id"],
        "source_id": item["source_id"],
        "title": item["title"],
        "input_type": input_type,
        "source_kind": source_kind,
        "source_url": source_url,
        "retrieved_at": retrieved_at,
        "source_format": source_format,
        "content_sha256": digest,
        "asset_files": ["transcript.md"] + ([raw_name] if raw_name else []),
        "content_checks": {
            "episode_identity": "passed",
            "transcript_kind": "passed",
            "completeness": "passed",
            "readability": "passed",
            "timestamp_coverage": timestamp_coverage,
            "required_listening_questions_resolved": listening_resolved if input_type == "video_agent_kit_asr" else "not_applicable",
            "checked_by": "zcode",
            "notes": notes.strip(),
        },
    }

    parent = target.parent
    parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{item['item_id']}-", dir=parent))
    try:
        (temporary / "transcript.md").write_text(
            render_transcript(item, transcript, input_type, source_url), encoding="utf-8", newline="\n"
        )
        if raw_name:
            (temporary / raw_name).write_bytes(payload)
        (temporary / "metadata.yaml").write_text(
            yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False), encoding="utf-8", newline="\n"
        )
        temporary.replace(target)
    except Exception:
        shutil.rmtree(temporary, ignore_errors=True)
        raise
    return target, True


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--item-id", required=True)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--input-file", type=Path)
    source.add_argument("--transcript-url")
    parser.add_argument("--source-url", help="Public provenance URL; required with --input-file")
    parser.add_argument("--input-type", choices=sorted(INPUT_TYPES), required=True)
    parser.add_argument("--source-kind", choices=sorted(SOURCE_KINDS), required=True)
    parser.add_argument("--format", choices=sorted(FORMATS))
    parser.add_argument("--items-dir", type=Path, default=Path("data/items"))
    parser.add_argument("--library-dir", type=Path, default=Path("local-library"))
    parser.add_argument("--retrieved-at", default=utc_now())
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--identity-confirmed", action="store_true")
    parser.add_argument("--transcript-confirmed", action="store_true")
    parser.add_argument("--complete", action="store_true")
    parser.add_argument("--readable", action="store_true")
    parser.add_argument("--timestamp-coverage", choices=sorted(TIMESTAMP_COVERAGE), required=True)
    parser.add_argument("--listening-resolved", action="store_true")
    parser.add_argument("--notes", required=True)
    parser.add_argument("--batch-asr-count", type=int, default=0)
    parser.add_argument("--batch-asr-seconds", type=int, default=0)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.timeout <= 0 or args.retries < 0:
            raise ArchiveError("--timeout must be positive and --retries must be non-negative")
        if args.batch_asr_count < 0 or args.batch_asr_seconds < 0:
            raise ArchiveError("batch ASR counters must be non-negative")
        retrieved_at = validate_utc_timestamp(args.retrieved_at)
        item = load_item(args.items_dir, args.item_id)

        if args.transcript_url:
            payload, final_url, content_type = fetch_transcript(args.transcript_url, args.timeout, args.retries)
            source_url = final_url
            source_name = final_url
        else:
            source_url = collect.public_url(args.source_url)
            if not source_url:
                raise ArchiveError("--source-url must be a public http(s) URL with --input-file")
            assert args.input_file is not None
            payload = read_transcript_file(args.input_file)
            content_type = None
            source_name = args.input_file.name

        if args.input_type == "video_agent_kit_asr" and source_url != item.get("audio_url"):
            raise ArchiveError("ASR source URL must match the item's audio_url")
        source_format = detect_format(args.format, source_name, content_type)
        _, has_timestamps, _ = convert_transcript(payload, source_format)
        validate_review(args, item, has_timestamps)
        target, created = archive_transcript(
            item=item,
            payload=payload,
            source_format=source_format,
            source_url=source_url,
            input_type=args.input_type,
            source_kind=args.source_kind,
            retrieved_at=retrieved_at,
            timestamp_coverage=args.timestamp_coverage,
            listening_resolved=args.listening_resolved,
            notes=args.notes,
            library_dir=args.library_dir,
        )
    except (ArchiveError, collect.CollectorError) as error:
        print(f"Transcript archive failed: {error}", file=__import__("sys").stderr)
        return 2

    action = "Archived" if created else "Already archived"
    print(f"{action}: {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
