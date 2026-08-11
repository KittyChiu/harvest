#!/usr/bin/env python3
"""Validate a conservative Obsidian-compatible Marp deck."""

from __future__ import annotations

import re
import sys
from pathlib import Path


FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
SLIDE_SEPARATOR = re.compile(r"(?m)^---\s*$")
COMMENT = re.compile(r"<!--(.*?)-->", re.DOTALL)
FENCED_CODE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)
RAW_HTML = re.compile(r"<\s*/?\s*[a-zA-Z][^>]*>")
DIRECTIVE = re.compile(r"^\s*[_$]?[a-zA-Z][\w-]*\s*:")


def fail(message: str) -> None:
    print(f"ERROR: {message}")


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <deck.md>")
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        fail(f"File not found: {path}")
        return 2

    text = path.read_text(encoding="utf-8")
    front = FRONT_MATTER.match(text)
    if not front:
        fail("Missing or malformed YAML front matter.")
        return 1

    metadata = front.group(1)
    required = ("marp: true", "theme:", "size:")
    missing = [item for item in required if item not in metadata]

    body = text[front.end() :]
    slides = SLIDE_SEPARATOR.split(body)
    slides = [slide.strip() for slide in slides if slide.strip()]

    errors: list[str] = []
    warnings: list[str] = []

    if missing:
        errors.append("Front matter is missing: " + ", ".join(missing))
    if not slides:
        errors.append("No slides found.")

    for index, slide in enumerate(slides, start=1):
        comments = COMMENT.findall(slide)
        notes = [
            comment
            for comment in comments
            if comment.strip() and not DIRECTIVE.match(comment.strip())
        ]
        if not notes:
            errors.append(f"Slide {index} has no speaker-note comment.")

        visible = COMMENT.sub("", FENCED_CODE.sub("", slide))
        if RAW_HTML.search(visible):
            errors.append(f"Slide {index} contains raw HTML.")

        visible_words = re.findall(r"\b[\w'-]+\b", visible)
        if len(visible_words) > 90:
            warnings.append(
                f"Slide {index} has {len(visible_words)} visible words; check overflow."
            )

        table_rows = [
            line for line in visible.splitlines() if line.strip().startswith("|")
        ]
        if len(table_rows) > 8:
            warnings.append(
                f"Slide {index} has a large table ({len(table_rows) - 1} rows)."
            )

    for error in errors:
        fail(error)
    for warning in warnings:
        print(f"WARNING: {warning}")

    print(
        f"Checked {len(slides)} slides: "
        f"{len(errors)} error(s), {len(warnings)} warning(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
