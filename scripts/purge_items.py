#!/usr/bin/env python3
"""Purge selected content-policy items from all local storage surfaces.

The default is a read-only dry run. Pass explicit item IDs and --execute to
remove their metadata, published posts, local transcript archives, and known
rebuildable collector/site output directories.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

import pending


@dataclass(frozen=True)
class Candidate:
    item_id: str
    paths: tuple[Path, ...]


def candidate_paths(root: Path, item_id: str) -> tuple[Path, ...]:
    item_files = tuple((root / "data" / "items").glob(f"*/*/{item_id}.json"))
    post_files = tuple((root / "site" / "posts").glob(f"*/*/{item_id}.md"))
    archive_dirs = tuple((root / "local-library").glob(f"*/*/{item_id}"))
    cache_items = tuple((root / ".cache").glob(f"**/{item_id}.json"))
    cache_posts = tuple((root / ".cache").glob(f"**/{item_id}.html"))
    return tuple(sorted(set(item_files + post_files + archive_dirs + cache_items + cache_posts)))


def parse_item_ids(values: Iterable[str]) -> list[str]:
    item_ids = sorted(set(values))
    if not item_ids:
        raise ValueError("at least one --item-id is required")
    invalid = [item_id for item_id in item_ids if not pending.ITEM_ID_PATTERN.fullmatch(item_id)]
    if invalid:
        raise ValueError(f"invalid item ID(s): {', '.join(invalid)}")
    return item_ids


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--item-id", action="append", default=[], help="Selected item ID; repeat for every item.")
    parser.add_argument("--execute", action="store_true", help="Delete matched local paths after reporting them.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root to purge from (default: the checkout containing this script).",
    )
    args = parser.parse_args(argv)

    try:
        item_ids = parse_item_ids(args.item_id)
    except ValueError as error:
        parser.error(str(error))

    root = args.root
    candidates = [Candidate(item_id, candidate_paths(root, item_id)) for item_id in item_ids]
    missing = [candidate.item_id for candidate in candidates if not candidate.paths]

    action = "DELETE" if args.execute else "DRY RUN"
    print(f"{action}: {len(candidates)} selected item(s)")
    for candidate in candidates:
        print(f"\n{candidate.item_id}")
        if candidate.paths:
            for path in candidate.paths:
                print(f"  {path.relative_to(root).as_posix()}")
        else:
            print("  (no local paths found)")

    if missing:
        print(f"\nwarning: no local paths found for: {', '.join(missing)}", file=sys.stderr)

    if not args.execute:
        return 0

    for candidate in candidates:
        for path in candidate.paths:
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
    print(f"\nDeleted {sum(len(candidate.paths) for candidate in candidates)} path(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
