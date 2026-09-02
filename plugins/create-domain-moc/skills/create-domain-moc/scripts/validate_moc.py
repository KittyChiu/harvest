#!/usr/bin/env python3
"""Validate one domain Map of Content."""

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
KEBAB_STEM = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*-moc$")
INTERNAL_FILENAME = re.compile(
    r"^[a-z0-9]+(?:-[a-z0-9]+)*(?:\.(?:coach|marp))?\.md$"
)
WORKFLOW_TAGS = {"draft", "review", "publish"}
VISIBILITY_TAGS = {"private", "public"}
RESERVED_TAGS = WORKFLOW_TAGS | VISIBILITY_TAGS | {"moc"}
EMPTY_STATE = re.compile(r"\bNo atomic notes yet\.", re.IGNORECASE)
REQUIRED_SECTIONS = ("scope", "notes")
TEMPLATE_PROMPTS = {
    "# Domain name",
    "Tags: #domain #moc #draft #private",
    "State what belongs in this domain. State the closest material that belongs elsewhere.",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate one domain MOC.")
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


def validate_tags(tags_line: str | None, errors: list[str]) -> None:
    if tags_line is None:
        errors.append("MOC requires a Tags field.")
        return
    tags = {tag.lower() for tag in TAG.findall(tags_line)}
    if "moc" not in tags:
        errors.append("MOC requires the #moc tag.")
    if len(tags & WORKFLOW_TAGS) != 1:
        errors.append("MOC tags must include exactly one workflow tag.")
    if len(tags & VISIBILITY_TAGS) != 1:
        errors.append("MOC tags must include exactly one visibility tag.")
    if not tags - RESERVED_TAGS:
        errors.append("MOC tags must include at least one domain tag.")


def template_prompts(text: str) -> list[str]:
    lines = {line.strip() for line in text.splitlines() if line.strip()}
    return sorted(lines & TEMPLATE_PROMPTS)


def main() -> int:
    args = parse_args()
    if not args.moc.is_file():
        fail(f"File not found: {args.moc}")
        return 2

    text = strip_fenced_blocks(args.moc.read_text(encoding="utf-8"))
    errors: list[str] = []

    if TRANSCLUSION.search(text):
        errors.append("MOC must not use tool-specific wiki transclusions.")
    remaining_prompts = template_prompts(text)
    if remaining_prompts:
        errors.append(
            "MOC contains unreplaced template prompt(s): "
            + ", ".join(remaining_prompts)
        )
    if not KEBAB_STEM.fullmatch(args.moc.stem):
        errors.append("MOC filename must use lowercase kebab-case and end in -moc.md.")
    if len(H1.findall(text)) != 1:
        errors.append("MOC requires exactly one level-one title.")
    validate_tags(field(text, "Tags"), errors)

    sections = [heading.strip().lower() for heading in H2.findall(text)]
    missing_sections = [
        section for section in REQUIRED_SECTIONS if section not in sections
    ]
    if missing_sections:
        errors.append(
            "MOC is missing section(s): " + ", ".join(missing_sections)
        )
    duplicate_sections = [
        section for section in REQUIRED_SECTIONS if sections.count(section) > 1
    ]
    if duplicate_sections:
        errors.append(
            "MOC repeats section(s): " + ", ".join(duplicate_sections)
        )
    required_in_document = [
        section for section in sections if section in REQUIRED_SECTIONS
    ]
    if (
        not missing_sections
        and not duplicate_sections
        and required_in_document != list(REQUIRED_SECTIONS)
    ):
        errors.append(
            "MOC sections must follow this order: "
            + ", ".join(REQUIRED_SECTIONS)
            + "."
        )

    section_bodies: dict[str, str] = {}
    for section in REQUIRED_SECTIONS:
        body = section_body(text, section)
        if body is not None and not WORD.search(strip_internal_links(body)):
            errors.append(f'MOC section "{section.title()}" must not be empty.')
        elif body is not None:
            section_bodies[section] = body

    notes = section_bodies.get("notes", "")
    note_targets = [
        filename
        for _raw, target in internal_links(notes)
        if (filename := normalized_filename(target)) is not None
    ]
    if note_targets and EMPTY_STATE.search(notes):
        errors.append(
            'MOC Notes cannot combine "No atomic notes yet." with atomic-note links.'
        )
    domain = args.moc.stem[: -len("-moc")] if args.moc.stem.endswith("-moc") else ""
    for target in note_targets:
        if (
            target.endswith(("-moc.md", ".coach.md", ".marp.md"))
            or (domain and not target.startswith(f"{domain}-"))
        ):
            errors.append(
                f"MOC Notes may link only to atomic notes in this domain: [[{target}]]."
            )

    for line in text.splitlines():
        links = internal_links(line)
        if not links:
            continue
        prose = strip_internal_links(line)
        prose = re.sub(r"^[\s>*+-]+", "", prose)
        if len(WORD.findall(prose)) < 2:
            errors.append("Every MOC internal link requires explanatory prose.")
        for raw, target in links:
            filename = normalized_filename(target)
            if filename is None or not INTERNAL_FILENAME.fullmatch(filename):
                errors.append(
                    "MOC internal links must use flat lowercase kebab-case "
                    f"Markdown .md filenames or wiki-style targets: {raw}."
                )
                continue
            target_path = (args.moc.parent / filename).resolve()
            if target_path.parent != args.moc.parent.resolve():
                errors.append(
                    f"MOC internal link escapes the knowledge directory: {raw}."
                )
                continue
            if not target_path.is_file():
                errors.append(f"Unresolved MOC internal link: {raw}.")

    for error in errors:
        fail(error)
    print(f"Checked domain MOC: {len(errors)} error(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
