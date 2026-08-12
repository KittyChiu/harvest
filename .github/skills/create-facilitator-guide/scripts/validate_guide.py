#!/usr/bin/env python3
"""Validate source coverage dispositions in a facilitator guide."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


COMMENT = re.compile(r"<!--(.*?)-->", re.DOTALL)
SOURCE_DISPOSITION_COMMENT = re.compile(
    r"^\s*(?:canonical|source)(?:-(participant|facilitator|optional|excluded))?\s*:\s*(.*?)\s*$",
    re.IGNORECASE | re.DOTALL,
)
SOURCE_CONTRACT_COMMENT = re.compile(
    r"^\s*(?:canonical|source)-contract\s*:\s*(.*?)\s*$",
    re.IGNORECASE | re.DOTALL,
)


def fail(message: str) -> None:
    print(f"ERROR: {message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate source coverage in a facilitator guide."
    )
    parser.add_argument("guide", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.guide.is_file():
        fail(f"File not found: {args.guide}")
        return 2
    guide = args.guide.read_text(encoding="utf-8")
    errors: list[str] = []
    markers: list[tuple[str, list[str]]] = []
    contract_ids: set[str] = set()

    for comment in COMMENT.findall(guide):
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

        disposition = (marker.group(1) or "participant").lower()
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

    source_items = {item: "" for item in contract_ids}
    if not source_items:
        errors.append("Guide requires a non-empty source-contract marker.")

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