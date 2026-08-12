#!/usr/bin/env python3
"""Validate a conservative Obsidian-compatible Marp deck."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


FRONT_MATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
SLIDE_SEPARATOR = re.compile(r"(?m)^(?:---|===)\s*$")
COMMENT = re.compile(r"<!--(.*?)-->", re.DOTALL)
FENCED_CODE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)
RAW_HTML = re.compile(r"<\s*/?\s*[a-zA-Z][^>]*>")
DIRECTIVE = re.compile(
    r"^\s*(?:"
    r"(?:_?class|_?backgroundColor|_?backgroundImage|_?backgroundPosition|"
    r"_?backgroundRepeat|_?backgroundSize|_?color|_?footer|_?header|"
    r"_?paginate|_?style|_?theme)\s*:|"
    r"\$[a-zA-Z][\w-]*\s*:"
    r")"
)
METADATA_LINE = re.compile(r"^([a-zA-Z][\w-]*)\s*:\s*(.*?)\s*$")
SOURCE_DISPOSITION_COMMENT = re.compile(
    r"^\s*(?:canonical|source)(?:-(visible|notes|optional|excluded))?\s*:\s*(.*?)\s*$",
    re.IGNORECASE | re.DOTALL,
)
SOURCE_CONTRACT_COMMENT = re.compile(
    r"^\s*(?:canonical|source)-contract\s*:\s*(.*?)\s*$",
    re.IGNORECASE | re.DOTALL,
)


def fail(message: str) -> None:
    print(f"ERROR: {message}")


def parse_metadata(metadata: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for line in metadata.splitlines():
        match = METADATA_LINE.match(line)
        if match:
            parsed[match.group(1)] = match.group(2).strip("'\"")
    return parsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a conservative Obsidian-compatible Marp deck."
    )
    parser.add_argument("deck", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    path = args.deck
    if not path.is_file():
        fail(f"File not found: {path}")
        return 2
    text = path.read_text(encoding="utf-8")
    front = FRONT_MATTER.match(text)
    if not front:
        fail("Missing or malformed YAML front matter.")
        return 1

    metadata = parse_metadata(front.group(1))

    body = text[front.end() :]
    slides = SLIDE_SEPARATOR.split(body)
    slides = [slide.strip() for slide in slides if slide.strip()]

    errors: list[str] = []
    warnings: list[str] = []
    markers: list[tuple[str, list[str], str | None, int]] = []
    contract_ids: set[str] = set()

    if metadata.get("marp", "").lower() != "true":
        errors.append("Front matter must set marp: true.")
    for key in ("theme", "size"):
        if not metadata.get(key):
            errors.append(f"Front matter must set a non-empty {key} value.")
    if not slides:
        errors.append("No slides found.")

    for index, slide in enumerate(slides, start=1):
        comments = COMMENT.findall(slide)
        notes = [
            comment
            for comment in comments
            if not DIRECTIVE.match(comment)
            and not SOURCE_DISPOSITION_COMMENT.match(comment)
            and not SOURCE_CONTRACT_COMMENT.match(comment)
        ]
        if not notes:
            errors.append(f"Slide {index} has no speaker-note comment.")

        for comment in comments:
            contract = SOURCE_CONTRACT_COMMENT.match(comment)
            if contract:
                contract_ids.update(
                    item.strip().lower()
                    for item in contract.group(1).split(",")
                    if item.strip()
                )
                continue
            marker = SOURCE_DISPOSITION_COMMENT.match(comment)
            if marker:
                disposition = (marker.group(1) or "visible").lower()
                payload = marker.group(2).strip()
                selector_text, separator, reason_text = payload.partition("|")
                selectors = [
                    item.strip().lower()
                    for item in selector_text.split(",")
                    if item.strip()
                ]
                reason_match = re.fullmatch(
                    r"\s*reason\s*:\s*(.+?)\s*", reason_text, re.IGNORECASE | re.DOTALL
                )
                reason = reason_match.group(1).strip() if reason_match else None
                if not selectors:
                    errors.append(f"Slide {index} has an empty source marker.")
                if separator and not reason_match:
                    errors.append(
                        f"Slide {index} has a malformed source marker reason."
                    )
                if disposition in {"optional", "excluded"} and not reason:
                    errors.append(
                        f"Slide {index} has {disposition} source content without a reason."
                    )
                markers.append((disposition, selectors, reason, index))

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

    source_items = {item: "" for item in contract_ids}
    dispositions: dict[str, set[str]] = {}
    if not source_items:
        errors.append("Deck requires a non-empty source-contract marker.")

    if source_items:
        for disposition, selectors, _reason, slide_index in markers:
            for selector in selectors:
                if selector.endswith("-*"):
                    if disposition not in {"optional", "excluded"}:
                        errors.append(
                            f"Slide {slide_index} uses a whole-group selector for "
                            f"the {disposition} disposition."
                        )
                        continue
                    prefix = selector[:-1]
                    matches = [item for item in source_items if item.startswith(prefix)]
                    if not matches:
                        errors.append(f"Unknown source group selector: {selector}")
                    for item in matches:
                        dispositions.setdefault(item, set()).add(disposition)
                else:
                    dispositions.setdefault(selector, set()).add(disposition)

        unclassified = sorted(set(source_items) - set(dispositions))
        unknown = sorted(set(dispositions) - set(source_items))
        conflicting = sorted(
            item for item, values in dispositions.items() if len(values) > 1
        )
        if unclassified:
            errors.append(
                "Unclassified source item(s): " + ", ".join(unclassified)
            )
        if unknown:
            errors.append("Unknown source item(s): " + ", ".join(unknown))
        if conflicting:
            errors.append(
                "Source item(s) have multiple dispositions: "
                + ", ".join(conflicting)
            )

    for error in errors:
        fail(error)
    for warning in warnings:
        print(f"WARNING: {warning}")

    if source_items:
        print(
            f"Checked contract for {len(source_items)} source item(s): "
            f"{len(set(source_items) - set(dispositions))} unclassified."
        )

    print(
        f"Checked {len(slides)} slides: "
        f"{len(errors)} error(s), {len(warnings)} warning(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
