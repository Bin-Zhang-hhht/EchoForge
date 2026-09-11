#!/usr/bin/env python3
"""Validate collected item metadata and list pending candidates."""

from __future__ import annotations

import argparse
import ipaddress
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Sequence
from urllib.parse import urlparse

ITEM_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*-[0-9a-f]{12}$")
SOURCE_ID_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
UTC_ISO_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
ALLOWED_STATUSES = {"pending", "processed", "ignored", "failed"}
REQUIRED_FIELDS = {
    "item_id",
    "source_id",
    "source_name",
    "guid",
    "title",
    "url",
    "published_at",
    "description",
    "audio_url",
    "transcript_url",
    "duration_seconds",
    "status",
    "reason",
}


def is_public_http_url(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = urlparse(value)
        port = parsed.port
    except ValueError:
        return False
    if (
        parsed.scheme.lower() not in {"http", "https"}
        or not parsed.netloc
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or (port is not None and not 1 <= port <= 65535)
    ):
        return False
    hostname = parsed.hostname.rstrip(".").casefold()
    if hostname == "localhost" or hostname.endswith(".localhost") or hostname.endswith(".local"):
        return False
    try:
        return ipaddress.ip_address(hostname).is_global
    except ValueError:
        return True


def validate_item(value: Any, path: Path) -> list[str]:
    if not isinstance(value, Mapping):
        return ["top-level JSON value must be an object"]

    errors: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(value))
    extra = sorted(set(value) - REQUIRED_FIELDS)
    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")
    if extra:
        errors.append(f"unexpected fields: {', '.join(extra)}")

    item_id = value.get("item_id")
    source_id = value.get("source_id")
    if not isinstance(item_id, str) or not ITEM_ID_PATTERN.fullmatch(item_id):
        errors.append("item_id must be a safe source-prefixed 12-hex identifier")
    elif path.stem != item_id:
        errors.append("filename must equal item_id + .json")
    if not isinstance(source_id, str) or not SOURCE_ID_PATTERN.fullmatch(source_id):
        errors.append("source_id must be a lowercase kebab-case identifier")
    elif isinstance(item_id, str) and not item_id.startswith(f"{source_id}-"):
        errors.append("item_id must start with source_id")

    for field in ("source_name", "title"):
        if not isinstance(value.get(field), str) or not value[field].strip():
            errors.append(f"{field} must be a non-empty string")

    guid = value.get("guid")
    if guid is not None and (not isinstance(guid, str) or not guid.strip()):
        errors.append("guid must be null or a non-empty string")

    for field in ("url", "audio_url", "transcript_url"):
        field_value = value.get(field)
        if field_value is not None and not is_public_http_url(field_value):
            errors.append(f"{field} must be null or a public http(s) URL")
    if guid is None and value.get("url") is None:
        errors.append("at least one of guid or url must be present")

    published_at = value.get("published_at")
    if published_at is not None:
        if not isinstance(published_at, str) or not UTC_ISO_PATTERN.fullmatch(published_at):
            errors.append("published_at must be null or UTC ISO-8601 ending in Z")
        else:
            try:
                datetime.fromisoformat(published_at.replace("Z", "+00:00"))
            except ValueError:
                errors.append("published_at is not a valid date-time")

    description = value.get("description")
    if not isinstance(description, str):
        errors.append("description must be a string")
    elif len(description) > 1000:
        errors.append("description must not exceed 1000 characters")

    duration = value.get("duration_seconds")
    if duration is not None and (isinstance(duration, bool) or not isinstance(duration, int) or duration < 0):
        errors.append("duration_seconds must be null or a non-negative integer")

    status = value.get("status")
    if status not in ALLOWED_STATUSES:
        errors.append(f"status must be one of: {', '.join(sorted(ALLOWED_STATUSES))}")
    reason = value.get("reason")
    if reason is not None and (not isinstance(reason, str) or not reason.strip()):
        errors.append("reason must be null or a non-empty string")

    return errors


def load_items(items_dir: Path) -> tuple[list[dict[str, Any]], list[str]]:
    if not items_dir.exists():
        return [], []
    if not items_dir.is_dir():
        return [], [f"{items_dir}: not a directory"]

    items: list[dict[str, Any]] = []
    errors: list[str] = []
    paths_by_item_id: dict[str, list[Path]] = {}
    for path in sorted(items_dir.glob("*.json"), key=lambda candidate: candidate.name):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except OSError as error:
            errors.append(f"{path}: cannot read file: {error}")
            continue
        except (UnicodeError, json.JSONDecodeError) as error:
            if isinstance(error, json.JSONDecodeError):
                errors.append(f"{path}: invalid JSON at line {error.lineno}, column {error.colno}")
            else:
                errors.append(f"{path}: invalid UTF-8: {error}")
            continue

        item_errors = validate_item(value, path)
        if item_errors:
            errors.extend(f"{path}: {error}" for error in item_errors)
            continue
        item = dict(value)
        items.append(item)
        paths_by_item_id.setdefault(item["item_id"], []).append(path)

    for item_id, paths in paths_by_item_id.items():
        if len(paths) > 1:
            for path in paths:
                errors.append(f"{path}: duplicate item_id: {item_id}")
    if any(len(paths) > 1 for paths in paths_by_item_id.values()):
        duplicate_ids = {item_id for item_id, paths in paths_by_item_id.items() if len(paths) > 1}
        items = [item for item in items if item["item_id"] not in duplicate_ids]
    return items, errors


def pending_items(items: Sequence[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    pending = [item for item in items if item["status"] == "pending"]
    pending.sort(key=lambda item: item["item_id"])
    pending.sort(key=lambda item: item["published_at"] or "", reverse=True)
    pending.sort(key=lambda item: item["published_at"] is None)
    return pending


def render(items: Sequence[Mapping[str, Any]], errors: Sequence[str], limit: int | None) -> str:
    candidates = pending_items(items)
    selected = candidates if limit is None else candidates[:limit]
    lines = [
        f"Pending items: {len(candidates)}",
        f"Valid item files: {len(items)}",
        f"Malformed item files: {len({error.split(': ', 1)[0] for error in errors})}",
    ]
    if limit is not None:
        lines.append(f"Candidate window: {len(selected)} (--limit {limit}; not a processing quota)")
    lines.append("")

    if selected:
        for item in selected:
            published = item["published_at"] or "unknown date"
            duration = item["duration_seconds"]
            duration_text = f"{duration}s" if duration is not None else "unknown duration"
            lines.append(
                f"- {published} | {item['item_id']} | {item['source_name']} | "
                f"{item['title']} | {duration_text}"
            )
    else:
        lines.append("No pending candidates.")

    if errors:
        lines.extend(["", "Validation errors:"])
        lines.extend(f"- {error}" for error in errors)
    return "\n".join(lines) + "\n"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--items-dir", type=Path, default=Path("data/items"))
    parser.add_argument("--limit", type=int)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.limit is not None and args.limit < 0:
        print("--limit must be non-negative", file=sys.stderr)
        return 2

    items, errors = load_items(args.items_dir)
    output = render(items, errors, args.limit)
    stream = sys.stderr if errors else sys.stdout
    print(output, file=stream, end="")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
