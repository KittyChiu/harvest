#!/usr/bin/env python3
"""Validate a concise Markdown knowledge note."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
FRONT_MATTER = re.compile(r"\A---[ \t]*\r?\n.*?\r?\n---[ \t]*(?:\r?\n|\Z)", re.DOTALL)
H2_HEADING = re.compile(r"^##(?!#)\s+(.+?)\s*#*\s*$", re.MULTILINE)
ANY_HEADING = re.compile(r"^ {0,3}#{1,6}\s+.*$", re.MULTILINE)
LINK_OR_IMAGE = re.compile(r"!?\[([^\]]*)\]\([^)]+\)")
REFERENCE_LINK = re.compile(r"!?\[([^\]]*)\]\[[^\]]*\]")
REFERENCE_DEFINITION = re.compile(r"^\s{0,3}\[[^\]]+\]:\s+\S+.*$", re.MULTILINE)
AUTOLINK = re.compile(r"<(?:https?://|mailto:)[^>]+>")
BARE_URL = re.compile(r"\b(?:https?://|www\.)\S+")
HTML_TAG = re.compile(r"</?[A-Za-z][^>]*>")
WORD = re.compile(r"[^\W_]+(?:['’\-][^\W_]+)*", re.UNICODE)


def fail(message: str) -> None:
    print(f"ERROR: {message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a Markdown knowledge note.")
    parser.add_argument("note", type=Path)
    parser.add_argument(
        "--allow-front-matter",
        action="store_true",
        help="Permit requested YAML front matter; metadata is excluded from word count.",
    )
    return parser.parse_args()


def remove_front_matter(text: str) -> tuple[str, bool]:
    match = FRONT_MATTER.match(text)
    if not match:
        return text, False
    return text[match.end() :], True


def visible_word_count(text: str) -> int:
    text, _ = remove_front_matter(text)
    text = COMMENT.sub(" ", text)
    text = REFERENCE_DEFINITION.sub(" ", text)
    text = LINK_OR_IMAGE.sub(r" \1 ", text)
    text = REFERENCE_LINK.sub(r" \1 ", text)
    text = AUTOLINK.sub(" visible-url ", text)
    text = BARE_URL.sub(" visible-url ", text)
    text = HTML_TAG.sub(" ", text)
    return len(WORD.findall(text))


def section_errors(text: str) -> tuple[list[str], int]:
    errors: list[str] = []
    headings = list(H2_HEADING.finditer(text))
    section_count = len(headings)

    if not 5 <= section_count <= 8:
        errors.append(
            f"Knowledge note requires 5-8 level-two sections; found {section_count}."
        )

    for index, heading in enumerate(headings):
        body_start = heading.end()
        body_end = headings[index + 1].start() if index + 1 < section_count else len(text)
        body = ANY_HEADING.sub(" ", text[body_start:body_end])
        body = COMMENT.sub(" ", body)
        if not WORD.search(body):
            errors.append(
                f'Level-two section "{heading.group(1).strip()}" must not be empty.'
            )

    return errors, section_count


def main() -> int:
    args = parse_args()
    if not args.note.is_file():
        fail(f"File not found: {args.note}")
        return 2

    text = args.note.read_text(encoding="utf-8")
    visible_text, has_front_matter = remove_front_matter(text)
    errors: list[str] = []

    if has_front_matter and not args.allow_front_matter:
        errors.append(
            "Knowledge note must not contain front matter unless "
            "--allow-front-matter is supplied."
        )

    section_issues, section_count = section_errors(visible_text)
    errors.extend(section_issues)

    word_count = visible_word_count(text)
    if word_count > 300:
        errors.append(
            f"Knowledge note must contain at most 300 visible words; found {word_count}."
        )

    for error in errors:
        fail(error)
    print(
        f"Checked knowledge note: {word_count} visible word(s), "
        f"{section_count} level-two section(s), {len(errors)} error(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
