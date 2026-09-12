from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
sys.path.insert(0, str(SCRIPTS))

import collect  # noqa: E402
import pending  # noqa: E402

NOW = datetime(2026, 9, 11, 0, 0, tzinfo=timezone.utc)


def write_config(path: Path, sources: list[dict[str, object]]) -> None:
    lines = ["sources:"]
    for source in sources:
        lines.extend(
            [
                f"  - id: {source['id']}",
                f"    name: {source['name']}",
                f"    url: {source['url']}",
                "    enabled: true",
                "    include_keywords:",
            ]
        )
        includes = source.get("include_keywords", [])
        if includes:
            lines.extend(f"      - {keyword}" for keyword in includes)
        else:
            lines[-1] += " []"
        lines.append("    exclude_keywords:")
        excludes = source.get("exclude_keywords", [])
        if excludes:
            lines.extend(f"      - {keyword}" for keyword in excludes)
        else:
            lines[-1] += " []"
        minimum = source.get("min_duration_minutes")
        lines.append(f"    min_duration_minutes: {minimum if minimum is not None else 'null'}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def fixture_fetcher(mapping: dict[str, str], failures: set[str] | None = None):
    failures = failures or set()

    def fetch(url: str, timeout: float, retries: int) -> bytes:
        assert timeout > 0
        assert retries >= 0
        if url in failures:
            raise collect.CollectorError("fixture failure")
        return (FIXTURES / mapping[url]).read_bytes()

    return fetch


def load_output(output_dir: Path) -> list[dict[str, object]]:
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(
            output_dir.rglob("*.json"), key=lambda candidate: candidate.relative_to(output_dir).as_posix()
        )
    ]


def valid_item(item_id: str, published_at: str | None, status: str = "pending") -> dict[str, object]:
    source_id = item_id.rsplit("-", 1)[0]
    return {
        "item_id": item_id,
        "source_id": source_id,
        "source_name": source_id.title(),
        "guid": f"guid-{item_id}",
        "title": f"Title {item_id}",
        "url": f"https://example.com/{item_id}",
        "published_at": published_at,
        "description": "Description",
        "audio_url": None,
        "transcript_url": None,
        "duration_seconds": None,
        "status": status,
        "reason": None,
    }


def test_stable_id_uses_guid_then_page_url_and_never_title_or_audio() -> None:
    guid_expected = hashlib.sha256(b"fixture:guid-1").hexdigest()[:12]
    page_expected = hashlib.sha256(b"fixture:https://example.com/episode").hexdigest()[:12]

    assert collect.stable_item_id("fixture", "guid-1", "https://example.com/episode") == f"fixture-{guid_expected}"
    assert collect.stable_item_id("fixture", None, "https://example.com/episode") == f"fixture-{page_expected}"
    assert collect.stable_item_id("fixture", None, None) is None

    source = collect.Source("fixture", "Fixture", "https://example.com/feed", True, (), (), None)
    item, reason = collect.build_item(
        {
            "title": "Same title",
            "enclosures": [{"href": "https://cdn.example.com/audio.mp3", "type": "audio/mpeg"}],
        },
        source,
    )
    assert item is None
    assert reason == "missing GUID and page URL"


def test_date_filter_keywords_duration_cleaning_and_optional_links(tmp_path: Path) -> None:
    config = tmp_path / "sources.yaml"
    output = tmp_path / "items"
    url = "https://example.com/collector.xml"
    write_config(
        config,
        [
            {
                "id": "fixture",
                "name": "Fixture",
                "url": url,
                "include_keywords": ["ai", "world"],
                "exclude_keywords": ["sponsor"],
                "min_duration_minutes": 1,
            }
        ],
    )

    exit_code, summaries, text = collect.collect(
        config,
        output,
        NOW,
        fetcher=fixture_fetcher({url: "collector.xml"}),
    )

    assert exit_code == 0
    assert summaries[0].entries == 8
    assert summaries[0].new == 4
    assert summaries[0].filtered == 3
    assert summaries[0].skipped == 1
    assert "Current pending items: 4" in text

    items = {item["guid"]: item for item in load_output(output)}
    assert set(items) == {"guid-fresh", "guid-updated", "guid-unknown-duration", None}
    assert (output / "fixture" / "2026").is_dir()
    assert {path.parent.name for path in output.rglob("*.json")} == {"2026"}
    assert items["guid-fresh"]["published_at"] == "2026-09-10T00:00:00Z"
    assert items["guid-updated"]["published_at"] == "2026-09-10T16:00:00Z"
    assert items["guid-fresh"]["duration_seconds"] == 3723
    assert items["guid-updated"]["duration_seconds"] == 2730
    assert items["guid-unknown-duration"]["duration_seconds"] is None
    assert items["guid-fresh"]["description"] == "Hello WORLD."
    assert items["guid-fresh"]["audio_url"] == "https://cdn.example.com/fresh.mp3"
    assert items["guid-fresh"]["transcript_url"] == "https://example.com/transcripts/fresh.vtt"

    fallback = items[None]
    expected = hashlib.sha256(b"fixture:https://example.com/episodes/fallback").hexdigest()[:12]
    assert fallback["item_id"] == f"fixture-{expected}"


def test_plain_html_episode_link_is_not_inferred_as_transcript() -> None:
    entry = {
        "links": [
            {"rel": "alternate", "type": "text/html", "href": "https://example.com/episode"},
        ]
    }

    assert collect.entry_transcript_url(entry) is None


def test_keywords_match_whole_words_with_plural_not_substrings() -> None:
    source = collect.Source(
        "fixture",
        "Fixture",
        "https://example.com/feed",
        True,
        ("AI", "agent", "database"),
        ("sponsor",),
        None,
    )

    assert collect.matches_keywords("Talking about AI agents", source)
    assert collect.matches_keywords("AI-native databases in production", source)
    assert collect.matches_keywords("HTTP user-agent headers", source)
    assert not collect.matches_keywords("email deliverability", source)
    assert not collect.matches_keywords("available training details", source)
    assert not collect.matches_keywords("OpenAI and Gemini news", source)
    assert not collect.matches_keywords("sponsored by nobody", source)


def test_lookback_days_extends_intake_window(tmp_path: Path) -> None:
    config = tmp_path / "sources.yaml"
    output = tmp_path / "items"
    url = "https://example.com/collector.xml"
    write_config(config, [{"id": "fixture", "name": "Fixture", "url": url}])
    fetcher = fixture_fetcher({url: "collector.xml"})

    exit_code, summaries, _ = collect.collect(
        config,
        output,
        NOW,
        lookback_days=120,
        fetcher=fetcher,
    )

    assert exit_code == 0
    assert summaries[0].status == "success"
    assert "guid-old" in {item["guid"] for item in load_output(output)}

    with pytest.raises(collect.CollectorError):
        collect.collect(config, tmp_path / "items2", NOW, lookback_days=0, fetcher=fetcher)


def test_unknown_dates_are_limited_to_three_new_per_run(tmp_path: Path) -> None:
    config = tmp_path / "sources.yaml"
    output = tmp_path / "items"
    url = "https://example.com/unknown.xml"
    write_config(config, [{"id": "unknown", "name": "Unknown", "url": url}])

    exit_code, summaries, _ = collect.collect(
        config,
        output,
        NOW,
        fetcher=fixture_fetcher({url: "unknown_dates.xml"}),
    )

    assert exit_code == 0
    assert summaries[0].new == 3
    assert summaries[0].filtered == 2
    items = load_output(output)
    assert {item["guid"] for item in items} == {"unknown-1", "unknown-2", "unknown-3"}
    assert all(item["published_at"] is None for item in items)
    assert {path.parent.name for path in output.rglob("*.json")} == {pending.UNKNOWN_YEAR}


def test_unknown_dates_admit_only_new_writes_across_runs(tmp_path: Path) -> None:
    config = tmp_path / "sources.yaml"
    output = tmp_path / "items"
    url = "https://example.com/unknown.xml"
    write_config(config, [{"id": "unknown", "name": "Unknown", "url": url}])
    fetcher = fixture_fetcher({url: "unknown_dates.xml"})

    collect.collect(config, output, NOW, fetcher=fetcher)
    exit_code, summaries, _ = collect.collect(config, output, NOW, fetcher=fetcher)

    assert exit_code == 0
    assert summaries[0].new == 2
    assert summaries[0].existing == 3
    assert summaries[0].filtered == 0
    assert {item["guid"] for item in load_output(output)} == {
        "unknown-1",
        "unknown-2",
        "unknown-3",
        "unknown-4",
        "unknown-5",
    }


def test_description_is_plain_text_and_truncated(tmp_path: Path) -> None:
    config = tmp_path / "sources.yaml"
    output = tmp_path / "items"
    url = "https://example.com/long.xml"
    write_config(config, [{"id": "long", "name": "Long", "url": url}])

    collect.collect(config, output, NOW, fetcher=fixture_fetcher({url: "long_description.xml"}))
    description = load_output(output)[0]["description"]

    assert len(description) == 1000
    assert "<" not in description
    assert "do-not-keep" not in description
    assert description.startswith("Start with HTML.")


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("3600", 3600),
        ("45:30", 2730),
        ("01:02:03", 3723),
        (62.9, 62),
        ("01:99", None),
        ("unknown", None),
        (None, None),
    ],
)
def test_duration_formats(value: object, expected: int | None) -> None:
    assert collect.parse_duration(value) == expected


def test_existing_item_is_preserved_byte_for_byte(tmp_path: Path) -> None:
    config = tmp_path / "sources.yaml"
    output = tmp_path / "items"
    url = "https://example.com/isolation.xml"
    write_config(config, [{"id": "healthy", "name": "Healthy", "url": url}])
    fetcher = fixture_fetcher({url: "isolation.xml"})

    collect.collect(config, output, NOW, fetcher=fetcher)
    item_path = next(iter(sorted(output.rglob("*.json"))))
    edited = json.loads(item_path.read_text(encoding="utf-8"))
    edited["status"] = "ignored"
    edited["reason"] = "manual decision"
    original_bytes = (json.dumps(edited, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    item_path.write_bytes(original_bytes)

    exit_code, summaries, _ = collect.collect(config, output, NOW, fetcher=fetcher)

    assert exit_code == 0
    assert summaries[0].new == 0
    assert summaries[0].existing == 1
    assert item_path.read_bytes() == original_bytes


def test_valid_empty_feed_is_a_success(tmp_path: Path) -> None:
    config = tmp_path / "sources.yaml"
    output = tmp_path / "items"
    url = "https://example.com/empty.xml"
    write_config(config, [{"id": "empty", "name": "Empty", "url": url}])

    exit_code, summaries, text = collect.collect(
        config,
        output,
        NOW,
        fetcher=lambda _url, _timeout, _retries: b"<?xml version='1.0'?><rss version='2.0'><channel><title>Empty</title></channel></rss>",
    )

    assert exit_code == 0
    assert summaries[0].status == "success"
    assert summaries[0].entries == 0
    assert "1 succeeded, 0 failed" in text


def test_source_failures_are_isolated_and_all_fail_is_nonzero(tmp_path: Path) -> None:
    config = tmp_path / "sources.yaml"
    output = tmp_path / "items"
    good_url = "https://example.com/good.xml"
    bad_url = "https://example.com/bad.xml"
    write_config(
        config,
        [
            {"id": "good", "name": "Good", "url": good_url},
            {"id": "bad", "name": "Bad", "url": bad_url},
        ],
    )
    fetcher = fixture_fetcher({good_url: "isolation.xml"}, {bad_url})

    exit_code, summaries, text = collect.collect(config, output, NOW, fetcher=fetcher)

    assert exit_code == 0
    assert [summary.status for summary in summaries] == ["success", "error"]
    assert len(load_output(output)) == 1
    assert "1 succeeded, 1 failed" in text
    assert "fixture failure" in text

    all_bad_config = tmp_path / "all-bad.yaml"
    write_config(all_bad_config, [{"id": "bad", "name": "Bad", "url": bad_url}])
    exit_code, summaries, _ = collect.collect(all_bad_config, tmp_path / "empty", NOW, fetcher=fetcher)
    assert exit_code == 1
    assert summaries[0].status == "error"


def test_pending_orders_valid_items_and_limit_is_candidate_window(tmp_path: Path) -> None:
    items_dir = tmp_path / "items"
    items_dir.mkdir()
    items = [
        valid_item("alpha-aaaaaaaaaaaa", "2026-09-09T00:00:00Z"),
        valid_item("beta-bbbbbbbbbbbb", None),
        valid_item("gamma-cccccccccccc", "2026-09-11T00:00:00Z"),
        valid_item("delta-dddddddddddd", "2026-09-10T00:00:00Z", status="processed"),
    ]
    for item in items:
        target = items_dir / pending.item_relpath(item)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(item), encoding="utf-8")

    valid, errors = pending.load_items(items_dir)
    ordered = pending.pending_items(valid)

    assert not errors
    assert [item["item_id"] for item in ordered] == [
        "gamma-cccccccccccc",
        "alpha-aaaaaaaaaaaa",
        "beta-bbbbbbbbbbbb",
    ]
    text = pending.render(valid, errors, limit=2)
    assert "Pending items: 3" in text
    assert "Candidate window: 2 (--limit 2; not a processing quota)" in text
    assert "beta-bbbbbbbbbbbb" not in text


def test_pending_cli_reports_malformed_json_nonzero(tmp_path: Path) -> None:
    items_dir = tmp_path / "items"
    items_dir.mkdir()
    good = valid_item("good-eeeeeeeeeeee", "2026-09-11T00:00:00Z")
    good_path = items_dir / pending.item_relpath(good)
    good_path.parent.mkdir(parents=True, exist_ok=True)
    good_path.write_text(json.dumps(good), encoding="utf-8")
    (items_dir / "broken.json").write_text('{"item_id":', encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "pending.py"), "--items-dir", str(items_dir), "--limit", "10"],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 1
    assert "Malformed item files: 1" in result.stderr
    assert "Validation errors:" in result.stderr
    assert "invalid JSON" in result.stderr
