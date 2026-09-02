#!/usr/bin/env python3
"""Validate a coaching note that accompanies one atomic note."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


H1 = re.compile(r"^#(?!#)\s+(.+?)\s*$", re.MULTILINE)
H2 = re.compile(r"^##(?!#)\s+(.+?)\s*$", re.MULTILINE)
H3 = re.compile(r"^###(?!#)\s+(.+?)\s*$", re.MULTILINE)
WIKI_LINK = re.compile(r"(?<!!)\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
TRANSCLUSION = re.compile(r"!\[\[")
MARKDOWN_LINK = re.compile(
    r"(?<!!)\[[^\]]+\]\(\s*(<?[^)\s>]+>?)\s*(?:[\"'][^)]*[\"'])?\)"
)
TAG = re.compile(r"(?<!\w)#([a-z0-9][a-z0-9-]*)", re.IGNORECASE)
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'-]*")
WORKFLOW_TAGS = {"draft", "review", "publish"}
VISIBILITY_TAGS = {"private", "public"}
RESERVED_TAGS = WORKFLOW_TAGS | VISIBILITY_TAGS | {"coaching", "slides", "moc"}
INTERNAL_FILENAME = re.compile(
    r"^[a-z0-9]+(?:-[a-z0-9]+)*(?:\.(?:coach|marp))?\.md$"
)
REQUIRED_SECTIONS = (
    "teach",
    "watch for",
    "conversation",
    "exercise",
    "adoption",
    "progress signals",
    "common resistance",
)
ADOPTION_SUBSECTIONS = ("start", "continue", "stop")
BULLET = re.compile(r"^\s*[-*+]\s+\S.*$", re.MULTILINE)
QUESTION_BULLET = re.compile(r"^\s*[-*+]\s+\S.*\?\s*$", re.MULTILINE)
NUMBERED_STEP = re.compile(r"^\s*(\d+)\.\s+(\S.*)$", re.MULTILINE)
TABLE_HEADER = re.compile(
    r"^\s*\|\s*Resistance\s*\|\s*Response\s*\|\s*$", re.IGNORECASE
)
TABLE_SEPARATOR = re.compile(
    r"^\s*\|\s*:?-{3,}:?\s*\|\s*:?-{3,}:?\s*\|\s*$"
)
TEMPLATE_PROMPTS = {
    "# Coaching companion: Atomic pattern title",
    "Explain the pattern in simple language.",
    "- What is the idea?",
    "- Why does it matter?",
    "- What misconception does it correct?",
    "Signals that indicate the learner or team would benefit from this pattern.",
    "- Observable behaviour",
    "- Common symptom",
    "- Typical failure mode",
    "Questions to help the learner discover the pattern themselves.",
    "- Question",
    "A small practical activity that lets the learner experience the pattern.",
    "- New behaviour to introduce.",
    "- Existing behaviour worth preserving.",
    "- Behaviour that works against the pattern.",
    "Signs that learning is occurring.",
    "- What to observe.",
    "- What improvement looks like.",
    "- What this signal cannot prove.",
    "Likely objections and how to respond.",
    "|            |          |",
}


def fail(message: str) -> None:
    print(f"ERROR: {message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a coaching companion for an atomic note."
    )
    parser.add_argument("atomic_note", type=Path)
    parser.add_argument("coach_note", type=Path)
    return parser.parse_args()


def field(text: str, name: str) -> str | None:
    match = re.search(rf"^{re.escape(name)}:\s*(.+?)\s*$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


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


def template_prompts(text: str) -> list[str]:
    lines = {line.strip() for line in text.splitlines() if line.strip()}
    return sorted(lines & TEMPLATE_PROMPTS)


def links(value: str | None) -> set[str]:
    return {
        filename.lower()
        for _raw, target in internal_links(value or "")
        if (filename := normalized_filename(target)) is not None
    }


def section_body(text: str, name: str) -> str | None:
    headings = list(H2.finditer(text))
    for index, heading in enumerate(headings):
        if heading.group(1).strip().lower() != name:
            continue
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        return text[heading.end() : end].strip()
    return None


def subsection_body(text: str, name: str) -> str | None:
    headings = list(H3.finditer(text))
    for index, heading in enumerate(headings):
        if heading.group(1).strip().lower() != name:
            continue
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        return text[heading.end() : end].strip()
    return None


def bullet_lines(text: str) -> list[str]:
    return [match.group(0) for match in BULLET.finditer(text)]


def has_populated_resistance_table(text: str) -> bool:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not TABLE_HEADER.fullmatch(line):
            continue
        if index + 1 >= len(lines) or not TABLE_SEPARATOR.fullmatch(lines[index + 1]):
            return False
        for row in lines[index + 2 :]:
            if not row.strip().startswith("|"):
                break
            cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
            if len(cells) == 2 and all(cells):
                return True
        return False
    return False


def validate_tags(tags_line: str | None, errors: list[str]) -> None:
    if tags_line is None:
        errors.append("Coaching note requires a Tags field.")
        return
    tags = {tag.lower() for tag in TAG.findall(tags_line)}
    if "coaching" not in tags:
        errors.append("Coaching note requires the #coaching tag.")
    if len(tags & WORKFLOW_TAGS) != 1:
        errors.append("Tags must include exactly one workflow tag.")
    if len(tags & VISIBILITY_TAGS) != 1:
        errors.append("Tags must include exactly one visibility tag.")
    if not tags - RESERVED_TAGS:
        errors.append("Tags must include at least one domain tag.")


def domain_tags(tags_line: str | None) -> set[str]:
    return {
        tag.lower()
        for tag in TAG.findall(tags_line or "")
        if tag.lower() not in RESERVED_TAGS
    }


def strip_internal_links(text: str) -> str:
    text = WIKI_LINK.sub(" ", text)
    return MARKDOWN_LINK.sub(
        lambda match: " "
        if markdown_link_target(match.group(1)) is not None
        else match.group(0),
        text,
    )


def validate_internal_links(text: str, directory: Path, errors: list[str]) -> None:
    for raw, target in internal_links(text):
        filename = normalized_filename(target)
        if filename is None or not INTERNAL_FILENAME.fullmatch(filename):
            errors.append(
                "Coaching-note internal link must use a flat lowercase kebab-case "
                f"Markdown .md filename or wiki-style target: {raw}."
            )
            continue
        if not (directory / filename).is_file():
            errors.append(f"Coaching note has an unresolved internal link: {raw}.")


def main() -> int:
    args = parse_args()
    missing = [
        path for path in (args.atomic_note, args.coach_note) if not path.is_file()
    ]
    if missing:
        for path in missing:
            fail(f"File not found: {path}")
        return 2

    atomic = strip_fenced_blocks(args.atomic_note.read_text(encoding="utf-8"))
    coach = strip_fenced_blocks(args.coach_note.read_text(encoding="utf-8"))
    errors: list[str] = []

    if TRANSCLUSION.search(atomic) or TRANSCLUSION.search(coach):
        errors.append("Atomic and coaching notes must not use tool-specific wiki transclusions.")
    remaining_prompts = template_prompts(coach)
    if remaining_prompts:
        errors.append(
            "Coaching note contains unreplaced template prompt(s): "
            + ", ".join(remaining_prompts)
        )
    if args.atomic_note.parent.resolve() != args.coach_note.parent.resolve():
        errors.append("Atomic note and coaching note must share a knowledge directory.")
    expected_name = f"{args.atomic_note.stem}.coach.md"
    if args.coach_note.name != expected_name:
        errors.append(f"Coaching-note filename must be {expected_name}.")
    if args.atomic_note.name.endswith(("-moc.md", ".coach.md", ".marp.md")):
        errors.append("Source must be an atomic note.")

    titles = H1.findall(coach)
    if len(titles) != 1:
        errors.append("Coaching note requires exactly one level-one title.")
    elif not re.fullmatch(
        r"Coaching companion:\s+\S.*", titles[0], re.IGNORECASE
    ):
        errors.append(
            'Coaching-note title must use "Coaching companion: <atomic pattern title>".'
        )

    atomic_parent = links(field(atomic, "Parent"))
    coach_parent = links(field(coach, "Parent"))
    if len(atomic_parent) != 1:
        errors.append("Atomic note requires exactly one Parent MOC link.")
    if coach_parent != atomic_parent:
        errors.append("Coaching note must use the atomic note's Parent MOC.")
    if args.atomic_note.name.lower() not in links(field(coach, "Companion to")):
        errors.append("Coaching note must link to the atomic note in Companion to.")

    atomic_tags = field(atomic, "Tags")
    coach_tags = field(coach, "Tags")
    atomic_domains = domain_tags(atomic_tags)
    if not atomic_domains:
        errors.append("Atomic note requires at least one domain tag.")
    validate_tags(coach_tags, errors)
    missing_domains = sorted(atomic_domains - domain_tags(coach_tags))
    if missing_domains:
        errors.append(
            "Coaching note must include the atomic note's domain tag(s): "
            + ", ".join(f"#{tag}" for tag in missing_domains)
        )

    sections = [heading.strip().lower() for heading in H2.findall(coach)]
    missing_sections = [
        section for section in REQUIRED_SECTIONS if section not in sections
    ]
    if missing_sections:
        errors.append("Coaching note is missing section(s): " + ", ".join(missing_sections))
    duplicate_sections = [
        section for section in REQUIRED_SECTIONS if sections.count(section) > 1
    ]
    if duplicate_sections:
        errors.append(
            "Coaching note repeats section(s): " + ", ".join(duplicate_sections)
        )
    unexpected_sections = [
        section for section in sections if section not in REQUIRED_SECTIONS
    ]
    if unexpected_sections:
        errors.append(
            "Coaching note has unexpected section(s): "
            + ", ".join(unexpected_sections)
        )
    required_in_document = [
        section for section in sections if section in REQUIRED_SECTIONS
    ]
    if not missing_sections and required_in_document != list(REQUIRED_SECTIONS):
        errors.append(
            "Coaching-note sections must follow this order: "
            + ", ".join(REQUIRED_SECTIONS)
            + "."
        )
    for section in REQUIRED_SECTIONS:
        body = section_body(coach, section)
        if body is not None and not WORD.search(strip_internal_links(body)):
            errors.append(f'Coaching-note section "{section}" must not be empty.')

    watch_for = section_body(coach, "watch for") or ""
    if watch_for and not bullet_lines(watch_for):
        errors.append('Coaching-note section "watch for" requires at least one bullet.')

    conversation = section_body(coach, "conversation") or ""
    conversation_bullets = bullet_lines(conversation)
    if conversation and (
        len(conversation_bullets) != 3
        or len(QUESTION_BULLET.findall(conversation)) != 3
    ):
        errors.append(
            "Conversation requires exactly three bullet questions ending in ?."
        )

    exercise = section_body(coach, "exercise") or ""
    steps_block = re.search(
        r"^Steps:\s*\n(.*?)(?=^Expected outcome:)",
        exercise,
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    steps = NUMBERED_STEP.findall(steps_block.group(1)) if steps_block else []
    if exercise and [number for number, _body in steps] != ["1", "2", "3"]:
        errors.append("Exercise requires exactly three populated steps numbered 1, 2, 3.")
    outcome = re.search(
        r"^Expected outcome:\s*(.*?)(?=\n###|\Z)",
        exercise,
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if exercise and (
        outcome is None
        or not WORD.search(strip_internal_links(outcome.group(1)))
    ):
        errors.append("Exercise requires a populated Expected outcome.")

    adoption = section_body(coach, "adoption") or ""
    adoption_sections = [
        heading.strip().lower() for heading in H3.findall(adoption)
    ]
    missing_adoption = [
        section for section in ADOPTION_SUBSECTIONS
        if section not in adoption_sections
    ]
    if adoption and missing_adoption:
        errors.append(
            "Adoption is missing subsection(s): " + ", ".join(missing_adoption)
        )
    duplicate_adoption = [
        section for section in ADOPTION_SUBSECTIONS
        if adoption_sections.count(section) > 1
    ]
    if duplicate_adoption:
        errors.append(
            "Adoption repeats subsection(s): " + ", ".join(duplicate_adoption)
        )
    unexpected_adoption = [
        section for section in adoption_sections
        if section not in ADOPTION_SUBSECTIONS
    ]
    if unexpected_adoption:
        errors.append(
            "Adoption has unexpected subsection(s): "
            + ", ".join(unexpected_adoption)
        )
    adoption_in_document = [
        section for section in adoption_sections
        if section in ADOPTION_SUBSECTIONS
    ]
    if (
        adoption
        and not missing_adoption
        and adoption_in_document != list(ADOPTION_SUBSECTIONS)
    ):
        errors.append(
            "Adoption subsections must follow this order: "
            + ", ".join(ADOPTION_SUBSECTIONS)
            + "."
        )
    for section in ADOPTION_SUBSECTIONS:
        body = subsection_body(adoption, section)
        if body is not None and (
            not WORD.search(strip_internal_links(body))
            or not bullet_lines(body)
        ):
            errors.append(
                f'Adoption subsection "{section}" requires at least one populated bullet.'
            )

    progress = section_body(coach, "progress signals") or ""
    if progress and len(bullet_lines(progress)) < 3:
        errors.append("Progress signals requires at least three bullets.")

    resistance = section_body(coach, "common resistance") or ""
    if resistance and not has_populated_resistance_table(resistance):
        errors.append(
            "Common resistance requires a Resistance | Response table "
            "with at least one populated row."
        )

    validate_internal_links(coach, args.coach_note.parent, errors)

    for error in errors:
        fail(error)
    print(f"Checked coaching companion: {len(errors)} error(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
