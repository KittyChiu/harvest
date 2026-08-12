#!/usr/bin/env python3
"""Regression tests for the bundled Marp validator."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


VALIDATOR = Path(__file__).with_name("validate_marp.py")


def run_validator(deck: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        deck_path = Path(directory) / "deck.md"
        deck_path.write_text(deck, encoding="utf-8")
        command = ["python3", str(VALIDATOR), str(deck_path)]
        return subprocess.run(
            command,
            capture_output=True,
            check=False,
            text=True,
        )


class ValidateMarpTests(unittest.TestCase):
    def test_accepts_both_separators_and_empty_notes(self) -> None:
        result = run_validator(
            """---
marp: true
theme: default
size: 16:9
---
# First
<!-- source-contract: first-message -->
<!-- source: first-message -->
<!---->
===
# Second
<!--Example: a natural-language speaker note.-->
"""
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Checked 2 slides", result.stdout)

    def test_rejects_substring_frontmatter_false_positive(self) -> None:
        result = run_validator(
            """---
marp: trueish
description: theme:
size: 16:9
---
# Slide
<!---->
"""
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("marp: true", result.stdout)
        self.assertIn("non-empty theme", result.stdout)

    def test_directive_comment_does_not_count_as_notes(self) -> None:
        result = run_validator(
            """---
marp: true
theme: default
size: 16:9
---
# Slide
<!--theme: uncover-->
"""
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("no speaker-note comment", result.stdout)

    def test_accepts_legacy_canonical_disposition_markers(self) -> None:
        result = run_validator(
            """---
marp: true
theme: default
size: 16:9
---
# Focus the context
<!-- source-contract: core-idea-1, guiding-principles-1, practices-1, constraints-1 -->
<!-- canonical: core-idea-1, guiding-principles-1 -->
<!--Explain why focus matters.-->
---
# Put it into practice
<!-- canonical: practices-1, constraints-1 -->
<!--Explain the trade-off.-->
""",
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("4 source item(s): 0 unclassified", result.stdout)

    def test_rejects_unclassified_source_item(self) -> None:
        result = run_validator(
            """---
marp: true
theme: default
size: 16:9
---
# Focus the context
<!-- source-contract: outcome-focus, checkpoint-choice -->
<!-- source: outcome-focus -->
<!--Explain why focus matters.-->
""",
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("checkpoint-choice", result.stdout)

    def test_canonical_marker_does_not_count_as_notes(self) -> None:
        result = run_validator(
            """---
marp: true
theme: default
size: 16:9
---
# Focus the context
<!-- source-contract: core-idea-1 -->
<!-- canonical: core-idea-1 -->
""",
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("no speaker-note comment", result.stdout)

    def test_accepts_descriptive_contract_ids(self) -> None:
        result = run_validator(
            """---
marp: true
theme: default
size: 16:9
---
# Adapt to the source
<!-- source-contract: tension, preserve-decision, reset-on-outcome-change -->
<!-- source: tension, preserve-decision, reset-on-outcome-change -->
<!--Explain the source in its own structure.-->
""",
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("3 source item(s): 0 unclassified", result.stdout)

    def test_accepts_approved_item_and_group_exclusions(self) -> None:
        result = run_validator(
            """---
marp: true
theme: default
size: 16:9
---
# Keep only what serves the objective
<!-- source-contract: tension, example, further-reading-context-rot, further-reading-recency-bias -->
<!-- source: tension -->
<!-- source-optional: example | reason: The live demo replaces it -->
<!-- source-excluded: further-reading-* | reason: Outside this deck's objective -->
<!--Explain the approved scope.-->
""",
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("4 source item(s): 0 unclassified", result.stdout)

    def test_rejects_exclusion_without_reason(self) -> None:
        result = run_validator(
            """---
marp: true
theme: default
size: 16:9
---
# Topic
<!-- source-contract: example -->
<!-- source-excluded: example -->
<!--Explain the scope.-->
""",
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("without a reason", result.stdout)

    def test_accepts_source_contract(self) -> None:
        result = run_validator(
            """---
marp: true
theme: default
size: 16:9
---
# Focus the context
<!-- source-contract: outcome-focus, checkpoint-choice -->
<!-- source: outcome-focus -->
<!-- source-notes: checkpoint-choice -->
<!--Explain the approved ideas from the raw notes.-->
"""
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("2 source item(s): 0 unclassified", result.stdout)

    def test_rejects_missing_source_contract(self) -> None:
        result = run_validator(
            """---
marp: true
theme: default
size: 16:9
---
# Focus the context
<!--Explain the raw notes.-->
"""
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("requires a non-empty source-contract", result.stdout)


if __name__ == "__main__":
    unittest.main()