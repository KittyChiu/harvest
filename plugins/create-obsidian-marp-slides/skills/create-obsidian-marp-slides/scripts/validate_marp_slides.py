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
PATTERN_HEADER = re.compile(
    r"^######\s+PATTERN P(\d+) OF (\d+)\s+·\s+(\S.*?)\s*$",
    re.MULTILINE | re.IGNORECASE,
)
PATTERN_TITLE = re.compile(
    r"^#\s+P(\d+)\s+·\s+(\S.*?)\s*$",
    re.MULTILINE,
)
PATTERN_STATEMENT = re.compile(
    r"^>\s+\*\*When\s+.+,\s*.+,\s*because\s+.+[.!?]\*\*\s*$",
    re.MULTILINE | re.IGNORECASE,
)
BULLET = re.compile(r"^\s*[-*+]\s+\S.*$", re.MULTILINE)
NUMBERED_ITEM = re.compile(r"^\s*(\d+)\.\s+\S.*$", re.MULTILINE)
SUPPORTED_RELATIONSHIPS = {
    "enables",
    "precedes",
    "informs",
    "complements",
    "contrasts with",
    "depends on",
}
RELATED_LINE = re.compile(
    r"^\*\*Related:\*\*\s+P(\d+)\s+·\s+\S.*?"
    r"\s+through\s+\*\*(.+?)\*\*\s*$",
    re.MULTILINE | re.IGNORECASE,
)
MERMAID_EDGE_LABEL = re.compile(
    r'(?:-->|==>)\|\s*"?([^"|]+?)"?\s*\|',
    re.IGNORECASE,
)
TEXT_EDGE_LABEL = re.compile(
    r"--\s*([a-z][a-z ]*?)\s*-->",
    re.IGNORECASE,
)
VERTICAL_EDGE_LABEL = re.compile(
    r"^[ \t]*↓[ \t]+([a-z][a-z ]+?)[ \t]*$",
    re.MULTILINE | re.IGNORECASE,
)
ATOMIC_RELATIONSHIP_LINE = re.compile(
    r"^\s*[-*+]\s+(?:\*\*)?"
    r"(prerequisite|extension|contrast|example)"
    r"(?:\*\*)?:\s+",
    re.IGNORECASE,
)
MERMAID_RELATIONSHIP = re.compile(
    r'(?=\bP(\d+)\b[^\n]*?(?:-->|==>)\|\s*"?([^"|]+?)"?'
    r"\s*\|\s*P(\d+)\b)",
    re.IGNORECASE,
)
TEXT_RELATIONSHIP = re.compile(
    r"(?=\bP(\d+)\b[^\n]*?--\s*([a-z][a-z ]*?)\s*-->\s*P(\d+)\b)",
    re.IGNORECASE,
)
VERTICAL_RELATIONSHIP = re.compile(
    r"(?=^[ \t]*P(\d+)\b.*\n"
    r"[ \t]*↓[ \t]+([a-z][a-z ]+?)[ \t]*\n"
    r"[ \t]*P(\d+)\b)",
    re.MULTILINE | re.IGNORECASE,
)
NAMED_PATTERN_REFERENCE = re.compile(
    r"\bP(\d+)\s+·\s+([^|\]\n\"*]+?)"
    r"(?=\s+through\s+\*\*|\s+--|[|\]\n\"*]|$)"
)
CORE_SLIDE_TITLES = (
    "Challenges & opportunities",
    "Pattern map",
    "Apply the patterns together",
    "What changes",
    "Pattern map revisited",
    "Choose one pattern to try",
)
TEMPLATE_PLACEHOLDER = re.compile(
    r"\[(?:"
    r"Domain name|One-line domain promise|"
    r"Describe the outcome this domain helps people achieve\.|"
    r"Recurring challenge|Practical consequence|"
    r"Limitation of the current approach|Potential improvement|"
    r"Capability the domain can enable|Value of connecting the patterns|"
    r"What do the patterns collectively help answer\?|"
    r"Cluster \d+|Pattern name|N|CLUSTER|Short pattern name|"
    r"condition|action|mechanism|Observable signal|Recurring situation|"
    r"Concrete action|Optional concrete action|relationship|"
    r"One question that helps the audience discover or apply the pattern\.|"
    r"Realistic situation|Observed signal|Expected outcome|"
    r"First practice|Next practice|Constraint or failure condition|"
    r"Current behaviour|Improved behaviour|"
    r"What these patterns do not solve\.|"
    r"Explain how the patterns work as a system\.|Something observable|"
    r"One small action|How the result will be discussed"
    r")\]",
    re.IGNORECASE,
)
EMPTY_PATTERN_CHOICE = re.compile(r"\bP\[\s*\]")
TEMPLATE_PROMPTS = (
    "Use the domain MOC, atomic pattern notes, and coaching companions.",
    "Repeat one slide for each pattern.",
    "Optional: use when two patterns are alternatives.",
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
    if not match:
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
        if fence_match:
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


def strip_fenced_blocks(text: str) -> str:
    visible_lines: list[str] = []
    fence: tuple[str, int] | None = None
    for line in text.splitlines():
        if fence is not None:
            if closes_fence(line, *fence):
                fence = None
            visible_lines.append("")
            continue
        fence_match = opening_fence(line)
        if fence_match:
            fence = fence_match[0], fence_match[1]
            visible_lines.append("")
            continue
        visible_lines.append(line)
    return "\n".join(visible_lines)


def fenced_languages(text: str) -> list[str]:
    languages: list[str] = []
    fence: tuple[str, int] | None = None
    for line in text.splitlines():
        if fence is not None:
            if closes_fence(line, *fence):
                fence = None
            continue
        match = opening_fence(line)
        if match:
            fence = match[0], match[1]
            languages.append(match[2].split(maxsplit=1)[0].lower() if match[2] else "")
    return languages


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


def strip_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


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


def source_target_list(text: str, field_name: str) -> list[str]:
    return [
        normalize_target(target)
        for value in field_values(text, field_name)
        for target in link_targets(value)
        if normalize_target(target)
    ]


def visible_slide(slide: str) -> str:
    return strip_comments(strip_fenced_blocks(slide))


def slide_title(slide: str) -> str | None:
    match = re.search(r"^#(?!#)\s+(.+?)\s*$", visible_slide(slide), re.MULTILINE)
    return match.group(1).strip() if match else None


def find_slide(slides: list[str], title: str) -> tuple[int, str] | None:
    for index, slide in enumerate(slides):
        if (slide_title(slide) or "").lower() == title.lower():
            return index, slide
    return None


def relationship_labels(text: str) -> list[str]:
    labels = [match.group(2).strip().lower() for match in RELATED_LINE.finditer(text)]
    labels.extend(
        match.group(1).strip().lower()
        for match in MERMAID_EDGE_LABEL.finditer(text)
    )
    labels.extend(
        match.group(1).strip().lower()
        for match in TEXT_EDGE_LABEL.finditer(text)
    )
    labels.extend(
        match.group(1).strip().lower()
        for match in VERTICAL_EDGE_LABEL.finditer(text)
    )
    return labels


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


def deck_relationship_claims(
    body: str,
    pattern_sources: dict[int, str],
    pattern_slides: dict[int, tuple[int, str]],
) -> set[tuple[str, str, str]]:
    id_claims: set[tuple[int, str, int]] = set()
    for pattern in (MERMAID_RELATIONSHIP, TEXT_RELATIONSHIP, VERTICAL_RELATIONSHIP):
        for match in pattern.finditer(strip_comments(body)):
            source_id = int(match.group(1))
            label = match.group(2).strip().lower()
            target_id = int(match.group(3))
            if source_id != target_id:
                id_claims.add((source_id, label, target_id))
    for pattern_id, (_index, slide) in pattern_slides.items():
        for line in visible_slide(slide).splitlines():
            match = RELATED_LINE.fullmatch(line.strip())
            if match is None:
                continue
            target_id = int(match.group(1))
            label = match.group(2).strip().lower()
            if pattern_id != target_id:
                id_claims.add((pattern_id, label, target_id))

    claims: set[tuple[str, str, str]] = set()
    for source_id, label, target_id in id_claims:
        if source_id in pattern_sources and target_id in pattern_sources:
            claims.add(
                (
                    pattern_sources[source_id],
                    label,
                    pattern_sources[target_id],
                )
            )
    return claims


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
    contract_body = strip_comments(scan_body)

    placeholders = sorted(set(TEMPLATE_PLACEHOLDER.findall(body)))
    if placeholders or EMPTY_PATTERN_CHOICE.search(body):
        rendered = placeholders + (["P[ ]"] if EMPTY_PATTERN_CHOICE.search(body) else [])
        errors.append(
            "Deck contains unreplaced template placeholder(s): "
            + ", ".join(rendered)
            + "."
        )
    remaining_prompts = sorted(
        prompt for prompt in TEMPLATE_PROMPTS if prompt in body
    )
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

    moc_values = field_values(contract_body, "MOC")
    moc_links = source_targets(contract_body, "MOC")
    expected_moc = {moc.name}
    opening_moc_links = (
        source_targets(visible_slide(slides[0]), "MOC") if slides else set()
    )
    if (
        len(moc_values) != 1
        or moc_links != expected_moc
        or opening_moc_links != expected_moc
    ):
        errors.append(
            f"Opening slide must contain the only MOC field linking exactly '{moc.name}'; "
            f"found {len(moc_values)} fields and links {sorted(moc_links)}."
        )

    deck_source_list = source_target_list(contract_body, "Source")
    deck_sources = set(deck_source_list)
    if deck_sources != expected_atomic:
        missing = sorted(expected_atomic - deck_sources)
        extra = sorted(deck_sources - expected_atomic)
        if missing:
            errors.append(f"Deck is missing atomic Source links: {missing}.")
        if extra:
            errors.append(f"Deck has Source links outside the MOC: {extra}.")
    duplicate_sources = sorted(
        source for source in deck_sources if deck_source_list.count(source) > 1
    )
    if duplicate_sources:
        errors.append(
            f"Each atomic Source must appear exactly once; duplicates: {duplicate_sources}."
        )

    deck_coach_list = source_target_list(contract_body, "Coach")
    deck_coaches = set(deck_coach_list)
    if deck_coaches != expected_coaches:
        missing = sorted(expected_coaches - deck_coaches)
        extra = sorted(deck_coaches - expected_coaches)
        if missing:
            errors.append(f"Deck is missing available Coach links: {missing}.")
        if extra:
            errors.append(f"Deck has unexpected Coach links: {extra}.")
    duplicate_coaches = sorted(
        coach for coach in deck_coaches if deck_coach_list.count(coach) > 1
    )
    if duplicate_coaches:
        errors.append(
            f"Each Coach link must appear exactly once; duplicates: {duplicate_coaches}."
        )

    moc_tags = tags_from_fields(moc_text)
    domain_tags = moc_tags - RESERVED_TAGS
    deck_tags = tags_from_fields(contract_body)
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
            errors.append(
                f"Deck requires exactly one '{title}' slide; found {len(matches)}."
            )
        else:
            core_locations.append(matches[0])
    if len(core_locations) == len(CORE_SLIDE_TITLES) and core_locations != sorted(
        core_locations
    ):
        errors.append("Required system slides do not follow the template order.")

    challenge_match = find_slide(slides, "Challenges & opportunities")
    if challenge_match:
        _index, challenge_slide = challenge_match
        challenge_visible = visible_slide(challenge_slide)
        if section(challenge_visible, "Challenges") is None:
            errors.append("Challenges & opportunities requires a Challenges section.")
        if section(challenge_visible, "Opportunities") is None:
            errors.append("Challenges & opportunities requires an Opportunities section.")
        domain_question = re.search(
            r"^\s*>\s+\*\*Domain question:\*\*\s+(.+?)\s*$",
            challenge_visible,
            re.MULTILINE | re.IGNORECASE,
        )
        if domain_question is None or not domain_question.group(1).endswith("?"):
            errors.append(
                "Challenges & opportunities requires a Domain question ending in ?."
            )

    for title in ("Pattern map", "Pattern map revisited"):
        map_match = find_slide(slides, title)
        if map_match:
            _index, map_slide = map_match
            if not {"mermaid", "text"} & set(fenced_languages(map_slide)):
                errors.append(
                    f"{title} requires a fenced mermaid or text system map."
                )

    pattern_slides: dict[int, tuple[int, str]] = {}
    pattern_names: dict[int, str] = {}
    pattern_clusters: dict[int, str] = {}
    pattern_sources: dict[int, str] = {}
    declared_totals: set[int] = set()
    for index, slide in enumerate(slides, start=1):
        visible = visible_slide(slide)
        headers = list(PATTERN_HEADER.finditer(visible))
        if len(headers) > 1:
            errors.append(f"Slide {index} contains more than one pattern header.")
            continue
        source_list = source_target_list(visible, "Source")
        coach_list = source_target_list(visible, "Coach")
        if not headers:
            if source_list:
                errors.append(
                    f"Slide {index} has a Source but is not a PATTERN Pn OF N slide."
                )
            if coach_list:
                errors.append(
                    f"Slide {index} has a Coach link but is not a pattern slide."
                )
            continue

        header = headers[0]
        pattern_id = int(header.group(1))
        declared_totals.add(int(header.group(2)))
        pattern_clusters[pattern_id] = header.group(3).strip()
        if pattern_id in pattern_slides:
            errors.append(f"Pattern ID P{pattern_id} is used more than once.")
        pattern_slides[pattern_id] = (index, slide)

        titles = list(PATTERN_TITLE.finditer(visible))
        if len(titles) != 1 or int(titles[0].group(1)) != pattern_id:
            errors.append(
                f"Pattern slide {index} requires one '# P{pattern_id} · <short name>' title."
            )
        else:
            pattern_names[pattern_id] = titles[0].group(2).strip()
        statements = PATTERN_STATEMENT.findall(visible)
        if len(statements) != 1:
            errors.append(
                f"Pattern slide {index} requires one bold "
                "'When X, do Y, because Z.' statement."
            )

        signals = section(visible, "Use it when")
        if signals is None or not BULLET.search(signals):
            errors.append(
                f"Pattern slide {index} requires Use it when with at least one bullet."
            )
        practices = section(visible, "Practices")
        practice_numbers = [
            int(match.group(1)) for match in NUMBERED_ITEM.finditer(practices or "")
        ]
        if (
            practices is None
            or not 1 <= len(practice_numbers) <= 3
            or practice_numbers != list(range(1, len(practice_numbers) + 1))
        ):
            errors.append(
                f"Pattern slide {index} requires one to three contiguous numbered practices."
            )
        if len(source_list) != 1:
            errors.append(f"Pattern slide {index} requires exactly one Source link.")
            source = None
        else:
            source = source_list[0]
            pattern_sources[pattern_id] = source
        expected_coach = (
            f"{source[:-3]}.coach.md"
            if source is not None and source.endswith(".md")
            else None
        )
        if expected_coach in expected_coaches:
            if coach_list != [expected_coach]:
                errors.append(
                    f"Pattern slide {index} must link its matching Coach "
                    f"'{expected_coach}'."
                )
        elif coach_list:
            errors.append(
                f"Pattern slide {index} must not declare a Coach without "
                "a matching companion."
            )

        related_lines = [
            line for line in visible.splitlines()
            if line.strip().lower().startswith("**related")
        ]
        if related_lines and (
            len(related_lines) != 1
            or RELATED_LINE.fullmatch(related_lines[0].strip()) is None
        ):
            errors.append(
                f"Pattern slide {index} has an invalid Related relationship."
            )

        if coach_list:
            note_blocks = re.findall(r"<!--(.*?)-->", slide, re.DOTALL)
            coaching_questions = [
                match.group(1).strip()
                for block in note_blocks
                for match in re.finditer(
                    r"^\s*Coach cue:\s*(\S.*?)\s*$",
                    block,
                    re.MULTILINE,
                )
            ]
            if len(coaching_questions) != 1 or not coaching_questions[0].endswith("?"):
                errors.append(
                    f"Pattern slide {index} with Coach requires one "
                    "Coach cue question ending in ?."
                )

    expected_ids = list(range(1, len(expected_atomic) + 1))
    if sorted(pattern_slides) != expected_ids:
        errors.append(
            f"Pattern slides must use contiguous IDs P1 through P{len(expected_atomic)}."
        )
    if declared_totals and declared_totals != {len(expected_atomic)}:
        errors.append(
            f"Every pattern header must declare OF {len(expected_atomic)}."
        )

    expected_id_set = set(expected_ids)
    referenced_ids = {
        int(value)
        for value in re.findall(r"\bP(\d+)\b", strip_comments(body))
    }
    unknown_ids = sorted(referenced_ids - expected_id_set)
    if unknown_ids:
        errors.append(f"Deck references unknown pattern ID(s): {unknown_ids}.")
    mismatched_names: list[str] = []
    for match in NAMED_PATTERN_REFERENCE.finditer(strip_comments(body)):
        pattern_id = int(match.group(1))
        actual_name = match.group(2).strip()
        expected_name = pattern_names.get(pattern_id)
        if expected_name is not None and actual_name.lower() != expected_name.lower():
            mismatched_names.append(
                f"P{pattern_id} · {actual_name} (expected {expected_name})"
            )
    if mismatched_names:
        errors.append(
            "Deck has inconsistent pattern name reference(s): "
            + ", ".join(sorted(set(mismatched_names)))
            + "."
        )

    for map_title in ("Pattern map", "Pattern map revisited"):
        map_match = find_slide(slides, map_title)
        if map_match:
            _index, map_slide = map_match
            missing_ids = [
                f"P{pattern_id}"
                for pattern_id in expected_ids
                if not re.search(rf"\bP{pattern_id}\b", map_slide)
            ]
            if missing_ids:
                errors.append(
                    f"{map_title} is missing pattern ID(s): {missing_ids}."
                )
            inconsistent_names = [
                f"P{pattern_id} · {name}"
                for pattern_id, name in pattern_names.items()
                if not re.search(
                    rf"\bP{pattern_id}\s+·\s+{re.escape(name)}\b",
                    map_slide,
                    re.IGNORECASE,
                )
            ]
            if inconsistent_names:
                errors.append(
                    f"{map_title} is missing exact pattern name(s): "
                    f"{inconsistent_names}."
                )
    pattern_map_match = find_slide(slides, "Pattern map")
    if pattern_map_match:
        _index, pattern_map_slide = pattern_map_match
        missing_clusters = sorted(
            {
                cluster
                for cluster in pattern_clusters.values()
                if cluster.lower() not in pattern_map_slide.lower()
            }
        )
        if missing_clusters:
            errors.append(
                f"Pattern map is missing pattern cluster(s): {missing_clusters}."
            )

    first_map = find_slide(slides, "Pattern map")
    apply_slide_match = find_slide(slides, "Apply the patterns together")
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
                f"Pattern slides must appear between Pattern map and "
                f"Apply the patterns together; misplaced IDs: {misplaced}."
            )
    close_slide_match = find_slide(slides, "Choose one pattern to try")
    if close_slide_match and close_slide_match[0] != len(slides) - 1:
        errors.append("Choose one pattern to try must be the final slide.")

    invalid_relationships = sorted(
        {
            label
            for label in relationship_labels(body)
            if label not in SUPPORTED_RELATIONSHIPS
        }
    )
    if invalid_relationships:
        errors.append(
            "Relationship labels must be one of "
            + ", ".join(sorted(SUPPORTED_RELATIONSHIPS))
            + f"; found {invalid_relationships}."
        )
    allowed_relationships = allowed_deck_relationships(
        moc.parent,
        expected_atomic,
    )
    claimed_relationships = deck_relationship_claims(
        body,
        pattern_sources,
        pattern_slides,
    )
    unsupported_relationships = sorted(
        f"{source} --{label}--> {target}"
        for source, label, target in (
            claimed_relationships - allowed_relationships
        )
    )
    if unsupported_relationships:
        errors.append(
            "Deck claims relationship(s) not permitted by typed, directed "
            f"atomic-note Relationships: {unsupported_relationships}."
        )

    apply_match = apply_slide_match
    if apply_match:
        _index, apply_slide = apply_match
        apply_visible = visible_slide(apply_slide)
        if not re.search(r"^##\s+Scenario:\s+\S", apply_visible, re.MULTILINE):
            errors.append("Apply the patterns together requires a named Scenario.")
        for label in ("Start with", "Then", "Watch for"):
            if not re.search(
                rf"^\s*[-*+]\s+\*\*{re.escape(label)}:\*\*\s+\S",
                apply_visible,
                re.MULTILINE | re.IGNORECASE,
            ):
                errors.append(
                    f"Apply the patterns together requires a '{label}' bullet."
                )

    changes_match = find_slide(slides, "What changes")
    if changes_match:
        _index, changes_slide = changes_match
        changes_visible = visible_slide(changes_slide)
        if not re.search(
            r"^\|\s*Before\s*\|\s*Pattern\s*\|\s*After\s*\|",
            changes_visible,
            re.MULTILINE | re.IGNORECASE,
        ):
            errors.append("What changes requires a Before | Pattern | After table.")
        if not re.search(
            r"^\s*>\s+\*\*Remaining constraint:\*\*\s+\S",
            changes_visible,
            re.MULTILINE | re.IGNORECASE,
        ):
            errors.append("What changes requires a Remaining constraint.")

    close_match = find_slide(slides, "Choose one pattern to try")
    if close_match:
        _index, close_slide = close_match
        close_visible = visible_slide(close_slide)
        for label in ("Signal", "Pattern", "Practice", "Review"):
            if not re.search(
                rf"^\s*[-*+]\s+\*\*{label}:\*\*\s+\S",
                close_visible,
                re.MULTILINE | re.IGNORECASE,
            ):
                errors.append(
                    f"Choose one pattern to try requires a '{label}' bullet."
                )

    for index, slide in enumerate(slides, start=1):
        visible = re.sub(r"<!--.*?-->", "", slide, flags=re.DOTALL).strip()
        visible_lines = [line for line in visible.splitlines() if line.strip()]
        if len(visible_lines) > 12:
            warnings.append(
                f"Slide {index} has {len(visible_lines)} visible lines; review projection density."
            )

    without_comments = strip_comments(scan_body)
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
