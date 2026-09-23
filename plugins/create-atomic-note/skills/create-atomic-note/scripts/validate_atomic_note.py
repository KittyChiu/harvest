#!/usr/bin/env python3
"""Validate an atomic note and its domain Map of Content."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
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
INLINE_TAG = re.compile(r"(?<!\w)#([a-z0-9][a-z0-9-]*)", re.IGNORECASE)
WORD = re.compile(r"[A-Za-z0-9][A-Za-z0-9'-]*")
WORKFLOW_TAGS = {"draft", "review", "publish"}
VISIBILITY_TAGS = {"private", "public"}
RESERVED_TAGS = WORKFLOW_TAGS | VISIBILITY_TAGS | {"moc", "coaching", "slides"}
REQUIRED_SECTIONS = (
    "pattern",
    "practice",
    "why it works",
    "signals",
    "learning",
    "constraints",
    "relationships",
)
ACTION_SECTIONS = ("practice", "signals", "constraints")
KEBAB_STEM = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
INTERNAL_FILENAME = re.compile(
    r"^[a-z0-9]+(?:-[a-z0-9]+)*(?:\.(?:coach|marp))?\.md$"
)
EMPTY_MOC = re.compile(r"\bNo atomic notes yet\.", re.IGNORECASE)
EMPTY_WORKFLOW = "No supported domain workflow yet."
PATTERN_FORM = re.compile(
    r"^When\b.+,\s*.+,\s*because\b.+[.!?]$", re.IGNORECASE
)
BULLET = re.compile(r"^\s*[-*+]\s+\S", re.MULTILINE)
TYPED_RELATIONSHIP = re.compile(
    r"^\s*[-*+]\s+(?:\*\*)?"
    r"(?:prerequisite|extension|contrast|example)"
    r"(?:\*\*)?:\s+",
    re.IGNORECASE,
)
NO_RELATIONSHIPS = re.compile(
    r"\bno supported relationships?(?: exist)?(?: yet)?\b", re.IGNORECASE
)
OKF_TYPE = "Reusable Pattern"
OKF_REQUIRED_FIELDS = {
    "type",
    "title",
    "description",
    "tags",
    "status",
    "sources",
    "generated",
}
TOP_LEVEL_YAML_FIELD = re.compile(r"^([a-z][a-z0-9_-]*):(?:\s*(.*))?$")
NESTED_YAML_FIELD = re.compile(r"^\s{2,}([a-z][a-z0-9_-]*):(?:\s*(.*))?$")
SEQUENCE_YAML_FIELD = re.compile(
    r"^\s{2}-\s+([a-z][a-z0-9_-]*):(?:\s*(.*))?$"
)
YAML_LIST_ITEM = re.compile(r"^\s{2}-\s+(.+?)\s*$")
ACTOR = re.compile(
    r"^(?:human:[A-Za-z0-9][A-Za-z0-9._-]*"
    r"|process:[A-Za-z0-9][A-Za-z0-9._-]*"
    r"|[A-Za-z0-9][A-Za-z0-9._-]*/[A-Za-z0-9][A-Za-z0-9._-]*)$"
)
SOURCE_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ANGLE_PLACEHOLDER = re.compile(r"<[^>]+>")
SOURCE_ATTRIBUTION = re.compile(
    r"^\s*(?:[-*+]\s+|#{1,6}\s+)?"
    r"(?:\*\*|__)?(?:sources?|references?|citations?|attributions?|based on)"
    r"(?:(?:\*\*|__)?:|:(?:\*\*|__)?)"
    r"(?:\s|\Z)",
    re.MULTILINE | re.IGNORECASE,
)
SOURCE_HEADING = re.compile(
    r"^#{1,6}\s+(?:\*\*|__)?"
    r"(?:sources?|references?|citations?|attributions?|based on)"
    r"(?:\*\*|__)?\s*$",
    re.MULTILINE | re.IGNORECASE,
)
EXTERNAL_SOURCE_URL = re.compile(
    r"(?<![\w.-])(?:https?://|www\.)[^\s<>()]+",
    re.IGNORECASE,
)
MOC_SOURCE_ATTRIBUTION = re.compile(
    r"\b(?:source|attribution|references?|citations?|based on)\s*:"
    r"|\b(?:based on|derived from)\s+(?:an?\s+|the\s+)?"
    r"(?:customer|client|team|interview|meeting|transcript|article|report)\b",
    re.IGNORECASE,
)
TEMPLATE_PROMPTS = {
    'title: "<Pattern title>"',
    'description: "<One-sentence decision summary>"',
    "  - <domain-tag>",
    '    resource: "<Approved URI, bundle path, or non-identifying scope descriptor>"',
    '    title: "<De-identified source label>"',
    '  at: "<Generation timestamp with UTC offset>"',
    '    by: "<Verifier actor; remove the verified field when not confirmed>"',
    '    at: "<Verification timestamp; remove the verified field when not confirmed>"',
    'stale_after: "<Expiration timestamp; remove when no evidence-backed expiry exists>"',
    "# Pattern title",
    "State the reusable rule in a single sentence.",
    "Use:",
    "> When X, do Y, because Z.",
    "A reader should understand the idea after reading it once.",
    "Describe the smallest set of actions needed to apply the pattern.",
    "- Use concrete, observable behaviours.",
    "- Keep the list short.",
    "- Prefer actions over advice.",
    "Explain the mechanism.",
    "Describe the cause-and-effect that makes the pattern effective.",
    "Apply this pattern when:",
    "- Observable symptom",
    "- Recurring situation",
    "- Trigger condition",
    "- Common failure mode",
    "Record the de-identified observation, experience, failure, or analysis that led to discovering this pattern.",
    "Write what was learned, not what should be done.",
    "Replace customer, organization, and team names with neutral roles.",
    "Keep source identities and sensitive details out of the body.",
    "- When the pattern does not apply.",
    "- Trade-offs, assumptions, or costs.",
    "- Conditions that would make the pattern ineffective.",
    "- Prerequisite:",
    "- Extension:",
    "- Contrast:",
    "- Example:",
    "Only include supported relationships.",
    "If none exist yet, state that explicitly.",
}


@dataclass(frozen=True)
class FrontmatterField:
    value: str
    lines: tuple[str, ...]


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


def split_frontmatter(
    text: str, errors: list[str]
) -> tuple[dict[str, FrontmatterField], str]:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        errors.append("Atomic note must start with YAML frontmatter.")
        return {}, text
    try:
        end = lines.index("---", 1)
    except ValueError:
        errors.append("Atomic note YAML frontmatter is not closed.")
        return {}, text

    fields: dict[str, FrontmatterField] = {}
    field_lines: dict[str, list[str]] = {}
    current: str | None = None
    values: dict[str, str] = {}
    for line in lines[1:end]:
        if "\t" in line:
            errors.append("Atomic note YAML frontmatter must use spaces, not tabs.")
            continue
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[0].isspace():
            if current is None:
                errors.append(
                    "Atomic note YAML frontmatter has nested content without a field."
                )
            else:
                field_lines[current].append(line)
            continue
        match = TOP_LEVEL_YAML_FIELD.fullmatch(line)
        if match is None:
            errors.append(f"Atomic note has invalid YAML frontmatter line: {line}")
            current = None
            continue
        current = match.group(1)
        if current in values:
            errors.append(f'Atomic note repeats frontmatter field "{current}".')
            current = None
            continue
        values[current] = (match.group(2) or "").strip()
        field_lines[current] = []

    for name, value in values.items():
        fields[name] = FrontmatterField(value, tuple(field_lines[name]))
    body = "\n".join(lines[end + 1 :]).lstrip("\n")
    return fields, body


def yaml_scalar(value: str, label: str, errors: list[str]) -> str:
    value = value.strip()
    if not value:
        errors.append(f"{label} must not be empty.")
        return ""
    if value.startswith('"'):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            errors.append(f"{label} has an invalid quoted YAML string.")
            return ""
        if not isinstance(parsed, str):
            errors.append(f"{label} must be a string.")
            return ""
        return parsed
    if value.startswith("'"):
        if len(value) < 2 or not value.endswith("'"):
            errors.append(f"{label} has an invalid quoted YAML string.")
            return ""
        return value[1:-1].replace("''", "'")
    return value


def scalar_field(
    fields: dict[str, FrontmatterField],
    name: str,
    errors: list[str],
) -> str:
    item = fields.get(name)
    label = f'Atomic-note frontmatter "{name}"'
    if item is None:
        return ""
    if item.lines:
        errors.append(f"{label} must be a scalar value.")
    value = yaml_scalar(item.value, label, errors)
    if ANGLE_PLACEHOLDER.search(value):
        errors.append(f"{label} contains an unreplaced placeholder.")
    return value


def yaml_list(
    item: FrontmatterField | None,
    label: str,
    errors: list[str],
) -> list[str]:
    if item is None:
        return []
    raw_values: list[str] = []
    if item.value:
        if item.lines or not (
            item.value.startswith("[") and item.value.endswith("]")
        ):
            errors.append(f"{label} must be a YAML list.")
            return []
        contents = item.value[1:-1].strip()
        raw_values = [] if not contents else contents.split(",")
    else:
        for line in item.lines:
            match = YAML_LIST_ITEM.fullmatch(line)
            if match is None:
                errors.append(f"{label} must contain only YAML list items.")
                continue
            raw_values.append(match.group(1))

    values = [
        yaml_scalar(value, f"{label} item", errors)
        for value in raw_values
    ]
    return [value for value in values if value]


def nested_mapping(
    item: FrontmatterField | None,
    label: str,
    errors: list[str],
) -> dict[str, str]:
    if item is None:
        return {}
    if item.value:
        errors.append(f"{label} must use an indented YAML mapping.")
        return {}
    result: dict[str, str] = {}
    for line in item.lines:
        match = NESTED_YAML_FIELD.fullmatch(line)
        if match is None or SEQUENCE_YAML_FIELD.fullmatch(line):
            errors.append(f"{label} must contain only YAML mapping fields.")
            continue
        name = match.group(1)
        if name in result:
            errors.append(f'{label} repeats field "{name}".')
            continue
        result[name] = yaml_scalar(
            (match.group(2) or "").strip(),
            f'{label} field "{name}"',
            errors,
        )
    return result


def mapping_sequence(
    item: FrontmatterField | None,
    label: str,
    errors: list[str],
) -> list[dict[str, str]]:
    if item is None:
        return []
    if item.value:
        errors.append(f"{label} must use an indented YAML sequence.")
        return []
    result: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in item.lines:
        first = SEQUENCE_YAML_FIELD.fullmatch(line)
        nested = NESTED_YAML_FIELD.fullmatch(line)
        if first:
            current = {}
            result.append(current)
            name = first.group(1)
            value = first.group(2) or ""
        elif nested and current is not None:
            name = nested.group(1)
            value = nested.group(2) or ""
        else:
            errors.append(f"{label} must contain only YAML mapping items.")
            continue
        if name in current:
            errors.append(f'{label} item repeats field "{name}".')
            continue
        current[name] = yaml_scalar(
            value.strip(), f'{label} field "{name}"', errors
        )
        if ANGLE_PLACEHOLDER.search(current[name]):
            errors.append(f'{label} field "{name}" contains an unreplaced placeholder.')
    return result


def parse_timestamp(value: str, label: str, errors: list[str]) -> datetime | None:
    if not value:
        return None
    try:
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        errors.append(f"{label} must be an ISO 8601 datetime with a UTC offset.")
        return None
    if timestamp.tzinfo is None or timestamp.utcoffset() is None:
        errors.append(f"{label} must be an ISO 8601 datetime with a UTC offset.")
        return None
    return timestamp


def validate_actor(value: str, label: str, errors: list[str]) -> None:
    if value and not ACTOR.fullmatch(value):
        errors.append(
            f"{label} must use producer/version, human:<id>, or process:<id>."
        )


def validate_okf_metadata(
    fields: dict[str, FrontmatterField],
    note_title: str,
    errors: list[str],
) -> None:
    missing = sorted(OKF_REQUIRED_FIELDS - fields.keys())
    if missing:
        errors.append(
            "Atomic note is missing required OKF frontmatter field(s): "
            + ", ".join(missing)
            + "."
        )

    concept_type = scalar_field(fields, "type", errors)
    if concept_type and concept_type != OKF_TYPE:
        errors.append(f'Atomic-note type must be "{OKF_TYPE}".')

    title = scalar_field(fields, "title", errors)
    if title and note_title and title != note_title:
        errors.append("Atomic-note frontmatter title must match the H1 title exactly.")

    description = scalar_field(fields, "description", errors)
    if description and (
        "\n" in description or len(re.findall(r"[.!?]", description)) != 1
    ):
        errors.append("Atomic-note description must be one sentence.")

    tags = yaml_list(fields.get("tags"), "Atomic-note tags", errors)
    normalized_tags = [tag.lower() for tag in tags]
    invalid_tags = sorted(
        {
            tag
            for tag in normalized_tags
            if tag.startswith("#") or not KEBAB_STEM.fullmatch(tag)
        }
    )
    if invalid_tags:
        errors.append(
            "Atomic-note tags must be lowercase kebab-case values without #: "
            + ", ".join(invalid_tags)
            + "."
        )
    if len(normalized_tags) != len(set(normalized_tags)):
        errors.append("Atomic-note tags must not contain duplicates.")
    tag_set = set(normalized_tags)
    if len(tag_set & WORKFLOW_TAGS) != 1:
        errors.append(
            "Atomic-note tags must include exactly one workflow value: "
            "draft, review, or publish."
        )
    if len(tag_set & VISIBILITY_TAGS) != 1:
        errors.append(
            "Atomic-note tags must include exactly one visibility value: "
            "private or public."
        )
    if not tag_set - RESERVED_TAGS:
        errors.append("Atomic-note tags must include at least one domain value.")

    status = scalar_field(fields, "status", errors).lower()
    if status and status not in {"draft", "stable", "deprecated"}:
        errors.append("Atomic-note status must be draft, stable, or deprecated.")
    workflow = tag_set & WORKFLOW_TAGS
    if status == "draft" and workflow and not workflow <= {"draft", "review"}:
        errors.append("Draft status requires a draft or review workflow tag.")
    if status in {"stable", "deprecated"} and workflow and workflow != {"publish"}:
        errors.append(f"{status.title()} status requires the publish workflow tag.")

    sources = mapping_sequence(
        fields.get("sources"), "Atomic-note sources", errors
    )
    if fields.get("sources") is not None and not sources:
        errors.append("Atomic-note sources must include at least one source.")
    source_ids: list[str] = []
    for source in sources:
        source_id = source.get("id", "")
        resource = source.get("resource", "")
        if not source_id:
            errors.append('Every atomic-note source requires an "id".')
        elif not SOURCE_ID.fullmatch(source_id):
            errors.append("Atomic-note source ids must use lowercase kebab-case.")
        else:
            source_ids.append(source_id)
        if not resource:
            errors.append('Every atomic-note source requires a "resource".')
        if source.get("author"):
            validate_actor(source["author"], "Source author", errors)
        if source.get("last_modified"):
            parse_timestamp(
                source["last_modified"], "Source last_modified", errors
            )
        if source.get("usage_count") and not source["usage_count"].isdigit():
            errors.append("Source usage_count must be a non-negative integer.")
    if len(source_ids) != len(set(source_ids)):
        errors.append("Atomic-note source ids must be unique.")

    generated = nested_mapping(
        fields.get("generated"), "Atomic-note generated", errors
    )
    if fields.get("generated") is not None:
        if not generated.get("by"):
            errors.append('Atomic-note generated requires a "by" actor.')
        else:
            validate_actor(generated["by"], "Atomic-note generated.by", errors)
        if not generated.get("at"):
            errors.append('Atomic-note generated requires an "at" timestamp.')
        else:
            parse_timestamp(
                generated["at"], "Atomic-note generated.at", errors
            )

    verified_item = fields.get("verified")
    if verified_item is not None:
        if any(SEQUENCE_YAML_FIELD.fullmatch(line) for line in verified_item.lines):
            verification_events = mapping_sequence(
                verified_item, "Atomic-note verified", errors
            )
        else:
            verification = nested_mapping(
                verified_item, "Atomic-note verified", errors
            )
            verification_events = [verification] if verification else []
        if not verification_events:
            errors.append(
                "Atomic-note verified must contain at least one verification event."
            )
        for event in verification_events:
            if not event.get("by"):
                errors.append('Every verification event requires a "by" actor.')
            else:
                validate_actor(
                    event["by"], "Atomic-note verified.by", errors
                )
            if not event.get("at"):
                errors.append('Every verification event requires an "at" timestamp.')
            else:
                parse_timestamp(
                    event["at"], "Atomic-note verified.at", errors
                )

    stale_after = scalar_field(fields, "stale_after", errors)
    if stale_after:
        parse_timestamp(stale_after, "Atomic-note stale_after", errors)


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


def validate_moc_diagram(
    raw_moc: str,
    section_name: str,
    note_titles: list[str],
    errors: list[str],
    *,
    allow_empty: bool = False,
) -> None:
    body = section_body(raw_moc, section_name)
    if body is None:
        errors.append(f"MOC requires a {section_name.title()} section.")
        return
    if allow_empty and body.strip().lower() == EMPTY_WORKFLOW.lower():
        return
    diagrams = [
        content for language, content in fenced_blocks(body) if language == "mermaid"
    ]
    if len(diagrams) != 1:
        errors.append(
            f"MOC {section_name.title()} requires exactly one fenced Mermaid diagram."
        )
        return
    labels = [
        label
        for line in diagrams[0].splitlines()
        if not line.lstrip().startswith("subgraph ")
        for label in MERMAID_NODE_LABEL.findall(line)
    ]
    expected = Counter(note_titles)
    actual = Counter(labels)
    missing = sorted((expected - actual).elements())
    extra = sorted((actual - expected).elements())
    if missing:
        errors.append(
            f"MOC {section_name.title()} is missing atomic-note title(s): "
            + ", ".join(missing)
            + "."
        )
    if extra:
        errors.append(
            f"MOC {section_name.title()} contains node(s) not listed in Notes: "
            + ", ".join(extra)
            + "."
        )


def template_prompts(text: str) -> list[str]:
    lines = {line.strip() for line in text.splitlines() if line.strip()}
    return sorted(lines & TEMPLATE_PROMPTS)


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
    tags = {tag.lower() for tag in INLINE_TAG.findall(tags_line)}
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
    raw_note = args.note.read_text(encoding="utf-8")
    raw_moc = args.moc.read_text(encoding="utf-8")
    frontmatter, note_body = split_frontmatter(raw_note, errors)
    note = strip_fenced_blocks(note_body)
    moc = strip_fenced_blocks(raw_moc)

    if WIKI_LINK.search(note):
        errors.append(
            "OKF atomic notes must use standard Markdown links, not wiki-style links."
        )
    if TRANSCLUSION.search(note) or TRANSCLUSION.search(moc):
        errors.append("Atomic note and MOC must not use tool-specific wiki transclusions.")
    remaining_prompts = template_prompts(raw_note)
    if remaining_prompts:
        errors.append(
            "Atomic note contains unreplaced template prompt(s): "
            + ", ".join(remaining_prompts)
        )
    if SOURCE_ATTRIBUTION.search(note_body) or SOURCE_HEADING.search(note_body):
        errors.append(
            "Atomic-note body must not include source, reference, citation, "
            "attribution, or based-on fields or headings; use frontmatter sources."
        )
    if EXTERNAL_SOURCE_URL.search(note_body):
        errors.append(
            "Atomic-note body must not include external source URLs; "
            "use an approved frontmatter sources resource."
        )
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
    note_title = H1.findall(note)[0].strip() if len(H1.findall(note)) == 1 else ""
    validate_okf_metadata(frontmatter, note_title, errors)

    parent = field(note, "Parent")
    parent_links = link_filenames(parent or "")
    if parent is None:
        errors.append("Atomic note requires a Parent field.")
    elif parent_links != {args.moc.name.lower()}:
        errors.append("Atomic-note Parent must contain exactly the supplied MOC link.")

    validate_tags(field(moc, "Tags"), errors, "MOC", "moc")

    sections = [heading.strip().lower() for heading in H2.findall(note)]
    missing_sections = [
        section for section in REQUIRED_SECTIONS if section not in sections
    ]
    if missing_sections:
        errors.append("Atomic note is missing section(s): " + ", ".join(missing_sections))
    duplicate_sections = [
        section for section in REQUIRED_SECTIONS if sections.count(section) > 1
    ]
    if duplicate_sections:
        errors.append(
            "Atomic note repeats section(s): " + ", ".join(duplicate_sections)
        )
    unexpected_sections = [
        section for section in sections if section not in REQUIRED_SECTIONS
    ]
    if unexpected_sections:
        errors.append(
            "Atomic note has unexpected section(s): "
            + ", ".join(unexpected_sections)
        )
    required_in_document = [
        section for section in sections if section in REQUIRED_SECTIONS
    ]
    if not missing_sections and required_in_document != list(REQUIRED_SECTIONS):
        errors.append(
            "Atomic-note sections must follow this order: "
            + ", ".join(REQUIRED_SECTIONS)
            + "."
        )
    for section in REQUIRED_SECTIONS:
        body = section_body(note, section)
        if body is not None and not WORD.search(strip_internal_links(body)):
            errors.append(f'Atomic-note section "{section}" must not be empty.')

    pattern = section_body(note, "pattern") or ""
    pattern_lines = [
        re.sub(r"^\s*>\s?", "", line).strip()
        for line in pattern.splitlines()
        if line.strip()
    ]
    if pattern and (
        len(pattern_lines) != 1
        or not PATTERN_FORM.fullmatch(pattern_lines[0])
        or len(re.findall(r"[.!?]", pattern_lines[0])) != 1
    ):
        errors.append(
            'Pattern section must contain one "When X, do Y, because Z." sentence.'
        )

    for section in ACTION_SECTIONS:
        body = section_body(note, section) or ""
        if body and not BULLET.search(body):
            errors.append(
                f'Atomic-note section "{section}" requires at least one bullet.'
            )

    relationships = section_body(note, "relationships") or ""
    relationship_links = internal_links(relationships)
    if relationships and not relationship_links:
        if not NO_RELATIONSHIPS.search(relationships):
            errors.append(
                "Relationships must contain typed links or state "
                '"No supported relationships yet."'
            )
    for line in relationships.splitlines():
        links = internal_links(line)
        if links:
            if not TYPED_RELATIONSHIP.match(line):
                errors.append(
                    "Every relationship link requires a supported type: "
                    "Prerequisite, Extension, Contrast, or Example."
                )
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
    if EXTERNAL_SOURCE_URL.search("\n".join(moc_link_lines)):
        errors.append("MOC entry for the atomic note must not include external source URLs.")
    if MOC_SOURCE_ATTRIBUTION.search("\n".join(moc_link_lines)):
        errors.append(
            "MOC entry for the atomic note must not include source attribution."
        )
    if moc_link_lines and EMPTY_MOC.search(moc_notes):
        errors.append(
            'MOC Notes cannot combine "No atomic notes yet." with atomic-note links.'
        )
    if moc_link_lines and note_title:
        current_display_labels: list[str] = []
        for line in moc_link_lines:
            markdown = MARKDOWN_LINK_WITH_LABEL.search(line)
            if markdown:
                current_display_labels.append(markdown.group(1).strip())
                continue
            wiki = WIKI_LINK_WITH_LABEL.search(line)
            if wiki:
                current_display_labels.append(
                    (wiki.group(2) or Path(wiki.group(1)).stem).strip()
                )
        if current_display_labels != [note_title]:
            errors.append("MOC entry title must match the atomic-note title exactly.")
        all_display_labels: list[str] = []
        for line in moc_notes.splitlines():
            markdown = MARKDOWN_LINK_WITH_LABEL.search(line)
            if markdown and markdown_link_target(markdown.group(2)) is not None:
                display_label = markdown.group(1).strip()
                target = normalized_filename(markdown.group(2))
            else:
                wiki = WIKI_LINK_WITH_LABEL.search(line)
                if not wiki:
                    continue
                display_label = (wiki.group(2) or Path(wiki.group(1)).stem).strip()
                target = normalized_filename(wiki.group(1))
            all_display_labels.append(display_label)
            target_path = args.moc.parent / target if target is not None else None
            if target_path is None or not target_path.is_file():
                continue
            target_titles = H1.findall(
                strip_fenced_blocks(target_path.read_text(encoding="utf-8"))
            )
            if len(target_titles) != 1:
                errors.append(
                    f'MOC atomic note "{target}" requires exactly one level-one title.'
                )
            elif display_label != target_titles[0].strip():
                errors.append(
                    f'MOC Notes title "{display_label}" must match atomic-note title '
                    f'"{target_titles[0].strip()}".'
                )
        validate_moc_diagram(raw_moc, "pattern map", all_display_labels, errors)
        validate_moc_diagram(
            raw_moc,
            "domain workflow",
            all_display_labels,
            errors,
            allow_empty=True,
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
