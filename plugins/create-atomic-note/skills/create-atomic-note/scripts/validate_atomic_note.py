#!/usr/bin/env python3
"""Validate an atomic note and its domain Map of Content."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


H1 = re.compile(r"^#(?!#)\s+(.+?)\s*$", re.MULTILINE)
H2 = re.compile(r"^##(?!#)\s+(.+?)\s*$", re.MULTILINE)
WIKI_LINK = re.compile(r"(?<!!)\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
TRANSCLUSION = re.compile(r"!\[\[")
MARKDOWN_LINK = re.compile(
    r"(?<!!)\[[^\]]+\]\(\s*(<?[^)\s>]+>?)\s*(?:[\"'][^)]*[\"'])?\)"
)
TAG = re.compile(r"(?<!\w)#([a-z0-9][a-z0-9-]*)", re.IGNORECASE)
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'-]*")
WORKFLOW_TAGS = {"draft", "review", "publish"}
VISIBILITY_TAGS = {"private", "public"}
RESERVED_TAGS = WORKFLOW_TAGS | VISIBILITY_TAGS | {"moc"}
REQUIRED_SECTIONS = {
    "core idea",
    "why it matters",
    "practices",
    "constraints",
    "relationships",
}
KEBAB_STEM = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
INTERNAL_FILENAME = re.compile(
    r"^[a-z0-9]+(?:-[a-z0-9]+)*(?:\.(?:coach|marp))?\.md$"
)
EMPTY_MOC = re.compile(r"\bNo atomic notes yet\.", re.IGNORECASE)


def fail(message: str) -> None:
    print(f"ERROR: {message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate an atomic note and its domain MOC."
    )
    parser.add_argument("note", type=Path)
    parser.add_argument("moc", type=Path)
    return parser.parse_args()


def field(text: str, name: str) -> str | None:
    match = re.search(rf"^{re.escape(name)}:\s*(.+?)\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def section_body(text: str, name: str) -> str | None:
    headings = list(H2.finditer(text))
    for index, heading in enumerate(headings):
        if heading.group(1).strip().lower() != name:
            continue
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        return text[heading.end() : end].strip()
    return None


def markdown_link_target(destination: str) -> str | None:
    destination = destination.strip("<>")
    if (
        "://" in destination
        or destination.startswith(("mailto:", "#", "//"))
    ):
        return None
    path = destination.split("#", 1)[0].split("?", 1)[0]
    if path.endswith(".md"):
        return path
    return path if path.lower().endswith(".md") else None


def internal_links(text: str) -> list[tuple[str, str]]:
    links = [(match.group(0), match.group(1)) for match in WIKI_LINK.finditer(text)]
    for match in MARKDOWN_LINK.finditer(text):
        target = markdown_link_target(match.group(1))
        if target is not None:
            links.append((match.group(0), target))
    return links


def strip_internal_links(text: str) -> str:
    text = WIKI_LINK.sub(" ", text)
    return MARKDOWN_LINK.sub(
        lambda match: " "
        if markdown_link_target(match.group(1)) is not None
        else match.group(0),
        text,
    )


def normalized_filename(target: str) -> str | None:
    filename = target if target.lower().endswith(".md") else f"{target}.md"
    path = Path(filename)
    if path.parent != Path("."):
        return None
    return path.name


def strip_fenced_blocks(text: str) -> str:
    visible_lines: list[str] = []
    fence: str | None = None
    for line in text.splitlines():
        fence_match = re.match(r"^(`{3,}|~{3,})", line.strip())
        if fence is not None:
            if fence_match and fence_match.group(1)[0] == fence:
                fence = None
            visible_lines.append("")
            continue
        if fence_match:
            fence = fence_match.group(1)[0]
            visible_lines.append("")
            continue
        visible_lines.append(line)
    return "\n".join(visible_lines)


def link_filenames(text: str) -> set[str]:
    return {
        filename.lower()
        for _raw, target in internal_links(text)
        if (filename := normalized_filename(target)) is not None
    }


def has_descriptive_link(line: str, target: str) -> bool:
    if target.lower() not in link_filenames(line):
        return False
    prose = strip_internal_links(line)
    prose = re.sub(r"^[\s>*+-]+", "", prose)
    return len(WORD.findall(prose)) >= 2


def validate_internal_links(
    text: str, directory: Path, artifact: str, errors: list[str]
) -> None:
    for raw, target in internal_links(text):
        filename = normalized_filename(target)
        if filename is None or not INTERNAL_FILENAME.fullmatch(filename):
            errors.append(
                f"{artifact} internal link must use a flat lowercase kebab-case "
                f"Markdown .md filename or wiki-style target: {raw}."
            )
            continue
        if not (directory / filename).is_file():
            errors.append(f"{artifact} has an unresolved internal link: {raw}.")


def validate_tags(
    tags_line: str | None,
    errors: list[str],
    artifact: str,
    required_type_tag: str | None = None,
) -> None:
    if tags_line is None:
        errors.append(f"{artifact} requires a Tags field.")
        return
    tags = {tag.lower() for tag in TAG.findall(tags_line)}
    if required_type_tag and required_type_tag not in tags:
        errors.append(f"{artifact} requires the #{required_type_tag} tag.")
    if not tags & WORKFLOW_TAGS:
        errors.append(
            f"{artifact} tags must include one workflow tag: "
            "#draft, #review, or #publish."
        )
    if len(tags & WORKFLOW_TAGS) > 1:
        errors.append(f"{artifact} tags must include exactly one workflow tag.")
    if not tags & VISIBILITY_TAGS:
        errors.append(
            f"{artifact} tags must include one visibility tag: #private or #public."
        )
    if len(tags & VISIBILITY_TAGS) > 1:
        errors.append(f"{artifact} tags must include exactly one visibility tag.")
    if not tags - RESERVED_TAGS:
        errors.append(f"{artifact} tags must include at least one domain tag.")


def main() -> int:
    args = parse_args()
    missing = [path for path in (args.note, args.moc) if not path.is_file()]
    if missing:
        for path in missing:
            fail(f"File not found: {path}")
        return 2

    errors: list[str] = []
    note = strip_fenced_blocks(args.note.read_text(encoding="utf-8"))
    moc = strip_fenced_blocks(args.moc.read_text(encoding="utf-8"))

    if TRANSCLUSION.search(note) or TRANSCLUSION.search(moc):
        errors.append("Atomic note and MOC must not use tool-specific wiki transclusions.")
    if args.note.parent.resolve() != args.moc.parent.resolve():
        errors.append("Atomic note and MOC must be in the same knowledge directory.")
    if not args.note.name.endswith(".md") or args.note.name.endswith(
        ("-moc.md", ".coach.md", ".marp.md")
    ):
        errors.append("Atomic-note filename must end in .md and identify an atomic note.")
    if not KEBAB_STEM.fullmatch(args.note.stem):
        errors.append("Atomic-note filename must use lowercase kebab-case.")
    if not args.moc.name.endswith("-moc.md"):
        errors.append("MOC filename must end in -moc.md.")
        domain = ""
    else:
        domain = args.moc.stem[: -len("-moc")]
    if not KEBAB_STEM.fullmatch(args.moc.stem):
        errors.append("MOC filename must use lowercase kebab-case.")
    if domain and not args.note.stem.startswith(f"{domain}-"):
        errors.append("Atomic-note filename must begin with the MOC domain stem.")

    if len(H1.findall(note)) != 1:
        errors.append("Atomic note requires exactly one level-one title.")
    if len(H1.findall(moc)) != 1:
        errors.append("MOC requires exactly one level-one title.")

    parent = field(note, "Parent")
    parent_links = link_filenames(parent or "")
    if parent is None:
        errors.append("Atomic note requires a Parent field.")
    elif parent_links != {args.moc.name.lower()}:
        errors.append("Atomic-note Parent must contain exactly the supplied MOC link.")

    validate_tags(field(note, "Tags"), errors, "Atomic note")
    validate_tags(field(moc, "Tags"), errors, "MOC", "moc")

    sections = {heading.strip().lower() for heading in H2.findall(note)}
    missing_sections = sorted(REQUIRED_SECTIONS - sections)
    if missing_sections:
        errors.append("Atomic note is missing section(s): " + ", ".join(missing_sections))
    for section in REQUIRED_SECTIONS:
        body = section_body(note, section)
        if body is not None and not WORD.search(strip_internal_links(body)):
            errors.append(f'Atomic-note section "{section}" must not be empty.')

    relationships = section_body(note, "relationships") or ""
    for line in relationships.splitlines():
        if internal_links(line):
            prose = strip_internal_links(line)
            if len(WORD.findall(prose)) < 2:
                errors.append("Every relationship link requires explanatory prose.")

    moc_notes = section_body(moc, "notes")
    if moc_notes is None:
        errors.append("MOC requires a Notes section.")
        moc_notes = ""
    moc_link_lines = [
        line
        for line in moc_notes.splitlines()
        if args.note.name.lower() in link_filenames(line)
    ]
    if not moc_link_lines:
        errors.append("MOC must link to the atomic note.")
    elif not any(has_descriptive_link(line, args.note.name) for line in moc_link_lines):
        errors.append("MOC entry for the atomic note requires a navigation description.")
    if moc_link_lines and EMPTY_MOC.search(moc_notes):
        errors.append(
            'MOC Notes cannot combine "No atomic notes yet." with atomic-note links.'
        )
    for _raw, target in internal_links(moc_notes):
        filename = normalized_filename(target)
        if filename is None:
            continue
        if (
            filename.endswith(("-moc.md", ".coach.md", ".marp.md"))
            or (domain and not filename.startswith(f"{domain}-"))
        ):
            errors.append(
                f"MOC Notes may link only to atomic notes in this domain: {filename}."
            )

    validate_internal_links(note, args.note.parent, "Atomic note", errors)
    validate_internal_links(moc, args.moc.parent, "MOC", errors)

    for error in errors:
        fail(error)
    print(f"Checked atomic note and MOC: {len(errors)} error(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
