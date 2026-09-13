#!/usr/bin/env python3
"""Run deterministic metadata, article, and repository safety checks."""

from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence
from urllib.parse import unquote

import yaml

import pending

ALLOWED_FRONTMATTER_FIELDS = {
    "item_id",
    "layout",
    "title",
    "date",
    "published_at",
    "transcribed_at",
    "model",
    "source_url",
    "source_name",
    "input_type",
    "tags",
    "summary",
    "transcript_url",
    "prev",
    "next",
}
REQUIRED_FRONTMATTER_FIELDS = {
    "item_id",
    "title",
    "date",
    "source_url",
    "source_name",
    "input_type",
    "summary",
}
INPUT_TYPES = {"official_transcript", "video_agent_kit_asr", "demo"}
DEMO_ITEM_ID = "demo-vitepress-site"
DISCLAIMER = "AI 编辑整理，请以原始节目为准。"
REQUIRED_HEADINGS = ("## 速读", "## 主题正文", "## 来源与定位", "## 整理说明")
PLACEHOLDER_PATTERN = re.compile(r"<(?:stable-item-id|中文文章标题|Podcast 名称|标题|重点主题|时间段或可识别原文小节)>")
HTML_TAG_PATTERN = re.compile(r"<(?!https?://)[A-Za-z!/][^>]*>", re.IGNORECASE)
VUE_TEMPLATE_PATTERN = re.compile(r"{{|}}|(?:^|\s)(?:v-[a-z-]+|@[a-z-]+|:[a-z-]+)=", re.IGNORECASE | re.MULTILINE)
DISALLOWED_TOP_LEVEL = {"local-library", ".cache"}
DISALLOWED_NAMES = {
    "editorial-notes.md",
    "machine-summary.md",
    "transcript.json",
    "transcript.md",
    "video-script.md",
    "wechat-draft.md",
}
DISALLOWED_SUFFIXES = {".mp3", ".mp4", ".wav", ".m4a", ".vtt", ".srt"}
MARKDOWN_LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+['\"][^'\"]*['\"])?\)")
MARKDOWN_LINK_TEXT_PATTERN = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
META_DATES_PATTERN = re.compile(
    r"^> 节目发布：(\d{4}-\d{2}-\d{2}) · 逐字稿获取：(\d{4}-\d{2}-\d{2}) · 笔记整理：(\d{4}-\d{2}-\d{2})$"
)
META_COUNTS_PATTERN = re.compile(r"^> 全文共 (\d+) 字 · 阅读约 (\d+) 分钟$")
META_TAGS_PREFIX = "> 标签："
META_TAGS_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\((/tags/[^)]+/)\)")
META_SHOW_PATTERN = re.compile(r"^> 节目：\[([^\]]+)\]\((/podcasts/[^)]+/)\)$")
META_SOURCE_PATTERN = re.compile(
    r"^> 🎧 \[收听原节目\]\(([^)]+)\)(?: · 📄 \[查看官方逐字稿\]\(([^)]+)\))?$"
)
META_MODEL_PATTERN = re.compile(r"^- 整理模型：.+$")
META_NOTE_PATTERN = re.compile(rf"^- {re.escape(DISCLAIMER)}$")
LOCATOR_ITEM_PATTERN = re.compile(r"^\s{2,}-\s+(.+)$")
NON_LOCATORS = {"不适用", "无", "N/A", "n/a"}
READING_SPEED_CHARS_PER_MINUTE = 400


@dataclass(frozen=True)
class Post:
    path: Path
    frontmatter: Mapping[str, Any]
    body: str


class CheckError(Exception):
    """Raised when a file cannot be parsed for deterministic validation."""


def relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def parse_post(path: Path) -> Post:
    try:
        source = path.read_text(encoding="utf-8")
    except OSError as error:
        raise CheckError(f"cannot read: {error}") from error
    except UnicodeError as error:
        raise CheckError(f"invalid UTF-8: {error}") from error

    match = re.match(r"\A---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)\Z", source)
    if not match:
        raise CheckError("must start with YAML frontmatter")
    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as error:
        raise CheckError(f"invalid YAML frontmatter: {error}") from error
    if not isinstance(frontmatter, Mapping):
        raise CheckError("frontmatter must be a mapping")
    return Post(path=path, frontmatter=dict(frontmatter), body=match.group(2))


def validate_frontmatter(post: Post, root: Path) -> list[str]:
    fields = post.frontmatter
    location = relative(post.path, root)
    errors: list[str] = []
    missing = sorted(REQUIRED_FRONTMATTER_FIELDS - set(fields))
    unexpected = sorted(set(fields) - ALLOWED_FRONTMATTER_FIELDS)
    if missing:
        errors.append(f"{location}: missing frontmatter fields: {', '.join(missing)}")
    if unexpected:
        errors.append(f"{location}: unexpected frontmatter fields: {', '.join(unexpected)}")

    for key in ("item_id", "title", "source_url", "source_name", "input_type"):
        if not isinstance(fields.get(key), str) or not fields[key].strip():
            errors.append(f"{location}: {key} must be a non-empty string")

    item_id = fields.get("item_id")
    if isinstance(item_id, str):
        if post.path.stem != item_id:
            errors.append(f"{location}: filename must equal item_id + .md")
        if item_id != DEMO_ITEM_ID and not pending.ITEM_ID_PATTERN.fullmatch(item_id):
            errors.append(f"{location}: item_id must be a collected item identifier")

    input_type = fields.get("input_type")
    if input_type not in INPUT_TYPES:
        errors.append(f"{location}: input_type must be one of: {', '.join(sorted(INPUT_TYPES))}")
    if input_type == "demo" and item_id != DEMO_ITEM_ID:
        errors.append(f"{location}: only {DEMO_ITEM_ID} may use input_type demo")
    if item_id == DEMO_ITEM_ID and input_type != "demo":
        errors.append(f"{location}: {DEMO_ITEM_ID} must use input_type demo")

    article_date = fields.get("date")
    if not isinstance(article_date, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", article_date):
        errors.append(f"{location}: date must be a quoted YYYY-MM-DD string")
    else:
        try:
            date.fromisoformat(article_date)
        except ValueError:
            errors.append(f"{location}: date is not a valid calendar date")

    for field in ("published_at", "transcribed_at"):
        value = fields.get(field)
        if value is None:
            continue
        if not isinstance(value, str) or not DATE_PATTERN.fullmatch(value):
            errors.append(f"{location}: {field} must be a YYYY-MM-DD string")
            continue
        try:
            date.fromisoformat(value)
        except ValueError:
            errors.append(f"{location}: {field} is not a valid calendar date")
    if item_id != DEMO_ITEM_ID and fields.get("transcribed_at") is None:
        errors.append(f"{location}: non-demo article must declare transcribed_at")
    if item_id != DEMO_ITEM_ID:
        model = fields.get("model")
        if not isinstance(model, str) or not model.strip():
            errors.append(f"{location}: non-demo article must declare model")

    if not pending.is_public_http_url(fields.get("source_url")):
        errors.append(f"{location}: source_url must be a public http(s) URL")

    summary = fields.get("summary")
    if not isinstance(summary, str) or not summary.strip():
        errors.append(f"{location}: summary must be a non-empty string")
    elif len(summary.strip()) > 180:
        errors.append(f"{location}: summary must be at most 180 characters")

    transcript_url = fields.get("transcript_url")
    if transcript_url is not None and not pending.is_public_http_url(transcript_url):
        errors.append(f"{location}: transcript_url must be null or a public http(s) URL")

    tags = fields.get("tags")
    if tags is not None and (
        not isinstance(tags, list)
        or any(not isinstance(tag, str) or not tag.strip() for tag in tags)
    ):
        errors.append(f"{location}: tags must be a list of non-empty strings")
    if fields.get("prev") not in (None, False) or fields.get("next") not in (None, False):
        errors.append(f"{location}: prev and next must be false when declared")
    layout = fields.get("layout")
    if layout is not None and layout != "doc":
        errors.append(f"{location}: layout may only be doc")
    return errors


def strip_fenced_code(body: str) -> str:
    lines = body.splitlines()
    output: list[str] = []
    fence_char: str | None = None
    fence_length = 0
    for line in lines:
        stripped = line.lstrip()
        fence_match = re.match(r"(`{3,}|~{3,})", stripped)
        if fence_match:
            marker = fence_match.group(1)
            if fence_char is None:
                fence_char = marker[0]
                fence_length = len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_length:
                fence_char = None
                fence_length = 0
            continue
        if fence_char is None:
            output.append(line)
    return "\n".join(output)


def markdown_link_targets(body: str) -> list[str]:
    return MARKDOWN_LINK_PATTERN.findall(strip_fenced_code(body))


def heading_match(body: str, heading: str) -> re.Match[str] | None:
    return re.search(rf"^{re.escape(heading)}[ \t]*$", body, re.MULTILINE)


def _strip_hard_break(line: str) -> str:
    stripped = line.strip()
    return stripped[:-1].rstrip() if stripped.endswith("\\") else stripped


def article_meta_block(body: str) -> tuple[re.Match[str] | None, re.Match[str] | None, str | None]:
    dates = counts = tags_line = None
    for line in strip_fenced_code(body).splitlines():
        stripped = _strip_hard_break(line)
        if dates is None and META_DATES_PATTERN.fullmatch(stripped):
            dates = META_DATES_PATTERN.fullmatch(stripped)
        elif counts is None and META_COUNTS_PATTERN.fullmatch(stripped):
            counts = META_COUNTS_PATTERN.fullmatch(stripped)
        elif tags_line is None and stripped.startswith(META_TAGS_PREFIX):
            tags_line = stripped
    return dates, counts, tags_line


def article_word_count(body: str) -> int:
    excluded = (
        META_DATES_PATTERN,
        META_COUNTS_PATTERN,
        re.compile(r"^>\s*$"),
        META_SHOW_PATTERN,
        META_SOURCE_PATTERN,
        META_MODEL_PATTERN,
        META_NOTE_PATTERN,
    )
    tags_prefix = re.compile(r"^>\s*标签：")
    lines = [
        line
        for line in body.splitlines()
        if not tags_prefix.match(_strip_hard_break(line))
        and not any(pattern.fullmatch(_strip_hard_break(line)) for pattern in excluded)
    ]
    text = MARKDOWN_LINK_TEXT_PATTERN.sub(r"\1", "\n".join(lines))
    return sum(1 for char in text if not char.isspace())


def reading_minutes(words: int) -> int:
    return max(1, math.ceil(words / READING_SPEED_CHARS_PER_MINUTE))


def section_text(body: str, heading: str) -> str:
    body = strip_fenced_code(body)
    match = heading_match(body, heading)
    if match is None:
        return ""
    start = match.end()
    next_heading = re.search(r"^##[ \t]+[^#\r\n].*$", body[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(body)
    return body[start:end].strip()


def validate_body(post: Post, root: Path) -> list[str]:
    body = strip_fenced_code(post.body)
    fields = post.frontmatter
    location = relative(post.path, root)
    errors: list[str] = []
    title = fields.get("title")
    if isinstance(title, str) and not re.search(rf"^#\s+{re.escape(title.strip())}\s*$", body, re.MULTILINE):
        errors.append(f"{location}: body must contain an H1 matching title")

    positions = [match.start() if (match := heading_match(body, heading)) else -1 for heading in REQUIRED_HEADINGS]
    for heading, position in zip(REQUIRED_HEADINGS, positions):
        if position < 0:
            errors.append(f"{location}: missing required heading: {heading}")
        elif not section_text(body, heading):
            errors.append(f"{location}: section is empty: {heading}")
    if all(position >= 0 for position in positions) and positions != sorted(positions):
        errors.append(f"{location}: required sections must use 速读 → 主题正文 → 来源与定位 order")

    explanation = section_text(body, "## 整理说明")
    if DISCLAIMER not in explanation:
        errors.append(f"{location}: missing AI editing disclaimer")
    if PLACEHOLDER_PATTERN.search(body):
        errors.append(f"{location}: contains an unresolved article template placeholder")
    if HTML_TAG_PATTERN.search(body):
        errors.append(f"{location}: raw HTML or component tags are not allowed")
    if VUE_TEMPLATE_PATTERN.search(body):
        errors.append(f"{location}: executable Vue template syntax is not allowed")
    for raw_target in markdown_link_targets(body):
        target = raw_target.strip("<>")
        if target.startswith("#") or re.match(r"^/(posts|tags|podcasts)/", target):
            continue
        if not pending.is_public_http_url(target):
            errors.append(f"{location}: Markdown links and images must use public http(s) URLs")
            break

    source_url = fields.get("source_url")
    input_type = fields.get("input_type")
    source_section = section_text(body, "## 来源与定位")
    if input_type != "demo":
        source_targets = [target.strip("<>") for target in markdown_link_targets(source_section)]
        if not isinstance(source_url, str) or source_url not in source_targets:
            errors.append(f"{location}: 来源与定位 must contain an exact source_url link")
        locator_match = re.search(r"^-\s*定位[：:][ \t]*(.*)$", source_section, re.MULTILINE)
        locator_items: list[str] = []
        if locator_match:
            for line in source_section[locator_match.end() :].splitlines():
                item = LOCATOR_ITEM_PATTERN.fullmatch(line.rstrip())
                if item:
                    locator_items.append(item.group(1).strip())
                elif line.strip() and not locator_items:
                    continue
                elif line.strip():
                    break
        if not locator_items or any(item in NON_LOCATORS for item in locator_items):
            errors.append(
                f"{location}: 来源与定位 must contain a real source locator list under 定位 (one timestamp or phrase per line)"
            )

        dates, counts, tags_line = article_meta_block(body)
        if dates is None or counts is None:
            errors.append(
                f"{location}: missing article meta blockquote (节目发布/逐字稿获取/笔记整理 and 全文共/阅读约 line)"
            )
        else:
            if (
                dates.group(1) != fields.get("published_at")
                or dates.group(2) != fields.get("transcribed_at")
                or dates.group(3) != fields.get("date")
            ):
                errors.append(f"{location}: meta blockquote dates must equal frontmatter published_at/transcribed_at/date")
            computed_words = article_word_count(post.body)
            expected_minutes = reading_minutes(computed_words)
            if int(counts.group(1)) != computed_words:
                errors.append(
                    f"{location}: meta blockquote 全文共 must be {computed_words} 字"
                )
            if int(counts.group(2)) != expected_minutes:
                errors.append(
                    f"{location}: meta blockquote 阅读约 must be {expected_minutes} 分钟 "
                    f"({READING_SPEED_CHARS_PER_MINUTE} characters per minute)"
                )
            stripped_body = strip_fenced_code(body)
            meta_index = stripped_body.find(dates.group(0))
            first_section = re.search(r"^##[ \t]+", stripped_body, re.MULTILINE)
            if first_section and (meta_index == -1 or meta_index > first_section.start()):
                errors.append(f"{location}: meta blockquote must sit directly under the H1 title, before the first section")

        show_lines = [
            META_SHOW_PATTERN.fullmatch(_strip_hard_break(line))
            for line in strip_fenced_code(body).splitlines()
        ]
        if not any(match and match.group(1) == fields.get("source_name") for match in show_lines):
            errors.append(f"{location}: meta blockquote must identify the source show")

        source_matches = [
            match
            for line in strip_fenced_code(body).splitlines()
            if (match := META_SOURCE_PATTERN.fullmatch(_strip_hard_break(line)))
        ]
        if len(source_matches) != 1:
            errors.append(
                f"{location}: meta blockquote must contain exactly one 收听原节目 line, with an optional official transcript on the same line"
            )
        else:
            source_link, transcript_link = source_matches[0].groups()
            if source_link != fields.get("source_url"):
                errors.append(f"{location}: meta blockquote 收听原节目 link must equal source_url")
            transcript_url = fields.get("transcript_url")
            if transcript_url is None and transcript_link is not None:
                errors.append(f"{location}: meta blockquote must not link an unavailable official transcript")
            elif transcript_url is not None and transcript_link != transcript_url:
                errors.append(f"{location}: meta blockquote transcript link must equal transcript_url")

        tags = fields.get("tags")
        if not isinstance(tags, list) or not tags or any(not str(tag).strip() for tag in tags):
            errors.append(f"{location}: non-demo article must declare a non-empty tags list")
        elif tags_line is None:
            errors.append(f"{location}: non-demo article must include a 标签 line in the meta blockquote")
        else:
            links = META_TAGS_LINK_PATTERN.findall(tags_line[len(META_TAGS_PREFIX) :])
            texts = [text for text, _ in links]
            if texts != [str(tag) for tag in tags] or any(
                unquote(target) != f"/tags/{text}/" for text, target in links
            ):
                errors.append(
                    f"{location}: 标签 line must list exactly the frontmatter tags in order, each linked to /tags/<tag>/"
                )
    return errors


def validate_status_reasons(items: Sequence[Mapping[str, Any]], items_dir: Path, root: Path) -> list[str]:
    errors: list[str] = []
    for item in items:
        path = items_dir / pending.item_relpath(item)
        location = relative(path, root)
        status = item["status"]
        reason = item["reason"]
        if status == "processed" and reason is not None:
            errors.append(f"{location}: processed item reason must be null")
        if status in {"ignored", "failed"} and (not isinstance(reason, str) or not reason.strip()):
            errors.append(f"{location}: {status} item must have a non-empty reason")
    return errors


def validate_correspondence(
    items: Sequence[Mapping[str, Any]], posts: Sequence[Post], root: Path
) -> list[str]:
    errors: list[str] = []
    items_by_id = {str(item["item_id"]): item for item in items}
    posts_by_id: dict[str, Post] = {}

    for post in posts:
        item_id = post.frontmatter.get("item_id")
        if not isinstance(item_id, str):
            continue
        if item_id in posts_by_id:
            errors.append(f"{relative(post.path, root)}: duplicate article item_id: {item_id}")
            continue
        posts_by_id[item_id] = post
        if item_id == DEMO_ITEM_ID:
            continue
        item = items_by_id.get(item_id)
        if item is None:
            errors.append(f"{relative(post.path, root)}: no matching data/items metadata")
            continue
        if item["status"] != "processed":
            errors.append(f"{relative(post.path, root)}: article item status must be processed")
        if post.frontmatter.get("source_url") != item["url"]:
            errors.append(f"{relative(post.path, root)}: source_url must match item metadata url")
        if post.frontmatter.get("source_name") != item["source_name"]:
            errors.append(f"{relative(post.path, root)}: source_name must match item metadata")
        expected_published = (item["published_at"] or "")[:10] or None
        if post.frontmatter.get("published_at") != expected_published:
            errors.append(
                f"{relative(post.path, root)}: published_at must match the item publish date "
                f"({expected_published or 'absent'})"
            )
        year_dir = post.path.parent.name
        source_dir = post.path.parent.parent.name
        if year_dir != pending.item_year(item) or source_dir != item["source_id"]:
            errors.append(
                f"{relative(post.path, root)}: article must be stored as "
                "site/posts/<source_id>/<year>/<item_id>.md matching item metadata"
            )

    for item in items:
        if item["status"] == "processed" and item["item_id"] not in posts_by_id:
            item_path = root / "data" / "items" / pending.item_relpath(item)
            errors.append(
                f"{relative(item_path, root)}: processed item has no matching article"
            )
    return errors


def is_disallowed_repository_path(value: str) -> bool:
    normalized = value.replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    path = PurePosixPath(normalized)
    parts = path.parts
    if not parts:
        return False
    normalized_parts = tuple(part.casefold() for part in parts)
    disallowed_directories = {part.casefold() for part in DISALLOWED_TOP_LEVEL}
    if any(part in disallowed_directories for part in normalized_parts):
        return True
    name = normalized_parts[-1]
    if name == ".env" or name.startswith(".env."):
        return True
    if name in DISALLOWED_NAMES or any(name.endswith(suffix) for suffix in DISALLOWED_SUFFIXES):
        return True
    if name.endswith(".transcript.json"):
        return True
    return False


def validate_directory_contents(root: Path, items_dir: Path, posts_dir: Path) -> list[str]:
    errors: list[str] = []
    if items_dir.is_dir():
        for path in sorted(items_dir.rglob("*"), key=lambda candidate: candidate.as_posix()):
            if path.is_dir():
                continue
            rel_parts = path.relative_to(items_dir).parts
            if len(rel_parts) != 3 or path.suffix != ".json":
                errors.append(
                    f"{relative(path, root)}: data/items item files must use <source_id>/<year>/<item_id>.json layout"
                )
    if posts_dir.is_dir():
        for path in sorted(posts_dir.rglob("*"), key=lambda candidate: candidate.as_posix()):
            if path.is_dir():
                continue
            rel_parts = path.relative_to(posts_dir).parts
            generated_index = path.name == "index.md" and len(rel_parts) == 1
            flat_demo = len(rel_parts) == 1 and path.name == f"{DEMO_ITEM_ID}.md"
            if path.suffix != ".md" or (len(rel_parts) != 3 and not (generated_index or flat_demo)):
                errors.append(
                    f"{relative(path, root)}: site/posts articles must use <source_id>/<year>/<item_id>.md layout "
                    "(only index.md and the demo article may sit directly in site/posts; "
                    "generated show pages live in site/podcasts)"
                )
    return errors


def git_index_paths(root: Path) -> tuple[list[str], list[str]]:
    git_marker = root / ".git"
    if not git_marker.exists():
        return [], []
    try:
        result = subprocess.run(
            ["git", "-c", f"safe.directory={root}", "-C", str(root), "ls-files", "-z"],
            capture_output=True,
            check=False,
        )
    except OSError as error:
        return [], [f"git index check failed: {error}"]
    if result.returncode != 0:
        message = result.stderr.decode("utf-8", errors="replace").strip()
        return [], [f"git index check failed: {message or f'exit {result.returncode}'}"]
    return [path.decode("utf-8", errors="surrogateescape") for path in result.stdout.split(b"\0") if path], []


def run_checks(root: Path, tracked_paths: Sequence[str] | None = None) -> tuple[list[str], int, int]:
    items_dir = root / "data" / "items"
    posts_dir = root / "site" / "posts"
    items, metadata_errors = pending.load_items(items_dir)
    errors = list(metadata_errors)
    errors.extend(validate_directory_contents(root, items_dir, posts_dir))
    errors.extend(validate_status_reasons(items, items_dir, root))

    posts: list[Post] = []
    if not posts_dir.is_dir():
        errors.append(f"{relative(posts_dir, root)}: not a directory")
    else:
        for path in sorted(posts_dir.rglob("*.md"), key=lambda candidate: candidate.as_posix()):
            if path.name == "index.md":
                continue
            try:
                post = parse_post(path)
            except CheckError as error:
                errors.append(f"{relative(path, root)}: {error}")
                continue
            posts.append(post)
            errors.extend(validate_frontmatter(post, root))
            errors.extend(validate_body(post, root))

    errors.extend(validate_correspondence(items, posts, root))
    if tracked_paths is None:
        tracked_paths, git_errors = git_index_paths(root)
        errors.extend(git_errors)
    for path in tracked_paths:
        if is_disallowed_repository_path(path):
            errors.append(f"{path}: private or generated asset must not be tracked or staged")
    return errors, len(items), len(posts)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = args.root.resolve()
    errors, item_count, post_count = run_checks(root)
    print(f"Valid item files: {item_count}")
    print(f"Checked article files: {post_count}")
    print(f"Validation errors: {len(errors)}")
    if errors:
        print("\nErrors:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("EchoForge deterministic checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
