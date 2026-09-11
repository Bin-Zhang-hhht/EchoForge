#!/usr/bin/env python3
"""Reserve the single ASR slot for a local podcast processing batch."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

import archive_transcript as archive


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--item-id", required=True)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--measured-audio-seconds", type=float, required=True)
    parser.add_argument("--items-dir", type=Path, default=Path("data/items"))
    parser.add_argument("--library-dir", type=Path, default=Path("local-library"))
    parser.add_argument("--reserved-at", default=archive.utc_now())
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        reserved_at = archive.validate_utc_timestamp(args.reserved_at)
        item = archive.load_item(args.items_dir, args.item_id)
        record = archive.reserve_asr_batch(
            args.library_dir,
            args.batch_id,
            item,
            args.measured_audio_seconds,
            reserved_at,
        )
    except archive.ArchiveError as error:
        print(f"ASR reservation failed: {error}", file=__import__("sys").stderr)
        return 2
    print(f"ASR slot reserved: {record}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
