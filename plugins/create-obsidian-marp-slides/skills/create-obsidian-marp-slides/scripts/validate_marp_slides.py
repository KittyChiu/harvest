#!/usr/bin/env python3
"""Validate one domain-level Obsidian Marp presentation."""

from __future__ import annotations

import argparse
import re
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
CORE_SLIDE_TITLES = (
    "Challenges & opportunities",
    "Pattern map",
    "Apply the patterns together",
    "What changes",
    "Pattern map revisited",
    "Choose one pattern to try",
)
SUPPORTED_RELATIONSHIPS = {
    "enables",
    "precedes",
    "informs",
    "complements",
    "contrasts with",
    "depends on",
}

HTML_TAG = re.compile(r"<(?!\!--)[A-Za-z][^>]*>")
AUTOLINK = re.compile(
    r"<(?:[A-Za-z][A-Za-z0-9+.-]{1,31}:[^ <>\n]*|[^ <>\n@]+@[^ <>\n@]+)>"
)
MARKDOWN_LINK = re.compile(
    r"(?<!!)\[[^\]]+\]\(\s*(<?[^)\s>]+>?)\s*(?:[\"'][^)]*[\"'])?\)"
)
MARKDOWN_LINK_DISPLAY = re.compile(
    r"(?<!!)\[([^\]]+)\]\(\s*<?[^)\s>]+>?\s*(?:[\"'][^)]*[\"'])?\)"
)
WIKI_LINK = re.compile(r"(?<!!)\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
WIKI_LINK_DISPLAY = re.compile(
    r"(?<!!)\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]"
)
TAG = re.compile(r"(?<!\w)#([a-z0-9][a-z0-9-]*)\b", re.IGNORECASE)
MOC_NAME = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*-moc\.md$")
H1 = re.compile(r"^#(?!#)\s+(.+?)\s*$", re.MULTILINE)
PATTERN_HEADER = re.compile(
    r"^######\s+p(\d+)\s+of\s+(\d+)\s+·\s+(\S.*?)\s*$",
    re.MULTILINE,
)
PATTERN_HEADER_CANDIDATE = re.compile(
    r"^######\s+\S+\s+of\s+\d+\s+·\s+\S",
    re.MULTILINE | re.IGNORECASE,
)
PATTERN_FORM = re.compile(
    r"^When\b.+,\s*.+,\s*because\b.+[.!?]$",
    re.IGNORECASE,
)
BULLET = re.compile(r"^\s*[-*+]\s+\S.*$", re.MULTILINE)
ATOMIC_RELATIONSHIP_LINE = re.compile(
    r"^\s*[-*+]\s+(?:\*\*)?"
    r"(prerequisite|extension|contrast|example)"
    r"(?:\*\*)?:\s+",
    re.IGNORECASE,
)
MERMAID_NODE = re.compile(
    r'^\s*([A-Za-z][A-Za-z0-9_-]*)\s*\[\s*"([^"]+)"\s*\]\s*$',
    re.MULTILINE,
)
MERMAID_ID_TOKEN = re.compile(r"\b([A-Za-z][A-Za-z0-9_-]*)\b")
MERMAID_PIPE_LABEL = re.compile(r"\|\s*\"?([^\"|]+?)\"?\s*\|")
MERMAID_INLINE_LABEL = re.compile(
    r"(?:--|-\.)\s+(.+?)\s+(?:-->|\.->)|"
    r"==\s+(.+?)\s+==>"
)
NOTE_LABEL = re.compile(r"^([A-Z][A-Za-z ]+):[ \t]*(.*?)$", re.MULTILINE)
NOTE_ONLY_VISIBLE = re.compile(
    r"^\s*(?:#{1,6}\s+)?(?:Narrative|Domain question|Pattern description|"
    r"Coach cue|Related|Source|Metadata|Evidence|Remaining constraint|"
    r"Domain takeaway|Selection rule):",
    re.MULTILINE | re.IGNORECASE,
)
SPEAKER_NOTE_ONLY_FIELDS = (
    "Narrative",
    "Domain question",
    "Pattern description",
    "Coach cue",
    "Related",
    "Evidence",
    "Remaining constraint",
    "Domain takeaway",
    "Selection rule",
)
POSITION_PLACEHOLDER = re.compile(r"\bp\[\d+\]", re.IGNORECASE)
BRACKET_PLACEHOLDER = re.compile(
    r"(?<![\[\w])\[(?!\[)([^\]\n]+)\](?!\()"
)
TEMPLATE_PROMPTS = (
    "INPUTS",
    "AUTHORING RULES",
    "PATTERN SLIDE",
    "Duplicate this slide once for each pattern.",
    "Replace the position, total, cluster, name, signals, practices, and notes.",
    "Optional: use only when two patterns are genuine alternatives.",
)


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


def opening_fence(line: str) -> tuple[str, int, str] | None:
    match = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
    if match is None:
        return None
    marker = match.group(1)
    return marker[0], len(marker), match.group(2).strip()


def closes_fence(line: str, marker: str, length: int) -> bool:
    return bool(re.fullmatch(rf"\s*{re.escape(marker)}{{{length},}}\s*", line))


def split_slides(body: str) -> list[str]:
    slides: list[list[str]] = [[]]
    fence: tuple[str, int] | None = None
    in_comment = False
    for line in body.splitlines():
        stripped = line.strip()
        if fence is not None:
            if closes_fence(line, *fence):
                fence = None
            slides[-1].append(line)
            continue
        if in_comment:
            if "-->" in line:
                in_comment = False
            slides[-1].append(line)
            continue
        fence_match = opening_fence(line)
        if fence_match is not None:
            fence = fence_match[0], fence_match[1]
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


def fenced_blocks(text: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    fence: tuple[str, int, str] | None = None
    content: list[str] = []
    for line in text.splitlines():
        if fence is not None:
            if closes_fence(line, fence[0], fence[1]):
                blocks.append((fence[2], "\n".join(content)))
                fence = None
                content = []
            else:
                content.append(line)
            continue
        match = opening_fence(line)
        if match is not None:
            language = match[2].split(maxsplit=1)[0].lower() if match[2] else ""
            fence = match[0], match[1], language
    return blocks


def strip_fenced_blocks(text: str) -> str:
    visible_lines: list[str] = []
    fence: tuple[str, int] | None = None
    for line in text.splitlines():
        if fence is not None:
            if closes_fence(line, *fence):
                fence = None
            visible_lines.append("")
            continue
        match = opening_fence(line)
        if match is not None:
            fence = match[0], match[1]
            visible_lines.append("")
            continue
        visible_lines.append(line)
    return "\n".join(visible_lines)


def strip_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def speaker_notes(slide: str) -> str:
    return "\n\n".join(
        match.group(1).strip()
        for match in re.finditer(r"<!--(.*?)-->", slide, re.DOTALL)
        if match.group(1).strip()
        and not match.group(1).strip().lower().startswith("markdownlint-")
    )


def note_field(notes: str, name: str) -> str | None:
    matches = list(NOTE_LABEL.finditer(notes))
    for index, match in enumerate(matches):
        if match.group(1).strip().lower() != name.lower():
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(notes)
        inline = match.group(2).strip()
        remainder = notes[match.end() : end].strip()
        return "\n".join(part for part in (inline, remainder) if part).strip()
    return None


def note_field_positions(notes: str, names: tuple[str, ...]) -> list[int]:
    positions: list[int] = []
    for name in names:
        match = re.search(rf"^{re.escape(name)}:", notes, re.MULTILINE)
        if match is not None:
            positions.append(match.start())
    return positions


def section(text: str, heading: str, level: int = 2) -> str | None:
    marker = "#" * level
    match = re.search(
        rf"^{marker}(?!#)\s+{re.escape(heading)}\s*$\n"
        rf"(.*?)(?=^{marker}(?!#)\s+|\Z)",
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


def local_markdown_target_list(text: str) -> list[str]:
    targets: list[str] = []
    for raw_target in link_targets(text):
        target = normalize_target(raw_target)
        if target and not is_external(target) and target.lower().endswith(".md"):
            targets.append(target)
    return targets


def local_markdown_targets(text: str) -> set[str]:
    return set(local_markdown_target_list(text))


def strict_source_targets(
    notes: str,
    slide_name: str,
    errors: list[str],
) -> list[str]:
    value = note_field(notes, "Source")
    if value is None:
        return []
    targets: list[str] = []
    for line in (line.strip() for line in value.splitlines() if line.strip()):
        raw_targets = link_targets(line)
        remainder = MARKDOWN_LINK.sub("", line)
        remainder = WIKI_LINK.sub("", remainder).strip()
        if len(raw_targets) != 1 or remainder:
            errors.append(
                f"{slide_name} speaker-note Source must contain only one "
                "Markdown or wiki link per line."
            )
            continue
        target = normalize_target(raw_targets[0])
        if (
            not target
            or is_external(target)
            or not target.lower().endswith(".md")
        ):
            errors.append(
                f"{slide_name} speaker-note Source links must use local Markdown files."
            )
            continue
        targets.append(target)
    duplicates = sorted(
        target for target in set(targets) if targets.count(target) > 1
    )
    if duplicates:
        errors.append(
            f"{slide_name} speaker-note Source repeats link(s): {duplicates}."
        )
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


def visible_slide(slide: str) -> str:
    return strip_comments(strip_fenced_blocks(slide))


def slide_title(slide: str) -> str | None:
    match = H1.search(visible_slide(slide))
    return match.group(1).strip() if match else None


def find_slide(slides: list[str], title: str) -> tuple[int, str] | None:
    for index, slide in enumerate(slides):
        if (slide_title(slide) or "").lower() == title.lower():
            return index, slide
    return None


def require_note_fields(
    notes: str,
    labels: tuple[str, ...],
    slide_name: str,
    errors: list[str],
) -> None:
    for label in labels:
        value = note_field(notes, label)
        if value is None or not value.strip():
            errors.append(f"{slide_name} speaker notes require a non-empty '{label}' field.")


def require_question(
    notes: str,
    label: str,
    slide_name: str,
    errors: list[str],
) -> None:
    value = note_field(notes, label)
    if value is None or not value.rstrip().endswith("?"):
        errors.append(
            f"{slide_name} speaker notes require '{label}' ending in ?."
        )


def allowed_deck_relationships(
    directory: Path, atomic_sources: set[str]
) -> set[tuple[str, str, str]]:
    allowed: set[tuple[str, str, str]] = set()
    for source in atomic_sources:
        text = strip_fenced_blocks((directory / source).read_text(encoding="utf-8"))
        relationships = section(text, "Relationships") or ""
        for line in relationships.splitlines():
            match = ATOMIC_RELATIONSHIP_LINE.match(line)
            if match is None:
                continue
            relationship_type = match.group(1).lower()
            for target in local_markdown_targets(line):
                if target not in atomic_sources or target == source:
                    continue
                if relationship_type == "prerequisite":
                    allowed.add((source, "depends on", target))
                    allowed.add((target, "precedes", source))
                elif relationship_type == "extension":
                    for label in ("enables", "informs", "complements"):
                        allowed.add((source, label, target))
                elif relationship_type == "contrast":
                    allowed.add((source, "contrasts with", target))
    return allowed


def mermaid_node_labels(text: str) -> dict[str, str]:
    return {
        match.group(1): match.group(2).strip()
        for match in MERMAID_NODE.finditer(text)
    }


def parse_named_relationship(
    line: str,
    name_to_source: dict[str, str],
) -> tuple[str, str, str] | None:
    cleaned = re.sub(r"^\s*[-*+]\s+", "", line).strip()
    names = sorted(name_to_source, key=len, reverse=True)
    for source_name in names:
        for target_name in names:
            if source_name == target_name:
                continue
            match = re.fullmatch(
                rf"{re.escape(source_name)}\s+(.+?)\s+{re.escape(target_name)}",
                cleaned,
                re.IGNORECASE,
            )
            if match is not None:
                return (
                    name_to_source[source_name],
                    " ".join(match.group(1).lower().split()),
                    name_to_source[target_name],
                )
    return None


def relationship_claims(
    body: str,
    slides: list[str],
    pattern_sources: dict[int, str],
    pattern_names: dict[int, str],
    pattern_slides: dict[int, tuple[int, str]],
    errors: list[str],
) -> set[tuple[str, str, str]]:
    name_to_source = {
        pattern_names[pattern_id].lower(): source
        for pattern_id, source in pattern_sources.items()
        if pattern_id in pattern_names
    }
    claims: set[tuple[str, str, str]] = set()
    labels: set[str] = set()

    for language, content in fenced_blocks(strip_comments(body)):
        if language != "mermaid":
            continue
        nodes = mermaid_node_labels(content)
        for line in content.splitlines():
            node_tokens = [
                token
                for token in MERMAID_ID_TOKEN.finditer(line)
                if token.group(1) in nodes
            ]
            for source_token, target_token in zip(node_tokens, node_tokens[1:]):
                connector = line[source_token.end() : target_token.start()]
                if not re.search(r"[-=.~]{2}", connector):
                    continue
                source_name = nodes[source_token.group(1)].lower()
                target_name = nodes[target_token.group(1)].lower()
                source = name_to_source.get(source_name)
                target = name_to_source.get(target_name)

                pipe_label = MERMAID_PIPE_LABEL.search(connector)
                inline_label = MERMAID_INLINE_LABEL.search(connector)
                label_text = (
                    pipe_label.group(1)
                    if pipe_label is not None
                    else next(
                        (
                            group
                            for group in (
                                inline_label.groups() if inline_label else ()
                            )
                            if group is not None
                        ),
                        None,
                    )
                )
                if label_text is not None:
                    label = " ".join(label_text.lower().split())
                    labels.add(label)
                    if source is not None and target is not None and source != target:
                        claims.add((source, label, target))
                    elif source is not None or target is not None:
                        errors.append(
                            "Labeled Mermaid relationship must connect two known "
                            f"pattern names: {line.strip()}."
                        )
                    continue
                if source is not None and target is not None and source != target:
                    errors.append(
                        "Mermaid edges between patterns require a supported relationship "
                        f"label: {line.strip()}."
                    )

    slide_to_pattern = {
        slide_index: pattern_id
        for pattern_id, (slide_index, _slide) in pattern_slides.items()
    }
    for slide_index, slide in enumerate(slides, start=1):
        notes = speaker_notes(slide)
        related = note_field(notes, "Related")
        if related is None:
            continue
        if not related.strip():
            errors.append(
                f"Slide {slide_index} must omit Related when no supported "
                "relationship exists."
            )
            continue
        atomic_sources = [
            target
            for target in local_markdown_target_list(note_field(notes, "Source") or "")
            if target in set(pattern_sources.values())
        ]
        current_source = None
        pattern_id = slide_to_pattern.get(slide_index)
        if pattern_id is not None:
            current_source = pattern_sources.get(pattern_id)
        elif len(set(atomic_sources)) == 1:
            current_source = atomic_sources[0]

        for line in related.splitlines():
            cleaned = re.sub(r"^\s*[-*+]\s+", "", line).strip()
            if not cleaned:
                continue
            parenthetical = re.fullmatch(r"(.+?)\s+\(([^()]+)\)", cleaned)
            if parenthetical is not None and current_source is not None:
                target = name_to_source.get(parenthetical.group(1).strip().lower())
                label = " ".join(parenthetical.group(2).lower().split())
                labels.add(label)
                if target is not None and target != current_source:
                    claims.add((current_source, label, target))
                    continue
            named = parse_named_relationship(cleaned, name_to_source)
            if named is not None:
                labels.add(named[1])
                claims.add(named)
                continue
            errors.append(
                f"Slide {slide_index} has an unparseable Related claim: {cleaned}."
            )

    invalid_labels = sorted(labels - SUPPORTED_RELATIONSHIPS)
    if invalid_labels:
        errors.append(
            "Relationship labels must be one of "
            + ", ".join(sorted(SUPPORTED_RELATIONSHIPS))
            + f"; found {invalid_labels}."
        )
    return claims


def validate_internal_links(
    scan_body: str,
    deck: Path,
    errors: list[str],
) -> None:
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
            errors.append(f"Internal link does not resolve: {normalized}.")


def markdown_table_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        rows.append(cells)
    return rows


def plain_cell(value: str) -> str:
    return re.sub(r"^(?:\*\*|__)(.*)(?:\*\*|__)$", r"\1", value).strip()


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
    visible_body = strip_comments(scan_body)
    visible_note_fields = sorted(
        {match.group(0).strip() for match in NOTE_ONLY_VISIBLE.finditer(visible_body)}
    )
    if visible_note_fields:
        errors.append(
            "Narrative, questions, relationships, sources, and supporting metadata "
            f"must remain in speaker notes; found visible field(s): {visible_note_fields}."
        )
    for index, slide in enumerate(slides, start=1):
        visible = plain_cell(visible_slide(slide)).lower()
        notes = speaker_notes(slide)
        duplicated_fields: set[str] = set()
        for label in SPEAKER_NOTE_ONLY_FIELDS:
            value = note_field(notes, label)
            for line in (value or "").splitlines():
                candidate = plain_cell(
                    re.sub(r"^\s*[-*+]\s+", "", line)
                ).strip()
                if candidate and candidate.lower() in visible:
                    duplicated_fields.add(label)
        if duplicated_fields:
            errors.append(
                f"Slide {index} duplicates speaker-note-only field content visibly: "
                f"{sorted(duplicated_fields)}."
            )
    placeholders = sorted(set(BRACKET_PLACEHOLDER.findall(body)))
    if placeholders or POSITION_PLACEHOLDER.search(body):
        rendered = placeholders + (
            [POSITION_PLACEHOLDER.search(body).group(0)]
            if POSITION_PLACEHOLDER.search(body)
            else []
        )
        errors.append(
            "Deck contains unreplaced template placeholder(s): "
            + ", ".join(rendered)
            + "."
        )
    remaining_prompts = sorted(prompt for prompt in TEMPLATE_PROMPTS if prompt in body)
    if remaining_prompts:
        errors.append(
            "Deck contains unreplaced template instruction(s): "
            + ", ".join(remaining_prompts)
            + "."
        )

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
        if Path(target).name != target or target != target.lower():
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
        if not (moc.parent / target).is_file():
            errors.append(f"MOC atomic-note link does not resolve: {target}")
            continue
        expected_atomic.add(target)
        coach_target = f"{target[:-3]}.coach.md"
        if (moc.parent / coach_target).is_file():
            expected_coaches.add(coach_target)

    allowed_links = expected_atomic | expected_coaches | {moc.name}
    deck_links = local_markdown_targets(scan_body)
    unexpected_links = sorted(deck_links - allowed_links)
    if unexpected_links:
        errors.append(f"Deck has source links outside the MOC domain: {unexpected_links}.")
    visible_links = sorted(local_markdown_targets(visible_body))
    if visible_links:
        errors.append(
            "MOC, atomic, and coaching source links must appear only in speaker notes: "
            f"{visible_links}."
        )

    if not slides:
        errors.append("Deck must contain at least one slide.")
        opening_notes = ""
    else:
        opening_notes = speaker_notes(slides[0])
        require_note_fields(
            opening_notes,
            ("Narrative", "Domain question", "Source"),
            "Opening slide",
            errors,
        )
        if not re.search(r"^Metadata:\s*$", opening_notes, re.MULTILINE):
            errors.append("Opening slide speaker notes require a 'Metadata' field.")
        require_question(opening_notes, "Domain question", "Opening slide", errors)
        opening_sources = set(
            strict_source_targets(opening_notes, "Opening slide", errors)
        )
        if opening_sources != {moc.name}:
            errors.append(
                f"Opening slide speaker-note Source must link exactly '{moc.name}'."
            )

    moc_tags = tags_from_fields(moc_text)
    domain_tags = moc_tags - RESERVED_TAGS
    deck_tag_fields = field_values(opening_notes, "Tags")
    deck_tags = tags_from_fields(opening_notes)
    if len(deck_tag_fields) != 1:
        errors.append("Opening slide Metadata requires exactly one Tags field.")
    if not domain_tags:
        errors.append("MOC Tags must include at least one domain tag.")
    elif not domain_tags.issubset(deck_tags):
        errors.append(
            f"Deck Tags must include every MOC domain tag: {sorted(domain_tags)}."
        )
    if "slides" not in deck_tags:
        errors.append("Deck Tags must include '#slides'.")
    if len(deck_tags & WORKFLOW_TAGS) != 1:
        errors.append("Deck Tags must include exactly one workflow tag.")
    if len(deck_tags & VISIBILITY_TAGS) != 1:
        errors.append("Deck Tags must include exactly one visibility tag.")

    if len(slides) < len(expected_atomic) + 7:
        errors.append(
            "Domain presentation requires the opening, six system slides, "
            "and one slide per atomic pattern."
        )
    if len(slides) > 30:
        warnings.append(
            f"Deck has {len(slides)} slides; review whether the domain narrative is focused."
        )

    core_locations: list[int] = []
    for title in CORE_SLIDE_TITLES:
        matches = [
            index
            for index, slide in enumerate(slides)
            if (slide_title(slide) or "").lower() == title.lower()
        ]
        if len(matches) != 1:
            errors.append(f"Deck requires exactly one '{title}' slide; found {len(matches)}.")
        else:
            core_locations.append(matches[0])
    if len(core_locations) == len(CORE_SLIDE_TITLES) and core_locations != sorted(
        core_locations
    ):
        errors.append("Required system slides do not follow the template order.")

    system_note_contracts = {
        "Challenges & opportunities": (
            ("Narrative", "Domain question", "Source"),
            ("Domain question",),
        ),
        "Pattern map": (
            ("Narrative", "Domain question", "Source"),
            ("Domain question",),
        ),
        "Apply the patterns together": (
            ("Narrative", "Coach cue", "Source"),
            ("Coach cue",),
        ),
        "What changes": (
            ("Narrative", "Evidence", "Coach cue", "Remaining constraint", "Source"),
            ("Coach cue",),
        ),
        "Pattern map revisited": (
            ("Domain takeaway", "Coach cue", "Source"),
            ("Coach cue",),
        ),
        "Choose one pattern to try": (
            ("Narrative", "Coach cue", "Source"),
            ("Coach cue",),
        ),
    }
    for title, (fields, questions) in system_note_contracts.items():
        match = find_slide(slides, title)
        if match is None:
            continue
        slide_notes = speaker_notes(match[1])
        require_note_fields(slide_notes, fields, title, errors)
        for question in questions:
            require_question(slide_notes, question, title, errors)

    challenge_match = find_slide(slides, "Challenges & opportunities")
    if challenge_match is not None:
        challenge_visible = visible_slide(challenge_match[1])
        if section(challenge_visible, "Challenges") is None:
            errors.append("Challenges & opportunities requires a Challenges section.")
        if section(challenge_visible, "Opportunities") is None:
            errors.append("Challenges & opportunities requires an Opportunities section.")

    pattern_slides: dict[int, tuple[int, str]] = {}
    pattern_names: dict[int, str] = {}
    pattern_clusters: dict[int, str] = {}
    pattern_sources: dict[int, str] = {}
    declared_totals: set[int] = set()
    for index, slide in enumerate(slides, start=1):
        visible = visible_slide(slide)
        headers = list(PATTERN_HEADER.finditer(visible))
        candidates = list(PATTERN_HEADER_CANDIDATE.finditer(visible))
        if candidates and not headers:
            errors.append(
                f"Slide {index} pattern metadata must use '###### p<n> of <N> · <cluster>'."
            )
        if len(headers) > 1:
            errors.append(f"Slide {index} contains more than one pattern header.")
            continue
        if not headers:
            continue

        header = headers[0]
        pattern_id = int(header.group(1))
        declared_totals.add(int(header.group(2)))
        pattern_clusters[pattern_id] = header.group(3).strip()
        if pattern_id in pattern_slides:
            errors.append(f"Pattern ID p{pattern_id} is used more than once.")
        pattern_slides[pattern_id] = (index, slide)

        titles = H1.findall(visible)
        if len(titles) != 1:
            errors.append(f"Pattern slide {index} requires one short-name H1 title.")
        else:
            title = titles[0].strip()
            if re.search(r"\bP\d+\b", title, re.IGNORECASE):
                errors.append(
                    f"Pattern slide {index} title must not expose its internal pattern ID."
                )
            pattern_names[pattern_id] = title

        signals = section(visible, "Use when", level=3)
        signal_count = len(BULLET.findall(signals or ""))
        if not 1 <= signal_count <= 3:
            errors.append(
                f"Pattern slide {index} requires one to three 'Use when' bullets."
            )
        practices = section(visible, "Do", level=3)
        practice_count = len(BULLET.findall(practices or ""))
        if not 1 <= practice_count <= 3:
            errors.append(f"Pattern slide {index} requires one to three 'Do' bullets.")

        slide_notes = speaker_notes(slide)
        require_note_fields(
            slide_notes,
            ("Pattern description", "Coach cue", "Source"),
            f"Pattern slide {index}",
            errors,
        )
        require_question(
            slide_notes, "Coach cue", f"Pattern slide {index}", errors
        )
        description = note_field(slide_notes, "Pattern description") or ""
        description_lines = [line.strip() for line in description.splitlines() if line.strip()]
        if len(description_lines) != 1 or not PATTERN_FORM.fullmatch(
            description_lines[0]
        ):
            errors.append(
                f"Pattern slide {index} speaker notes require one "
                "'When X, do Y, because Z.' Pattern description."
            )
        if any(
            PATTERN_FORM.fullmatch(line.strip())
            for line in visible.splitlines()
            if line.strip()
        ):
            errors.append(
                f"Pattern slide {index} must keep its complete pattern description "
                "in speaker notes."
            )

        source_targets = strict_source_targets(
            slide_notes,
            f"Pattern slide {index}",
            errors,
        )
        atomic_sources = [target for target in source_targets if target in expected_atomic]
        coach_sources = [target for target in source_targets if target in expected_coaches]
        if len(atomic_sources) != 1:
            errors.append(
                f"Pattern slide {index} Source requires exactly one MOC atomic note."
            )
            source = None
        else:
            source = atomic_sources[0]
            pattern_sources[pattern_id] = source
        expected_coach = (
            f"{source[:-3]}.coach.md"
            if source is not None and source.endswith(".md")
            else None
        )
        if expected_coach in expected_coaches:
            if coach_sources != [expected_coach]:
                errors.append(
                    f"Pattern slide {index} Source must link its matching coaching "
                    f"companion '{expected_coach}'."
                )
        elif coach_sources:
            errors.append(
                f"Pattern slide {index} Source must not link a coaching companion "
                "without a matching atomic note."
            )
        expected_source_targets = set(atomic_sources) | set(coach_sources)
        if set(source_targets) != expected_source_targets:
            errors.append(
                f"Pattern slide {index} Source may contain only its atomic note "
                "and matching coaching companion."
            )

        order = tuple(
            label
            for label in ("Pattern description", "Coach cue", "Related", "Source")
            if note_field(slide_notes, label) is not None
        )
        positions = note_field_positions(slide_notes, order)
        if positions != sorted(positions):
            errors.append(
                f"Pattern slide {index} speaker-note fields must follow: "
                "Pattern description, Coach cue, Related, Source."
            )

    expected_ids = list(range(1, len(expected_atomic) + 1))
    if sorted(pattern_slides) != expected_ids:
        errors.append(
            f"Pattern slides must use contiguous internal IDs P1 through "
            f"p{len(expected_atomic)}."
        )
    if declared_totals and declared_totals != {len(expected_atomic)}:
        errors.append(f"Every pattern header must declare of {len(expected_atomic)}.")
    if len({name.lower() for name in pattern_names.values()}) != len(pattern_names):
        errors.append("Pattern slide short names must be unique.")

    mapped_sources = list(pattern_sources.values())
    missing_sources = sorted(expected_atomic - set(mapped_sources))
    extra_sources = sorted(set(mapped_sources) - expected_atomic)
    duplicate_sources = sorted(
        source for source in set(mapped_sources) if mapped_sources.count(source) > 1
    )
    if missing_sources:
        errors.append(f"Deck is missing pattern slides for atomic sources: {missing_sources}.")
    if extra_sources:
        errors.append(f"Deck has pattern sources outside the MOC: {extra_sources}.")
    if duplicate_sources:
        errors.append(
            f"Each atomic source must map to one pattern slide; duplicates: "
            f"{duplicate_sources}."
        )

    source_to_name = {
        source: pattern_names[pattern_id]
        for pattern_id, source in pattern_sources.items()
        if pattern_id in pattern_names
    }
    exact_moc_source_slides = (
        "Challenges & opportunities",
        "Pattern map",
        "Pattern map revisited",
    )
    for title in exact_moc_source_slides:
        match = find_slide(slides, title)
        if match is None:
            continue
        targets = set(
            strict_source_targets(
                speaker_notes(match[1]),
                title,
                errors,
            )
        )
        if targets != {moc.name}:
            errors.append(
                f"{title} speaker-note Source must link exactly '{moc.name}'."
            )

    for title in ("Apply the patterns together", "What changes"):
        match = find_slide(slides, title)
        if match is None:
            continue
        targets = set(
            strict_source_targets(
                speaker_notes(match[1]),
                title,
                errors,
            )
        )
        atomic_sources = targets & expected_atomic
        if (
            moc.name not in targets
            or not atomic_sources
            or targets - ({moc.name} | expected_atomic)
        ):
            errors.append(
                f"{title} speaker-note Source must link the MOC and at least "
                "one relevant atomic note."
            )

    close_source_targets: set[str] = set()
    close_source_match = find_slide(slides, "Choose one pattern to try")
    if close_source_match is not None:
        close_source_targets = set(
            strict_source_targets(
                speaker_notes(close_source_match[1]),
                "Choose one pattern to try",
                errors,
            )
        )
        atomic_sources = close_source_targets & expected_atomic
        coach_sources = close_source_targets & expected_coaches
        expected_linked_coaches = {
            f"{source[:-3]}.coach.md"
            for source in atomic_sources
            if f"{source[:-3]}.coach.md" in expected_coaches
        }
        if (
            not atomic_sources
            or close_source_targets - (expected_atomic | expected_coaches)
            or coach_sources != expected_linked_coaches
        ):
            errors.append(
                "Choose one pattern to try speaker-note Source must link at "
                "least one atomic note and each matching available companion."
            )

    body_without_headers = PATTERN_HEADER.sub("", deck_text)
    body_without_headers = MARKDOWN_LINK_DISPLAY.sub(
        lambda match: match.group(1),
        body_without_headers,
    )
    body_without_headers = WIKI_LINK_DISPLAY.sub(
        lambda match: match.group(2) or match.group(1),
        body_without_headers,
    )
    exposed_ids = sorted(
        set(re.findall(r"\bP(\d+)\b", body_without_headers, re.IGNORECASE))
    )
    if exposed_ids:
        errors.append(
            "Pattern IDs may appear only in H6 position metadata, not in titles, "
            f"Mermaid nodes, tables, or prose: {exposed_ids}."
        )

    for map_title in ("Pattern map", "Pattern map revisited"):
        match = find_slide(slides, map_title)
        if match is None:
            continue
        mermaid = [
            content
            for language, content in fenced_blocks(strip_comments(match[1]))
            if language == "mermaid"
        ]
        if len(mermaid) != 1:
            errors.append(f"{map_title} requires exactly one fenced Mermaid diagram.")
            continue
        labels = {label.lower() for label in mermaid_node_labels(mermaid[0]).values()}
        missing_names = sorted(
            name for name in pattern_names.values() if name.lower() not in labels
        )
        if missing_names:
            errors.append(
                f"{map_title} is missing exact pattern name(s): {missing_names}."
            )
        missing_clusters = sorted(
            cluster
            for cluster in set(pattern_clusters.values())
            if cluster.lower() not in mermaid[0].lower()
        )
        if map_title == "Pattern map" and missing_clusters:
            errors.append(
                f"Pattern map is missing pattern cluster(s): {missing_clusters}."
            )

    apply_slide_match = find_slide(slides, "Apply the patterns together")
    if apply_slide_match is not None:
        apply_slide = apply_slide_match[1]
        apply_visible = visible_slide(apply_slide)
        if section(apply_visible, "Scenario") is not None:
            errors.append(
                "Apply the patterns together requires '## Scenario: <name>', "
                "not a plain Scenario section."
            )
        if not re.search(r"^##\s+Scenario:\s+\S", apply_visible, re.MULTILINE):
            errors.append("Apply the patterns together requires a named Scenario.")
        mermaid = [
            content
            for language, content in fenced_blocks(strip_comments(apply_slide))
            if language == "mermaid"
        ]
        if len(mermaid) != 1:
            errors.append(
                "Apply the patterns together requires exactly one fenced Mermaid flow."
            )
        else:
            labels = {
                label.lower() for label in mermaid_node_labels(mermaid[0]).values()
            }
            source_targets = local_markdown_targets(
                note_field(speaker_notes(apply_slide), "Source") or ""
            )
            missing_names = sorted(
                source_to_name[source]
                for source in source_targets & expected_atomic
                if source in source_to_name
                and source_to_name[source].lower() not in labels
            )
            if missing_names:
                errors.append(
                    "Apply the patterns together Mermaid flow is missing "
                    f"source-linked pattern name(s): {missing_names}."
                )
        for label in ("Start with", "Then", "Watch for"):
            if not re.search(
                rf"^\s*[-*+]\s+\*\*{re.escape(label)}:\*\*\s+\S",
                apply_visible,
                re.MULTILINE | re.IGNORECASE,
            ):
                errors.append(
                    f"Apply the patterns together requires a '{label}' bullet."
                )

    first_map = find_slide(slides, "Pattern map")
    if first_map and apply_slide_match and pattern_slides:
        map_index = first_map[0] + 1
        apply_index = apply_slide_match[0] + 1
        misplaced = sorted(
            pattern_id
            for pattern_id, (index, _slide) in pattern_slides.items()
            if not map_index < index < apply_index
        )
        if misplaced:
            errors.append(
                "Pattern slides must appear between Pattern map and "
                f"Apply the patterns together; misplaced IDs: {misplaced}."
            )

    changes_match = find_slide(slides, "What changes")
    if changes_match is not None:
        changes_visible = visible_slide(changes_match[1])
        if not re.search(
            r"^\|\s*Before\s*\|\s*Pattern\s*\|\s*After\s*\|",
            changes_visible,
            re.MULTILINE | re.IGNORECASE,
        ):
            errors.append("What changes requires a Before | Pattern | After table.")
        else:
            rows = markdown_table_rows(changes_visible)
            invalid_names = sorted(
                {
                    plain_cell(row[1])
                    for row in rows[1:]
                    if len(row) >= 3
                    and plain_cell(row[1]).lower()
                    not in {name.lower() for name in pattern_names.values()}
                }
            )
            if invalid_names:
                errors.append(
                    "What changes Pattern column must use exact pattern short "
                    f"names; found {invalid_names}."
                )

    close_match = find_slide(slides, "Choose one pattern to try")
    if close_match is not None:
        close_visible = visible_slide(close_match[1])
        for label in ("Signal", "Pattern", "Practice", "Review"):
            if not re.search(
                rf"^\s*[-*+]\s+\*\*{label}:\*\*\s+\S",
                close_visible,
                re.MULTILINE | re.IGNORECASE,
            ):
                errors.append(f"Choose one pattern to try requires a '{label}' bullet.")
        pattern_choice = re.search(
            r"^\s*[-*+]\s+\*\*Pattern:\*\*\s+(.+?)\s*$",
            close_visible,
            re.MULTILINE | re.IGNORECASE,
        )
        if pattern_choice is not None:
            chosen_name = pattern_choice.group(1).strip().lower()
            source_by_name = {
                name.lower(): pattern_sources[pattern_id]
                for pattern_id, name in pattern_names.items()
                if pattern_id in pattern_sources
            }
            chosen_source = source_by_name.get(chosen_name)
            if chosen_source is None:
                errors.append(
                    "Choose one pattern to try must name an exact pattern short name."
                )
            else:
                expected_targets = {chosen_source}
                chosen_coach = f"{chosen_source[:-3]}.coach.md"
                if chosen_coach in expected_coaches:
                    expected_targets.add(chosen_coach)
                if close_source_targets != expected_targets:
                    errors.append(
                        "Choose one pattern to try speaker-note Source must match "
                        "the selected pattern and its available companion."
                    )
        if close_match[0] != len(slides) - 1:
            errors.append("Choose one pattern to try must be the final slide.")

    comparison_slides = [
        (index, slide)
        for index, slide in enumerate(slides, start=1)
        if (slide_title(slide) or "").lower().startswith("choosing between ")
    ]
    if len(comparison_slides) > 1:
        errors.append("Deck may contain at most one optional comparison slide.")
    for index, slide in comparison_slides:
        notes = speaker_notes(slide)
        require_note_fields(
            notes,
            ("Selection rule", "Coach cue", "Related", "Source"),
            f"Comparison slide {index}",
            errors,
        )
        require_question(notes, "Coach cue", f"Comparison slide {index}", errors)
        source_targets = strict_source_targets(
            notes,
            f"Comparison slide {index}",
            errors,
        )
        atomic_sources = [target for target in source_targets if target in expected_atomic]
        if len(set(atomic_sources)) != 2 or set(source_targets) != set(atomic_sources):
            errors.append(
                f"Comparison slide {index} Source requires exactly two atomic notes "
                "and no other links."
            )
            continue
        expected_names = {
            source_to_name[source].lower()
            for source in set(atomic_sources)
            if source in source_to_name
        }
        title = slide_title(slide) or ""
        title_match = re.fullmatch(
            r"Choosing between (.+?) and (.+)",
            title,
            re.IGNORECASE,
        )
        title_names = (
            {title_match.group(1).strip().lower(), title_match.group(2).strip().lower()}
            if title_match is not None
            else set()
        )
        if title_names != expected_names:
            errors.append(
                f"Comparison slide {index} title must use its two source-linked "
                "pattern short names."
            )
        rows = markdown_table_rows(visible_slide(slide))
        table_names = {
            plain_cell(row[1]).lower()
            for row in rows[1:]
            if len(row) >= 2
        }
        if table_names != expected_names:
            errors.append(
                f"Comparison slide {index} table must use its two source-linked "
                "pattern short names."
            )

    allowed_slide_indexes = (
        {1}
        | {index + 1 for index in core_locations}
        | {index for index, _slide in pattern_slides.values()}
        | {index for index, _slide in comparison_slides}
    )
    unexpected_slides = [
        index
        for index in range(1, len(slides) + 1)
        if index not in allowed_slide_indexes
    ]
    if unexpected_slides:
        errors.append(
            "Deck contains slide(s) outside the template sequence: "
            f"{unexpected_slides}."
        )

    claims = relationship_claims(
        body,
        slides,
        pattern_sources,
        pattern_names,
        pattern_slides,
        errors,
    )
    allowed_relationships = allowed_deck_relationships(moc.parent, expected_atomic)
    unsupported_relationships = sorted(
        f"{source} --{label}--> {target}"
        for source, label, target in claims - allowed_relationships
    )
    if unsupported_relationships:
        errors.append(
            "Deck claims relationship(s) not permitted by typed, directed "
            f"atomic-note Relationships: {unsupported_relationships}."
        )

    for index, slide in enumerate(slides, start=1):
        visible = visible_slide(slide)
        visible_lines = [line for line in visible.splitlines() if line.strip()]
        bullet_count = len(BULLET.findall(visible))
        if len(visible_lines) > 12:
            warnings.append(
                f"Slide {index} has {len(visible_lines)} visible lines; "
                "review projection density."
            )
        if bullet_count > 6:
            warnings.append(
                f"Slide {index} has {bullet_count} visible bullets; prefer no more than six."
            )

    without_comments = strip_comments(scan_body)
    without_autolinks = AUTOLINK.sub("", without_comments)
    if HTML_TAG.search(without_autolinks):
        errors.append("Arbitrary HTML is not allowed; use Markdown and speaker-note comments.")

    validate_internal_links(scan_body, deck, errors)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    if errors:
        return 1
    print(
        f"Validated {deck.name} against {moc.name}: {len(slides)} slides, "
        f"{len(expected_atomic)} atomic sources, {len(expected_coaches)} coaching sources."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
