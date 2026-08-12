#!/usr/bin/env python3
"""Validate participant and coach guides as one self-paced learning module."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


COMMENT = re.compile(r"<!--(.*?)-->", re.DOTALL)
SOURCE_DISPOSITION_COMMENT = re.compile(
    r"^\s*(?:canonical|source)(?:-(learner|coach|participant|facilitator|optional|excluded))?\s*:\s*(.*?)\s*$",
    re.IGNORECASE | re.DOTALL,
)
SOURCE_CONTRACT_COMMENT = re.compile(
    r"^\s*(?:canonical|source)-contract\s*:\s*(.*?)\s*$",
    re.IGNORECASE | re.DOTALL,
)
PARTICIPANT_COACHING_SECTION = re.compile(
    r"^#{1,6}\s+(?:appendix:\s*)?(?:coach guide|coaching notes)\s*$",
    re.IGNORECASE | re.MULTILINE,
)
COACH_STAGE_TABLE = re.compile(
    r"^\|\s*Stage\s*\|.*\n\|(?:\s*:?-+:?\s*\|){2,}",
    re.IGNORECASE | re.MULTILINE,
)
PARTICIPANT_STAGE_HEADINGS = (
    "## Scenario",
    "## Exercise",
    "## Reflection",
    "## Takeaways and next step",
)
COACH_STAGE_HEADINGS = (
    "### 1. Scenario",
    "### 2. Exercise",
    "### 3. Reflection",
    "### 4. Takeaways and next step",
)


def fail(message: str) -> None:
    print(f"ERROR: {message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a paired participant and coach learning module."
    )
    parser.add_argument("participant", type=Path)
    parser.add_argument("coach", type=Path)
    return parser.parse_args()


def parse_comments(
    text: str, errors: list[str]
) -> tuple[set[str], list[tuple[str, list[str]]]]:
    contract_ids: set[str] = set()
    markers: list[tuple[str, list[str]]] = []
    for comment in COMMENT.findall(text):
        contract = SOURCE_CONTRACT_COMMENT.match(comment)
        if contract:
            contract_ids.update(
                item.strip().lower()
                for item in contract.group(1).split(",")
                if item.strip()
            )
            continue
        marker = SOURCE_DISPOSITION_COMMENT.match(comment)
        if not marker:
            continue

        disposition = (marker.group(1) or "learner").lower()
        disposition = {
            "participant": "learner",
            "facilitator": "coach",
        }.get(disposition, disposition)
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
            errors.append("Guide has an empty source marker.")
        if separator and not reason_match:
            errors.append("Guide has a malformed source marker reason.")
        if disposition in {"optional", "excluded"} and not reason:
            errors.append(f"Guide has {disposition} source content without a reason.")
        markers.append((disposition, selectors))
    return contract_ids, markers


def main() -> int:
    args = parse_args()
    missing = [path for path in (args.participant, args.coach) if not path.is_file()]
    if missing:
        for path in missing:
            fail(f"File not found: {path}")
        return 2

    participant = args.participant.read_text(encoding="utf-8")
    coach = args.coach.read_text(encoding="utf-8")
    errors: list[str] = []
    participant_suffix = ".participant.guide.md"
    coach_suffix = ".coach.guide.md"

    if not args.participant.name.endswith(participant_suffix):
        errors.append(
            "Participant-guide filename must end with .participant.guide.md."
        )
    if not args.coach.name.endswith(coach_suffix):
        errors.append("Coach-guide filename must end with .coach.guide.md.")
    if (
        args.participant.name.endswith(participant_suffix)
        and args.coach.name.endswith(coach_suffix)
        and args.participant.name[: -len(participant_suffix)]
        != args.coach.name[: -len(coach_suffix)]
    ):
        errors.append("Participant and coach guides require matching module stems.")
    if args.participant.parent.resolve() != args.coach.parent.resolve():
        errors.append(
            "Participant and coach guides require the same output directory."
        )

    participant_contract, participant_markers = parse_comments(participant, errors)
    coach_contract, coach_markers = parse_comments(coach, errors)
    if participant_contract:
        errors.append("Participant guide must not contain a source-contract marker.")
    if PARTICIPANT_COACHING_SECTION.search(participant):
        errors.append("Participant guide must not contain coaching sections.")
    if any(disposition == "coach" for disposition, _ in participant_markers):
        errors.append("Participant guide must not contain coach source markers.")
    if any(
        disposition in {"optional", "excluded"}
        for disposition, _ in participant_markers
    ):
        errors.append(
            "Participant guide must not contain optional or excluded source markers."
        )
    if any(disposition == "learner" for disposition, _ in coach_markers):
        errors.append("Coach guide must not contain learner source markers.")
    if COACH_STAGE_TABLE.search(coach):
        errors.append("Coach guide must not use a stage table.")
    for heading in PARTICIPANT_STAGE_HEADINGS:
        if not re.search(rf"^{re.escape(heading)}\s*$", participant, re.MULTILINE):
            errors.append(f"Participant guide requires heading: {heading}")
    for heading in COACH_STAGE_HEADINGS:
        if not re.search(rf"^{re.escape(heading)}\s*$", coach, re.MULTILINE):
            errors.append(f"Coach guide requires heading: {heading}")

    contract_ids = coach_contract
    markers = participant_markers + coach_markers

    source_items = {item: "" for item in contract_ids}
    if not source_items:
        errors.append("Coach guide requires a non-empty source-contract marker.")

    dispositions: dict[str, set[str]] = {}
    for disposition, selectors in markers:
        for selector in selectors:
            if selector.endswith("-*"):
                if disposition not in {"optional", "excluded"}:
                    errors.append(
                        "Whole-group selectors are allowed only for optional or "
                        f"excluded content: {selector}"
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
        errors.append("Unclassified source item(s): " + ", ".join(unclassified))
    if unknown:
        errors.append("Unknown source item(s): " + ", ".join(unknown))
    if conflicting:
        errors.append(
            "Source item(s) have multiple dispositions: " + ", ".join(conflicting)
        )

    for error in errors:
        fail(error)
    print(
        f"Checked contract for {len(source_items)} source item(s): "
        f"{len(unclassified)} unclassified, {len(errors)} error(s)."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())