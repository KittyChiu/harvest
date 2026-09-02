#!/usr/bin/env python3
"""Validate one domain-level Obsidian Marp presentation."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import unquote

REQUIRED_FRONT_MATTER = {
    "marp": "true",
    "theme": None,
    "paginate": None,
    "size": None,
    "title": None,
    "description": None,
}
WORKFLOW_TAGS = {"draft", "review", "publish"}
VISIBILITY_TAGS = {"private", "public"}
RESERVED_TAGS = WORKFLOW_TAGS | VISIBILITY_TAGS | {"moc", "coaching", "slides"}
HTML_TAG = re.compile(r"<(?!\!--)[A-Za-z][^>]*>")
AUTOLINK = re.compile(
    r"<(?:[A-Za-z][A-Za-z0-9+.-]{1,31}:[^ <>\n]*|[^ <>\n@]+@[^ <>\n@]+)>"
)
MARKDOWN_LINK = re.compile(
    r"(?<!!)\[[^\]]+\]\(\s*(<?[^)\s>]+>?)\s*(?:[\"'][^)]*[\"'])?\)"
)
WIKI_LINK = re.compile(r"(?<!!)\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
TAG = re.compile(r"(?<!\w)#([a-z0-9][a-z0-9-]*)\b", re.IGNORECASE)
MOC_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*-moc\.md$")


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip()
    return values, text[end + 5 :]


def split_slides(body: str) -> list[str]:
    slides: list[list[str]] = [[]]
    fence: str | None = None
    in_comment = False
    for line in body.splitlines():
        stripped = line.strip()
        fence_match = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence is not None:
            if fence_match and fence_match.group(1)[0] == fence:
                fence = None
            slides[-1].append(line)
            continue
        if in_comment:
            if "-->" in line:
                in_comment = False
            slides[-1].append(line)
            continue
        if fence_match:
            fence = fence_match.group(1)[0]
            slides[-1].append(line)
            continue
        if "<!--" in line and "-->" not in line.split("<!--", 1)[1]:
            in_comment = True
            slides[-1].append(line)
            continue
        if stripped in {"---", "==="}:
            slides.append([])
        else:
            slides[-1].append(line)
    return ["\n".join(lines).strip() for lines in slides if "\n".join(lines).strip()]


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


def section(text: str, heading: str) -> str | None:
    match = re.search(
        rf"^##\s+{re.escape(heading)}\s*$\n(.*?)(?=^##\s+|\Z)",
        text,
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    return match.group(1).strip() if match else None


def field_values(text: str, name: str) -> list[str]:
    return re.findall(
        rf"^{re.escape(name)}:\s*(.+?)\s*$",
        text,
        re.MULTILINE | re.IGNORECASE,
    )


def link_targets(text: str) -> list[str]:
    targets = MARKDOWN_LINK.findall(text)
    targets.extend(
        target if target.lower().endswith(".md") else f"{target}.md"
        for target in WIKI_LINK.findall(text)
    )
    return targets


def normalize_target(target: str) -> str:
    value = unquote(target.strip().split("#", 1)[0])
    if value.startswith("<") and value.endswith(">"):
        value = value[1:-1]
    return value


def is_external(target: str) -> bool:
    return bool(re.match(r"^(?:[a-z][a-z0-9+.-]*:|//)", target, re.IGNORECASE))


def local_markdown_targets(text: str) -> set[str]:
    targets: set[str] = set()
    for raw_target in link_targets(text):
        target = normalize_target(raw_target)
        if target and not is_external(target) and target.lower().endswith(".md"):
            targets.add(target)
    return targets


def tags_from_fields(text: str) -> set[str]:
    return {
        tag.lower()
        for value in field_values(text, "Tags")
        for tag in TAG.findall(value)
    }


def resolve_target(base: Path, target: str) -> Path | None:
    normalized = normalize_target(target)
    if not normalized or is_external(normalized):
        return None
    return (base / normalized).resolve()


def source_targets(text: str, field_name: str) -> set[str]:
    return {
        normalize_target(target)
        for value in field_values(text, field_name)
        for target in link_targets(value)
        if normalize_target(target)
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate one <domain>.marp.md presentation against its domain MOC."
    )
    parser.add_argument("deck", type=Path)
    parser.add_argument("moc", type=Path)
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    deck = args.deck.resolve()
    moc = args.moc.resolve()

    for path, label in ((deck, "Deck"), (moc, "MOC")):
        if not path.is_file():
            errors.append(f"{label} file does not exist: {path}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    if deck.parent != moc.parent:
        errors.append("Deck and MOC must be in the same knowledge directory.")

    if not MOC_NAME.fullmatch(moc.name):
        errors.append("MOC filename must use lowercase kebab-case and end in '-moc.md'.")
        domain = moc.stem
    else:
        domain = moc.name[: -len("-moc.md")]

    expected_deck = f"{domain}.marp.md"
    if deck.name != expected_deck:
        errors.append(
            f"Deck filename must be '{expected_deck}', derived from '{moc.name}'."
        )
    if deck.name != deck.name.lower() or moc.name != moc.name.lower():
        errors.append("Deck and MOC filenames must use lowercase characters.")

    deck_text = deck.read_text(encoding="utf-8")
    moc_text = moc.read_text(encoding="utf-8")
    front_matter, body = parse_front_matter(deck_text)
    if not front_matter:
        errors.append("Deck must begin with valid YAML front matter.")
    else:
        for key, expected in REQUIRED_FRONT_MATTER.items():
            value = front_matter.get(key, "").strip()
            if not value:
                errors.append(f"Front matter requires a non-empty '{key}' field.")
            elif expected is not None and value.lower() != expected:
                errors.append(f"Front matter '{key}' must be '{expected}'.")

    slides = split_slides(body)
    scan_body = strip_fenced_blocks(body)

    notes = section(moc_text, "Notes")
    if notes is None:
        errors.append("MOC requires a level-2 'Notes' section.")
        atomic_targets: set[str] = set()
    else:
        atomic_targets = local_markdown_targets(notes)
        if not atomic_targets:
            errors.append("MOC Notes must link at least one atomic note.")

    expected_atomic: set[str] = set()
    expected_coaches: set[str] = set()
    for target in atomic_targets:
        target_path = Path(target)
        if target_path.name != target or target != target.lower():
            errors.append(
                f"MOC atomic-note link '{target}' must be a lowercase flat filename."
            )
            continue
        if (
            not target.endswith(".md")
            or target.endswith(("-moc.md", ".coach.md", ".marp.md"))
            or not target.startswith(f"{domain}-")
        ):
            errors.append(
                f"MOC Notes link '{target}' is not an atomic note in domain '{domain}'."
            )
            continue
        atomic_path = (moc.parent / target).resolve()
        if not atomic_path.is_file():
            errors.append(f"MOC atomic-note link does not resolve: {target}")
            continue
        expected_atomic.add(target)
        coach_target = f"{target[:-3]}.coach.md"
        if (moc.parent / coach_target).is_file():
            expected_coaches.add(coach_target)

    moc_values = field_values(scan_body, "MOC")
    moc_links = source_targets(scan_body, "MOC")
    expected_moc = {moc.name}
    opening_moc_links = source_targets(slides[0], "MOC") if slides else set()
    if (
        len(moc_values) != 1
        or moc_links != expected_moc
        or opening_moc_links != expected_moc
    ):
        errors.append(
            f"Opening slide must contain the only MOC field linking exactly '{moc.name}'; "
            f"found {len(moc_values)} fields and links {sorted(moc_links)}."
        )

    deck_sources = source_targets(scan_body, "Source")
    if deck_sources != expected_atomic:
        missing = sorted(expected_atomic - deck_sources)
        extra = sorted(deck_sources - expected_atomic)
        if missing:
            errors.append(f"Deck is missing atomic Source links: {missing}.")
        if extra:
            errors.append(f"Deck has Source links outside the MOC: {extra}.")

    deck_coaches = source_targets(scan_body, "Coach source")
    if deck_coaches != expected_coaches:
        missing = sorted(expected_coaches - deck_coaches)
        extra = sorted(deck_coaches - expected_coaches)
        if missing:
            errors.append(f"Deck is missing available Coach source links: {missing}.")
        if extra:
            errors.append(f"Deck has unexpected Coach source links: {extra}.")

    moc_tags = tags_from_fields(moc_text)
    domain_tags = moc_tags - RESERVED_TAGS
    deck_tags = tags_from_fields(scan_body)
    if not domain_tags:
        errors.append("MOC Tags must include at least one domain tag.")
    elif not domain_tags.issubset(deck_tags):
        errors.append(
            f"Deck Tags must include every MOC domain tag: {sorted(domain_tags)}."
        )
    if "slides" not in deck_tags:
        errors.append("Deck Tags must include '#slides'.")
    workflow = deck_tags & WORKFLOW_TAGS
    visibility = deck_tags & VISIBILITY_TAGS
    if len(workflow) != 1:
        errors.append("Deck Tags must include exactly one workflow tag.")
    if len(visibility) != 1:
        errors.append("Deck Tags must include exactly one visibility tag.")

    if len(slides) < 3:
        errors.append("Domain presentation must contain at least 3 slides.")
    if len(slides) > 30:
        warnings.append(
            f"Deck has {len(slides)} slides; review whether the domain narrative is focused."
        )

    for index, slide in enumerate(slides, start=1):
        if source_targets(strip_fenced_blocks(slide), "Coach source"):
            note_blocks = re.findall(r"<!--(.*?)-->", slide, re.DOTALL)
            coaching_blocks = [
                block for block in note_blocks if re.search(r"\bCoach cue:\s*\S", block)
            ]
            if not coaching_blocks:
                errors.append(
                    f"Slide {index} has a Coach source and requires a non-empty "
                    "speaker-note comment beginning with 'Coach cue:'."
                )
        visible = re.sub(r"<!--.*?-->", "", slide, flags=re.DOTALL).strip()
        visible_lines = [line for line in visible.splitlines() if line.strip()]
        if len(visible_lines) > 12:
            warnings.append(
                f"Slide {index} has {len(visible_lines)} visible lines; review projection density."
            )

    without_comments = re.sub(r"<!--.*?-->", "", scan_body, flags=re.DOTALL)
    without_autolinks = AUTOLINK.sub("", without_comments)
    if HTML_TAG.search(without_autolinks):
        errors.append("Arbitrary HTML is not allowed; use Markdown and speaker-note comments.")

    allowed_root = deck.parent.resolve()
    for target in link_targets(scan_body):
        normalized = normalize_target(target)
        if not normalized or is_external(normalized):
            continue
        if normalized.endswith(".MD") or not normalized.endswith(".md"):
            errors.append(
                f"Internal link '{normalized}' must use the lowercase '.md' extension."
            )
            continue
        if Path(normalized).name != normalized:
            errors.append(f"Internal link '{normalized}' must be a flat filename.")
            continue
        resolved = resolve_target(deck.parent, normalized)
        if resolved is None or resolved.parent != allowed_root:
            errors.append(
                f"Internal link '{normalized}' must stay in the knowledge directory."
            )
        elif not resolved.is_file():
            errors.append(f"Internal link does not resolve: {normalized}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(
        "OK: domain Marp presentation is valid "
        f"({len(slides)} slides, {len(expected_atomic)} atomic sources, "
        f"{len(expected_coaches)} coaching sources)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
