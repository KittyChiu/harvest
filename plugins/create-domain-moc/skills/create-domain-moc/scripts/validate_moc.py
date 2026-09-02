#!/usr/bin/env python3
"""Validate one domain Map of Content."""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


H1 = re.compile(r"^#(?!#)\s+(.+?)\s*$", re.MULTILINE)
H2 = re.compile(r"^##(?!#)\s+(.+?)\s*$", re.MULTILINE)
WIKI_LINK = re.compile(r"(?<!!)\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]")
TRANSCLUSION = re.compile(r"!\[\[")
MARKDOWN_LINK = re.compile(
    r"(?<!!)\[[^\]]+\]\(\s*(<?[^)\s>]+>?)\s*(?:[\"'][^)]*[\"'])?\)"
)
MARKDOWN_LINK_WITH_LABEL = re.compile(
    r"(?<!!)\[([^\]]+)\]\(\s*(<?[^)\s>]+>?)\s*(?:[\"'][^)]*[\"'])?\)"
)
WIKI_LINK_WITH_LABEL = re.compile(
    r"(?<!!)\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|([^\]]+))?\]\]"
)
MERMAID_NODE_LABEL = re.compile(
    r"\b[A-Za-z][A-Za-z0-9_-]*\s*\[\s*\"([^\"]+)\"\s*\]"
)
MERMAID_NODE = re.compile(
    r'\b([A-Za-z][A-Za-z0-9_-]*)\s*\[\s*"([^"]+)"\s*\]',
)
MERMAID_ID_TOKEN = re.compile(r"\b([A-Za-z][A-Za-z0-9_-]*)\b")
MERMAID_PIPE_LABEL = re.compile(r"\|\s*\"?([^\"|]+?)\"?\s*\|")
MERMAID_INLINE_LABEL = re.compile(
    r"(?:--|-\.)\s+(.+?)\s+(?:-->|\.->)|"
    r"==\s+(.+?)\s+==>"
)
ATOMIC_RELATIONSHIP_LINE = re.compile(
    r"^\s*[-*+]\s+(?:\*\*)?"
    r"(prerequisite|extension|contrast|example)"
    r"(?:\*\*)?:\s+",
    re.IGNORECASE,
)
TAG = re.compile(r"(?<!\w)#([a-z0-9][a-z0-9-]*)", re.IGNORECASE)
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'-]*")
KEBAB_STEM = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*-moc$")
INTERNAL_FILENAME = re.compile(
    r"^[a-z0-9]+(?:-[a-z0-9]+)*(?:\.(?:coach|marp))?\.md$"
)
WORKFLOW_TAGS = {"draft", "review", "publish"}
VISIBILITY_TAGS = {"private", "public"}
RESERVED_TAGS = WORKFLOW_TAGS | VISIBILITY_TAGS | {"moc", "coaching", "slides"}
SUPPORTED_RELATIONSHIPS = {
    "enables",
    "precedes",
    "informs",
    "complements",
    "contrasts with",
    "depends on",
}
EMPTY_STATE = re.compile(r"\bNo atomic notes yet\.", re.IGNORECASE)
EMPTY_MAP = "No pattern map yet."
EMPTY_WORKFLOW = "No supported domain workflow yet."
REQUIRED_SECTIONS = ("scope", "pattern map", "domain workflow", "notes")
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


def fenced_blocks(text: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    marker: str | None = None
    length = 0
    language = ""
    content: list[str] = []
    for line in text.splitlines():
        if marker is not None:
            if re.fullmatch(rf"\s*{re.escape(marker)}{{{length},}}\s*", line):
                blocks.append((language, "\n".join(content)))
                marker = None
                content = []
            else:
                content.append(line)
            continue
        match = re.match(r"^\s*(`{3,}|~{3,})(.*)$", line)
        if match:
            marker = match.group(1)[0]
            length = len(match.group(1))
            language = match.group(2).strip().lower()
    return blocks


def note_entries(notes: str) -> list[tuple[str, str]]:
    entries: list[tuple[str, str]] = []
    for line in notes.splitlines():
        markdown = MARKDOWN_LINK_WITH_LABEL.search(line)
        if markdown and markdown_link_target(markdown.group(2)) is not None:
            target = normalized_filename(markdown.group(2))
            if target is not None:
                entries.append((markdown.group(1).strip(), target))
            continue
        wiki = WIKI_LINK_WITH_LABEL.search(line)
        if wiki:
            target = normalized_filename(wiki.group(1))
            if target is not None:
                entries.append(
                    ((wiki.group(2) or Path(wiki.group(1)).stem).strip(), target)
                )
    return entries


def allowed_relationships(
    directory: Path,
    targets: set[str],
) -> set[tuple[str, str, str]]:
    allowed: set[tuple[str, str, str]] = set()
    for source in targets:
        path = directory / source
        if not path.is_file():
            continue
        relationships = section_body(
            strip_fenced_blocks(path.read_text(encoding="utf-8")),
            "relationships",
        ) or ""
        for line in relationships.splitlines():
            match = ATOMIC_RELATIONSHIP_LINE.match(line)
            if match is None:
                continue
            relationship_type = match.group(1).lower()
            for _raw, raw_target in internal_links(line):
                target = normalized_filename(raw_target)
                if target not in targets or target == source:
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


def validate_pattern_relationships(
    body: str,
    entries: list[tuple[str, str]],
    allowed: set[tuple[str, str, str]],
    errors: list[str],
) -> None:
    mermaid = [content for language, content in fenced_blocks(body) if language == "mermaid"]
    if len(mermaid) != 1:
        return
    nodes = {}
    for line in mermaid[0].splitlines():
        if line.lstrip().startswith("subgraph "):
            continue
        nodes.update(
            {
                node_id: (label.strip(), dict(entries).get(label.strip()))
                for node_id, label in MERMAID_NODE.findall(line)
            }
        )
    for line in mermaid[0].splitlines():
        node_tokens = [
            token
            for token in MERMAID_ID_TOKEN.finditer(line)
            if token.group(1) in nodes
        ]
        for source_token, target_token in zip(node_tokens, node_tokens[1:]):
            connector = line[source_token.end() : target_token.start()]
            if not re.search(r"[-=.~]{2}", connector):
                continue
            pairs = [(source_token, target_token)]
            if connector.lstrip().startswith("<"):
                pairs = [(target_token, source_token)]
                if ">" in connector:
                    pairs.append((source_token, target_token))
            pipe_label = MERMAID_PIPE_LABEL.search(connector)
            inline_label = MERMAID_INLINE_LABEL.search(connector)
            label_text = (
                pipe_label.group(1)
                if pipe_label is not None
                else next(
                    (
                        group
                        for group in (inline_label.groups() if inline_label else ())
                        if group is not None
                    ),
                    None,
                )
            )
            for directed_source, directed_target in pairs:
                source = nodes[directed_source.group(1)][1]
                target = nodes[directed_target.group(1)][1]
                if source is None or target is None or source == target:
                    continue
                if label_text is None:
                    errors.append(
                        "MOC Pattern map edges between patterns require a supported "
                        f"relationship label: {line.strip()}."
                    )
                    continue
                label = " ".join(label_text.lower().split())
                if label not in SUPPORTED_RELATIONSHIPS:
                    errors.append(
                        f"MOC Pattern map uses unsupported relationship label: {label}."
                    )
                elif (source, label, target) not in allowed:
                    errors.append(
                        "MOC Pattern map relationship is not supported by the atomic "
                        f"notes: {source} --{label}--> {target}."
                    )


def validate_diagram(
    section: str,
    body: str,
    labels: list[str],
    empty_state: str,
    errors: list[str],
    *,
    allow_empty_with_notes: bool = False,
) -> None:
    if not labels:
        if body.strip().lower() != empty_state.lower():
            errors.append(
                f'MOC {section.title()} must be exactly "{empty_state}" '
                "when Notes has no atomic notes."
            )
        return

    if allow_empty_with_notes and body.strip().lower() == empty_state.lower():
        return

    mermaid = [content for language, content in fenced_blocks(body) if language == "mermaid"]
    if len(mermaid) != 1:
        errors.append(
            f"MOC {section.title()} requires exactly one fenced Mermaid diagram "
            "when Notes has atomic notes."
        )
        return
    diagram = mermaid[0]
    if not re.search(r"^\s*(?:flowchart|graph)\s+\S+", diagram, re.MULTILINE):
        errors.append(f"MOC {section.title()} Mermaid diagram must be a flowchart.")
    nodes = [
        label.strip()
        for line in diagram.splitlines()
        if not line.lstrip().startswith("subgraph ")
        for label in MERMAID_NODE_LABEL.findall(line)
    ]
    expected = Counter(labels)
    actual = Counter(nodes)
    missing = sorted((expected - actual).elements())
    if missing:
        errors.append(
            f"MOC {section.title()} is missing exact atomic-note title(s): "
            + ", ".join(missing)
            + "."
        )
    extra = sorted((actual - expected).elements())
    if extra:
        errors.append(
            f"MOC {section.title()} contains pattern node(s) not listed in Notes: "
            + ", ".join(extra)
            + "."
        )


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

    raw_text = args.moc.read_text(encoding="utf-8")
    text = strip_fenced_blocks(raw_text)
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
    elif not note_targets and not re.fullmatch(
        r"No atomic notes yet\.", notes.strip(), re.IGNORECASE
    ):
        errors.append(
            'MOC Notes must contain atomic-note links or exactly '
            '"No atomic notes yet."'
        )

    entries = note_entries(notes)
    labels = [label for label, _target in entries]
    for label, target in entries:
        target_path = args.moc.parent / target
        if not target_path.is_file():
            continue
        titles = H1.findall(
            strip_fenced_blocks(target_path.read_text(encoding="utf-8"))
        )
        if len(titles) != 1:
            errors.append(
                f'MOC atomic note "{target}" requires exactly one level-one title.'
            )
        elif label != titles[0].strip():
            errors.append(
                f'MOC Notes title "{label}" must match atomic-note title '
                f'"{titles[0].strip()}".'
            )
    validate_diagram(
        "pattern map",
        section_body(raw_text, "pattern map") or "",
        labels,
        EMPTY_MAP,
        errors,
    )
    validate_diagram(
        "domain workflow",
        section_body(raw_text, "domain workflow") or "",
        labels,
        EMPTY_WORKFLOW,
        errors,
        allow_empty_with_notes=True,
    )
    validate_pattern_relationships(
        section_body(raw_text, "pattern map") or "",
        entries,
        allowed_relationships(args.moc.parent, set(note_targets)),
        errors,
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
