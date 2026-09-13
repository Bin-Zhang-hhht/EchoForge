from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import purge_items  # noqa: E402

ITEM_ID = "fixture-aaaaaaaaaaaa"
OTHER_ID = "fixture-bbbbbbbbbbbb"


def seed_item(root: Path, item_id: str, source_id: str = "fixture", year: str = "2026") -> None:
    (root / "data" / "items" / source_id / year / f"{item_id}.json").parent.mkdir(parents=True, exist_ok=True)
    (root / "data" / "items" / source_id / year / f"{item_id}.json").write_text("{}\n", encoding="utf-8")
    (root / "site" / "posts" / source_id / year / f"{item_id}.md").parent.mkdir(parents=True, exist_ok=True)
    (root / "site" / "posts" / source_id / year / f"{item_id}.md").write_text("---\n---\n", encoding="utf-8")
    archive = root / "local-library" / source_id / year / item_id
    archive.mkdir(parents=True, exist_ok=True)
    (archive / "transcript.md").write_text("archive\n", encoding="utf-8")


def test_parse_item_ids_requires_valid_ids() -> None:
    assert purge_items.parse_item_ids([ITEM_ID, ITEM_ID, OTHER_ID]) == [ITEM_ID, OTHER_ID]

    with pytest.raises(ValueError, match="at least one"):
        purge_items.parse_item_ids([])
    with pytest.raises(ValueError, match="invalid item ID"):
        purge_items.parse_item_ids(["not-an-item-id"])


def test_candidate_paths_covers_all_storage_surfaces(tmp_path: Path) -> None:
    seed_item(tmp_path, ITEM_ID)

    paths = {path.relative_to(tmp_path).as_posix() for path in purge_items.candidate_paths(tmp_path, ITEM_ID)}

    assert paths == {
        f"data/items/fixture/2026/{ITEM_ID}.json",
        f"site/posts/fixture/2026/{ITEM_ID}.md",
        f"local-library/fixture/2026/{ITEM_ID}",
    }


def test_dry_run_leaves_files_and_execute_removes_only_selected(tmp_path: Path) -> None:
    seed_item(tmp_path, ITEM_ID)
    seed_item(tmp_path, OTHER_ID, source_id="other")

    exit_code = purge_items.main(["--root", str(tmp_path), "--item-id", ITEM_ID])

    assert exit_code == 0
    assert (tmp_path / "data" / "items" / "fixture" / "2026" / f"{ITEM_ID}.json").exists()
    assert (tmp_path / "local-library" / "fixture" / "2026" / ITEM_ID).is_dir()

    exit_code = purge_items.main(["--root", str(tmp_path), "--execute", "--item-id", ITEM_ID])

    assert exit_code == 0
    assert not (tmp_path / "data" / "items" / "fixture" / "2026" / f"{ITEM_ID}.json").exists()
    assert not (tmp_path / "site" / "posts" / "fixture" / "2026" / f"{ITEM_ID}.md").exists()
    assert not (tmp_path / "local-library" / "fixture" / "2026" / ITEM_ID).exists()
    # Unselected items and their archives stay intact.
    assert (tmp_path / "data" / "items" / "other" / "2026" / f"{OTHER_ID}.json").exists()
    assert (tmp_path / "local-library" / "other" / "2026" / OTHER_ID).is_dir()
