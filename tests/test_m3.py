from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import archive_transcript as archive  # noqa: E402
import check  # noqa: E402
import pending  # noqa: E402

ITEM_ID = "fixture-aaaaaaaaaaaa"
SOURCE_URL = "https://example.com/episodes/fixture"
TRANSCRIPT_URL = "https://example.com/transcripts/fixture.vtt"
AUDIO_URL = "https://cdn.example.com/fixture.mp3"


def item(status: str = "pending", reason: str | None = None, duration: int | None = 3600) -> dict[str, object]:
    return {
        "item_id": ITEM_ID,
        "source_id": "fixture",
        "source_name": "Fixture Podcast",
        "guid": "fixture-guid",
        "title": "A Complete Fixture Episode",
        "url": SOURCE_URL,
        "published_at": "2026-09-10T00:00:00Z",
        "description": "Fixture description",
        "audio_url": AUDIO_URL,
        "transcript_url": TRANSCRIPT_URL,
        "duration_seconds": duration,
        "status": status,
        "reason": reason,
    }


def transcript_payload() -> bytes:
    repeated = "A substantial transcript cue about systems, evidence, limitations, and implementation details. " * 4
    cues = []
    for start in (0, 600, 1200, 1800, 2400, 3000, 3570):
        end = min(start + 30, 3600)
        cues.append(f"{start // 3600:02d}:{start % 3600 // 60:02d}:{start % 60:02d}.000 --> "
                    f"{end // 3600:02d}:{end % 3600 // 60:02d}:{end % 60:02d}.000\n{repeated}")
    return ("WEBVTT\n\n" + "\n\n".join(cues) + "\n").encode()


def asr_payload(duration: float = 3600.0) -> bytes:
    repeated = "A complete ASR segment about recommendation systems, evidence, constraints, and outcomes. " * 4
    starts = [0.0, 600.0, 1200.0, 1800.0, 2400.0, 3000.0, max(0.0, duration - 30.0)]
    segments = [
        {"start": start, "end": min(start + 30.0, duration), "text": repeated}
        for start in starts
        if start < duration
    ]
    return json.dumps({"audio_duration_seconds": duration, "segments": segments}).encode()


def review_args(**overrides: object) -> argparse.Namespace:
    values: dict[str, object] = {
        "identity_confirmed": True,
        "transcript_confirmed": True,
        "complete": True,
        "readable": True,
        "notes": "Identity, completeness, readability, and time coverage reviewed.",
        "timestamp_coverage": "passed",
        "input_type": "official_transcript",
        "source_kind": "rss",
        "batch_id": None,
        "listening_resolved": False,
    }
    values.update(overrides)
    return argparse.Namespace(**values)


def write_item(root: Path, value: dict[str, object]) -> None:
    target = root / "data" / "items" / pending.item_relpath(value)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value), encoding="utf-8")


def write_post(posts_dir: Path, value: dict[str, object], content: str) -> Path:
    target = posts_dir / pending.item_relpath(value).with_suffix(".md")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")
    return target


def article(value: dict[str, object], body_extra: str = "") -> str:
    frontmatter = f"""---
item_id: {value['item_id']}
title: 测试文章
DateIgnored: no
date: '2026-09-11'
published_at: '{str(value['published_at'])[:10]}'
transcribed_at: '2026-09-11'
source_url: {value['url']}
source_name: {value['source_name']}
input_type: official_transcript
tags: [推荐系统, 测试]
---

"""
    body = f"""# 测试文章

> 节目发布：{str(value['published_at'])[:10]} · 逐字稿获取：2026-09-11 · 笔记整理：2026-09-11
> 标签：[推荐系统](/tags/推荐系统/) · [测试](/tags/测试/)
> AI 编辑整理，请以原始节目为准。

## 速读

这是一段有具体内容的测试速读。

## 主题正文

### 一个主题

这是一段有来源约束和适用条件的测试正文。{body_extra}

## 来源与定位

- 原始节目：[A Complete Fixture Episode]({value['url']})
- 定位：
  - 逐字稿小节 “implementation details”
"""
    words = check.article_word_count(body)
    minutes = check.reading_minutes(words)
    return frontmatter + body.replace(
        "> 标签：", f"> 全文 {words} 字 · 预计阅读 {minutes} 分钟\n> 标签：", 1
    )


def valid_article(value: dict[str, object], body_extra: str = "") -> str:
    return article(value, body_extra).replace("DateIgnored: no\n", "")


def reviewed_timing(duration: float = 3600.0) -> archive.TimingCoverage:
    return archive.TimingCoverage(cue_count=7, first_start=0.0, last_end=duration, max_gap=570.0)


def test_archive_requires_explicit_human_readable_review() -> None:
    value = item()
    with pytest.raises(archive.ArchiveError, match="--complete"):
        archive.validate_review(review_args(complete=False), value, reviewed_timing())
    with pytest.raises(archive.ArchiveError, match="untimed transcript"):
        archive.validate_review(review_args(timestamp_coverage="passed"), value, None)


def test_rss_transcript_source_must_match_item_metadata() -> None:
    assert archive.rss_transcript_matches(TRANSCRIPT_URL, TRANSCRIPT_URL)
    assert archive.rss_transcript_matches(
        "https://example.com/transcripts/fixture", TRANSCRIPT_URL
    )
    assert not archive.rss_transcript_matches(
        TRANSCRIPT_URL, "https://example.com/transcripts/other.vtt"
    )
    assert not archive.rss_transcript_matches(
        TRANSCRIPT_URL, "https://attacker.example/transcripts/fixture.vtt"
    )


def test_archive_writes_private_assets_and_is_idempotent(tmp_path: Path) -> None:
    value = item()
    payload = transcript_payload()
    target, created = archive.archive_transcript(
        item=value,
        payload=payload,
        source_format="vtt",
        source_url=TRANSCRIPT_URL,
        input_type="official_transcript",
        source_kind="rss",
        retrieved_at="2026-09-11T12:00:00Z",
        timestamp_coverage="passed",
        listening_resolved=False,
        notes="Reviewed the episode identity and complete one-hour timestamp coverage.",
        library_dir=tmp_path / "local-library",
    )

    assert created
    assert target == tmp_path / "local-library" / "fixture" / ITEM_ID
    assert (target / "transcript.md").read_text(encoding="utf-8").startswith("# A Complete Fixture Episode")
    assert (target / "transcript.vtt").read_bytes() == payload
    metadata = yaml.safe_load((target / "metadata.yaml").read_text(encoding="utf-8"))
    assert metadata["item_id"] == ITEM_ID
    assert metadata["content_checks"]["completeness"] == "passed"
    assert metadata["asset_files"] == ["transcript.md", "transcript.vtt"]

    same_target, second_created = archive.archive_transcript(
        item=value,
        payload=payload,
        source_format="vtt",
        source_url=TRANSCRIPT_URL,
        input_type="official_transcript",
        source_kind="rss",
        retrieved_at="2026-09-11T12:00:00Z",
        timestamp_coverage="passed",
        listening_resolved=False,
        notes="Reviewed the episode identity and complete one-hour timestamp coverage.",
        library_dir=tmp_path / "local-library",
    )
    assert same_target == target
    assert not second_created

    with pytest.raises(archive.ArchiveError, match="different content"):
        archive.archive_transcript(
            item=value,
            payload=payload + b"changed",
            source_format="vtt",
            source_url=TRANSCRIPT_URL,
            input_type="official_transcript",
            source_kind="rss",
            retrieved_at="2026-09-11T12:00:00Z",
            timestamp_coverage="passed",
            listening_resolved=False,
            notes="Reviewed.",
            library_dir=tmp_path / "local-library",
        )


def test_archive_rejects_corrupted_existing_assets(tmp_path: Path) -> None:
    value = item()
    payload = transcript_payload()
    library = tmp_path / "local-library"
    target, _ = archive.archive_transcript(
        item=value,
        payload=payload,
        source_format="vtt",
        source_url=TRANSCRIPT_URL,
        input_type="official_transcript",
        source_kind="rss",
        retrieved_at="2026-09-11T12:00:00Z",
        timestamp_coverage="passed",
        listening_resolved=False,
        notes="Reviewed the episode identity and complete one-hour timestamp coverage.",
        library_dir=library,
    )

    original_transcript = (target / "transcript.md").read_text(encoding="utf-8")
    (target / "transcript.md").write_text("corrupted", encoding="utf-8")
    with pytest.raises(archive.ArchiveError, match="corrupted transcript.md"):
        archive.archive_transcript(
            item=value,
            payload=payload,
            source_format="vtt",
            source_url=TRANSCRIPT_URL,
            input_type="official_transcript",
            source_kind="rss",
            retrieved_at="2026-09-11T12:00:00Z",
            timestamp_coverage="passed",
            listening_resolved=False,
            notes="Reviewed.",
            library_dir=library,
        )

    (target / "transcript.md").write_text(original_transcript, encoding="utf-8")
    (target / "transcript.vtt").unlink()
    with pytest.raises(archive.ArchiveError, match="cannot be validated"):
        archive.archive_transcript(
            item=value,
            payload=payload,
            source_format="vtt",
            source_url=TRANSCRIPT_URL,
            input_type="official_transcript",
            source_kind="rss",
            retrieved_at="2026-09-11T12:00:00Z",
            timestamp_coverage="passed",
            listening_resolved=False,
            notes="Reviewed.",
            library_dir=library,
        )


def test_archive_rejects_missing_content_checks(tmp_path: Path) -> None:
    value = item()
    payload = transcript_payload()
    library = tmp_path / "local-library"
    target, _ = archive.archive_transcript(
        item=value,
        payload=payload,
        source_format="vtt",
        source_url=TRANSCRIPT_URL,
        input_type="official_transcript",
        source_kind="rss",
        retrieved_at="2026-09-11T12:00:00Z",
        timestamp_coverage="passed",
        listening_resolved=False,
        notes="Reviewed.",
        library_dir=library,
    )
    metadata_path = target / "metadata.yaml"
    metadata = yaml.safe_load(metadata_path.read_text(encoding="utf-8"))
    metadata.pop("content_checks")
    metadata_path.write_text(yaml.safe_dump(metadata), encoding="utf-8")

    with pytest.raises(archive.ArchiveError, match="missing content_checks"):
        archive.archive_transcript(
            item=value,
            payload=payload,
            source_format="vtt",
            source_url=TRANSCRIPT_URL,
            input_type="official_transcript",
            source_kind="rss",
            retrieved_at="2026-09-11T12:00:00Z",
            timestamp_coverage="passed",
            listening_resolved=False,
            notes="Reviewed.",
            library_dir=library,
        )


def test_json_transcript_rejects_non_finite_timestamp() -> None:
    payload = b'{"segments":[{"start":Infinity,"end":20,"text":"This is invalid timestamp data with enough transcript text to parse."}]}'
    with pytest.raises(archive.ArchiveError, match="invalid timestamp"):
        archive.convert_transcript(payload, "json")


def test_timed_transcript_rejects_false_coverage_and_bad_ranges() -> None:
    repeated = "A substantial transcript cue with enough readable source material. " * 5
    early = f"WEBVTT\n\n00:00:00.000 --> 00:00:30.000\n{repeated}\n\n00:10:00.000 --> 00:10:30.000\n{repeated}\n".encode()
    with pytest.raises(archive.ArchiveError, match="ends too early"):
        archive.archive_transcript(
            item=item(),
            payload=early,
            source_format="vtt",
            source_url=TRANSCRIPT_URL,
            input_type="official_transcript",
            source_kind="rss",
            retrieved_at="2026-09-11T12:00:00Z",
            timestamp_coverage="passed",
            listening_resolved=False,
            notes="Reviewed.",
            library_dir=Path("unused"),
        )

    sparse = (
        "WEBVTT\n\n"
        f"00:00:00.000 --> 00:00:30.000\n{repeated}\n\n"
        f"00:59:30.000 --> 01:00:00.000\n{repeated}\n"
    ).encode()
    with pytest.raises(archive.ArchiveError, match="internal gap"):
        archive.archive_transcript(
            item=item(),
            payload=sparse,
            source_format="vtt",
            source_url=TRANSCRIPT_URL,
            input_type="official_transcript",
            source_kind="rss",
            retrieved_at="2026-09-11T12:00:00Z",
            timestamp_coverage="passed",
            listening_resolved=False,
            notes="Reviewed.",
            library_dir=Path("unused"),
        )

    reversed_cues = f"WEBVTT\n\n00:10:00.000 --> 00:10:30.000\n{repeated}\n\n00:05:00.000 --> 00:05:30.000\n{repeated}\n".encode()
    with pytest.raises(archive.ArchiveError, match="out-of-order"):
        archive.convert_transcript(reversed_cues, "vtt")

    missing_end = json.dumps({"segments": [{"start": 0, "text": repeated}]}).encode()
    with pytest.raises(archive.ArchiveError, match="both start and end"):
        archive.convert_transcript(missing_end, "json")


def test_asr_requires_known_duration_batch_measured_duration_and_listening_resolution() -> None:
    unknown = item(duration=None)
    with pytest.raises(archive.ArchiveError, match="known episode duration"):
        archive.validate_review(
            review_args(
                input_type="video_agent_kit_asr",
                source_kind="video_agent_kit",
                listening_resolved=True,
                batch_id="batch-1",
            ),
            unknown,
            reviewed_timing(),
            3600.0,
        )

    value = item(duration=3600)
    with pytest.raises(archive.ArchiveError, match="--batch-id"):
        archive.validate_review(
            review_args(
                input_type="video_agent_kit_asr",
                source_kind="video_agent_kit",
                listening_resolved=True,
            ),
            value,
            reviewed_timing(),
            3600.0,
        )
    with pytest.raises(archive.ArchiveError, match="measured audio_duration_seconds"):
        archive.validate_review(
            review_args(
                input_type="video_agent_kit_asr",
                source_kind="video_agent_kit",
                listening_resolved=True,
                batch_id="batch-1",
            ),
            value,
            reviewed_timing(),
        )
    with pytest.raises(archive.ArchiveError, match="duration limit"):
        archive.validate_review(
            review_args(
                input_type="video_agent_kit_asr",
                source_kind="video_agent_kit",
                listening_resolved=True,
                batch_id="batch-1",
            ),
            item(duration=8000),
            archive.TimingCoverage(cue_count=14, first_start=0.0, last_end=8000.0, max_gap=570.0),
            8000.0,
        )
    with pytest.raises(archive.ArchiveError, match="--listening-resolved"):
        archive.validate_review(
            review_args(
                input_type="video_agent_kit_asr",
                source_kind="video_agent_kit",
                batch_id="batch-1",
            ),
            value,
            reviewed_timing(),
            3600.0,
        )


def test_asr_batch_reservation_enforces_one_item_across_calls(tmp_path: Path) -> None:
    value = item(duration=3600)
    library = tmp_path / "local-library"
    record = archive.reserve_asr_batch(
        library, "batch-1", value, 3600.0, "2026-09-11T12:00:00Z"
    )
    assert record.is_file()
    assert archive.reserve_asr_batch(
        library, "batch-1", value, 3600.0, "2026-09-11T12:00:01Z"
    ) == record
    archive.validate_asr_batch_reservation(library, "batch-1", value, 3600.0)
    with pytest.raises(archive.ArchiveError, match="does not match"):
        archive.validate_asr_batch_reservation(library, "batch-1", value, 3000.0)

    with pytest.raises(archive.ArchiveError, match="does not match"):
        archive.reserve_asr_batch(
            tmp_path / "other-library", "batch-2", value, 3000.0, "2026-09-11T12:00:01Z"
        )

    other = item(duration=1800)
    other["item_id"] = "fixture-bbbbbbbbbbbb"
    with pytest.raises(archive.ArchiveError, match="item limit"):
        archive.reserve_asr_batch(
            library, "batch-1", other, 1800.0, "2026-09-11T12:00:02Z"
        )


def test_check_accepts_processed_article_and_demo(tmp_path: Path) -> None:
    value = item(status="processed")
    write_item(tmp_path, value)
    posts = tmp_path / "site" / "posts"
    write_post(posts, value, valid_article(value))

    demo = posts / "demo-vitepress-site.md"
    demo.write_text(
        """---
item_id: demo-vitepress-site
title: 演示文章
date: '2026-09-11'
source_url: https://example.com/demo
source_name: Demo
input_type: demo
---

# 演示文章

## 速读

这是一篇演示文章的速读。

## 主题正文

演示正文内容。

## 来源与定位

- 原始节目：[Demo](https://example.com/demo)
- 定位：演示内容。

AI 编辑整理，请以原始节目为准。
""",
        encoding="utf-8",
    )

    errors, item_count, post_count = check.run_checks(tmp_path, tracked_paths=[])

    assert errors == []
    assert item_count == 1
    assert post_count == 2


def test_check_rejects_status_mismatch_executable_markdown_and_private_assets(tmp_path: Path) -> None:
    value = item(status="pending")
    write_item(tmp_path, value)
    posts = tmp_path / "site" / "posts"
    write_post(
        posts,
        value,
        valid_article(value, " <script>alert(1)</script> [unsafe](javascript:alert(1))"),
    )

    errors, _, _ = check.run_checks(
        tmp_path,
        tracked_paths=[
            "site/posts/fixture/2026/fixture-aaaaaaaaaaaa.md",
            "local-library/fixture/fixture-aaaaaaaaaaaa/transcript.md",
            "notes/wechat-draft.md",
        ],
    )

    assert any("article item status must be processed" in error for error in errors)
    assert any("raw HTML" in error for error in errors)
    assert any("Markdown links and images" in error for error in errors)
    assert sum("must not be tracked or staged" in error for error in errors) == 2


def test_check_requires_reason_for_failed_and_article_for_processed(tmp_path: Path) -> None:
    failed = item(status="failed", reason=None)
    write_item(tmp_path, failed)
    (tmp_path / "site" / "posts").mkdir(parents=True)
    errors, _, _ = check.run_checks(tmp_path, tracked_paths=[])
    assert any("failed item must have a non-empty reason" in error for error in errors)

    processed = copy.deepcopy(failed)
    processed["status"] = "processed"
    processed["reason"] = None
    write_item(tmp_path, processed)
    errors, _, _ = check.run_checks(tmp_path, tracked_paths=[])
    assert any("processed item has no matching article" in error for error in errors)


def test_check_rejects_structure_hidden_in_fenced_code(tmp_path: Path) -> None:
    value = item(status="processed")
    write_item(tmp_path, value)
    posts = tmp_path / "site" / "posts"
    hidden = f"""---
item_id: {ITEM_ID}
title: 测试文章
date: '2026-09-11'
source_url: {SOURCE_URL}
source_name: Fixture Podcast
input_type: official_transcript
---

```markdown
# 测试文章

## 速读
隐藏内容
## 主题正文
隐藏内容
## 来源与定位
- 原始节目：[fixture]({SOURCE_URL})
- 定位：隐藏内容
{check.DISCLAIMER}
```
"""
    write_post(posts, value, hidden)

    errors, _, _ = check.run_checks(tmp_path, tracked_paths=[])

    assert any("body must contain an H1" in error for error in errors)
    assert any("missing required heading" in error for error in errors)

def test_check_rejects_structure_spoofed_by_inline_code(tmp_path: Path) -> None:
    value = item(status="processed")
    write_item(tmp_path, value)
    posts = tmp_path / "site" / "posts"
    spoofed = valid_article(value)
    spoofed = spoofed.replace("## 速读", "This sentence contains `## 速读`")
    spoofed = spoofed.replace("## 主题正文", "This sentence contains ## 主题正文")
    write_post(posts, value, spoofed)

    errors, _, _ = check.run_checks(tmp_path, tracked_paths=[])

    assert any("missing required heading: ## 速读" in error for error in errors)
    assert any("missing required heading: ## 主题正文" in error for error in errors)


def test_check_requires_exact_source_link(tmp_path: Path) -> None:
    value = item(status="processed")
    write_item(tmp_path, value)
    posts = tmp_path / "site" / "posts"
    wrong = valid_article(value).replace(f"]({SOURCE_URL})", f"]({SOURCE_URL}-attacker)")
    write_post(posts, value, wrong)

    errors, _, _ = check.run_checks(tmp_path, tracked_paths=[])

    assert any("exact source_url link" in error for error in errors)


def test_check_rejects_case_variant_private_paths() -> None:
    assert check.is_disallowed_repository_path("Local-Library/source/transcript.md")
    assert check.is_disallowed_repository_path(".Cache/source/audio.mp3")
    assert check.is_disallowed_repository_path("NOTES/WECHAT-DRAFT.MD")
    assert check.is_disallowed_repository_path("backup/Local-Library/private.txt")
    assert check.is_disallowed_repository_path("snapshots/.Cache/private.bin")


def test_check_rejects_unexpected_files_in_public_data_directories(tmp_path: Path) -> None:
    value = item()
    write_item(tmp_path, value)
    posts = tmp_path / "site" / "posts"
    posts.mkdir(parents=True)
    (tmp_path / "data" / "items" / "transcript.md").write_text("private", encoding="utf-8")
    (posts / "audio.mp3").write_bytes(b"private")

    errors, _, _ = check.run_checks(tmp_path, tracked_paths=[])

    assert any("data/items item files must use" in error for error in errors)
    assert any("site/posts articles must use" in error for error in errors)


def test_check_rejects_misplaced_public_content(tmp_path: Path) -> None:
    value = item()
    write_item(tmp_path, value)
    items_dir = tmp_path / "data" / "items"
    posts = tmp_path / "site" / "posts"
    posts.mkdir(parents=True)
    (items_dir / "flat.json").write_text("{}", encoding="utf-8")
    deep = items_dir / "fixture" / "2026" / "extra"
    deep.mkdir(parents=True)
    (deep / "deep.json").write_text("{}", encoding="utf-8")
    (posts / "stray.md").write_text("# unchecked", encoding="utf-8")
    notes = posts / "fixture" / "2026" / "notes.txt"
    notes.parent.mkdir(parents=True)
    notes.write_text("x", encoding="utf-8")

    errors, _, _ = check.run_checks(tmp_path, tracked_paths=[])

    assert any("flat.json" in error and "data/items item files must use" in error for error in errors)
    assert any("deep.json" in error and "data/items item files must use" in error for error in errors)
    assert any("stray.md" in error and "site/posts articles must use" in error for error in errors)
    assert any("notes.txt" in error and "site/posts articles must use" in error for error in errors)


def test_check_accepts_generated_source_index_pages(tmp_path: Path) -> None:
    value = item(status="processed")
    write_item(tmp_path, value)
    posts = tmp_path / "site" / "posts"
    write_post(posts, value, valid_article(value))
    index_page = posts / "fixture" / "index.md"
    index_page.parent.mkdir(parents=True, exist_ok=True)
    index_page.write_text("---\nlayout: doc\ntitle: Fixture Podcast\n---\n\n# Fixture Podcast\n", encoding="utf-8")

    errors, item_count, post_count = check.run_checks(tmp_path, tracked_paths=[])

    assert errors == []
    assert item_count == 1
    assert post_count == 1


def test_check_requires_meta_blockquote_with_accurate_word_count(tmp_path: Path) -> None:
    value = item(status="processed")
    write_item(tmp_path, value)
    posts = tmp_path / "site" / "posts"

    stripped = re.sub(r"> (节目发布|全文)[^\n]*\n", "", valid_article(value))
    write_post(posts, value, stripped)
    errors, _, _ = check.run_checks(tmp_path, tracked_paths=[])
    assert any("missing article meta blockquote" in error for error in errors)

    write_post(posts, value, re.sub(r"全文 \d+ 字", "全文 1 字", valid_article(value)))
    errors, _, _ = check.run_checks(tmp_path, tracked_paths=[])
    assert any("computed count is" in error for error in errors)

    write_post(posts, value, re.sub(r"预计阅读 \d+ 分钟", "预计阅读 99 分钟", valid_article(value)))
    errors, _, _ = check.run_checks(tmp_path, tracked_paths=[])
    assert any("预计阅读 must be" in error for error in errors)

    write_post(posts, value, valid_article(value))
    errors, _, _ = check.run_checks(tmp_path, tracked_paths=[])
    assert not any("meta blockquote" in error for error in errors)


def test_check_requires_tag_line_matching_frontmatter(tmp_path: Path) -> None:
    value = item(status="processed")
    write_item(tmp_path, value)
    posts = tmp_path / "site" / "posts"

    write_post(posts, value, re.sub(r"> 标签：[^\n]*\n", "", valid_article(value)))
    errors, _, _ = check.run_checks(tmp_path, tracked_paths=[])
    assert any("must include a 标签 line" in error for error in errors)

    write_post(posts, value, valid_article(value).replace("](/tags/测试/)", "](/tags/wrong/)"))
    errors, _, _ = check.run_checks(tmp_path, tracked_paths=[])
    assert any("must list exactly the frontmatter tags" in error for error in errors)


def test_check_requires_item_publish_date_match(tmp_path: Path) -> None:
    value = item(status="processed")
    write_item(tmp_path, value)
    posts = tmp_path / "site" / "posts"
    digest_date = str(value["published_at"])[:10]
    mismatched = (
        valid_article(value)
        .replace(f"published_at: '{digest_date}'", "published_at: '2020-01-01'")
        .replace(f"节目发布：{digest_date}", "节目发布：2020-01-01")
    )
    write_post(posts, value, mismatched)

    errors, _, _ = check.run_checks(tmp_path, tracked_paths=[])

    assert any("published_at must match the item publish date" in error for error in errors)

    missing_transcribed = re.sub(r"transcribed_at: '[^']*'\n", "", valid_article(value))
    write_post(posts, value, missing_transcribed)
    errors, _, _ = check.run_checks(tmp_path, tracked_paths=[])
    assert any("must declare transcribed_at" in error for error in errors)


def test_check_requires_article_path_to_match_item_shards(tmp_path: Path) -> None:
    value = item(status="processed")
    write_item(tmp_path, value)
    posts = tmp_path / "site" / "posts"
    target = posts / "fixture" / "2025" / f"{ITEM_ID}.md"
    target.parent.mkdir(parents=True)
    target.write_text(valid_article(value), encoding="utf-8")

    errors, _, _ = check.run_checks(tmp_path, tracked_paths=[])

    assert any("must be stored as" in error for error in errors)


def test_check_rejects_unknown_frontmatter_and_missing_real_locator(tmp_path: Path) -> None:
    value = item(status="processed")
    write_item(tmp_path, value)
    posts = tmp_path / "site" / "posts"
    invalid = article(value).replace("  - 逐字稿小节 “implementation details”", "  - 不适用")
    write_post(posts, value, invalid)

    errors, _, _ = check.run_checks(tmp_path, tracked_paths=[])

    assert any("unexpected frontmatter fields" in error for error in errors)
    assert any("real source locator" in error for error in errors)
