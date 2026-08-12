#!/usr/bin/env python3
"""Regression tests for the facilitator-guide validator."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


VALIDATOR = Path(__file__).with_name("validate_guide.py")


def run_validator(guide: str) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        guide_path = Path(directory) / "guide.md"
        guide_path.write_text(guide, encoding="utf-8")
        command = ["python3", str(VALIDATOR), str(guide_path)]
        return subprocess.run(
            command,
            capture_output=True,
            check=False,
            text=True,
        )


class ValidateGuideTests(unittest.TestCase):
    def test_accepts_legacy_canonical_disposition_markers(self) -> None:
        result = run_validator(
            """# Guide

<!-- source-contract: tension-1, field-notes-1, field-notes-2 -->
<!-- canonical: tension-1 -->
<!-- canonical-facilitator: field-notes-1 -->
<!-- canonical-optional: field-notes-2 | reason: Advanced groups only -->
""",
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("3 source item(s): 0 unclassified", result.stdout)

    def test_accepts_approved_whole_group_exclusion(self) -> None:
        result = run_validator(
            """# Guide

<!-- source-contract: tension, further-reading-context-rot, further-reading-recency-bias -->
<!-- source: tension -->
<!-- source-excluded: further-reading-* | reason: Outside workshop scope -->
""",
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("3 source item(s): 0 unclassified", result.stdout)

    def test_rejects_unclassified_source_item(self) -> None:
        result = run_validator(
            """# Guide

<!-- source-contract: tension, handoff-review -->
<!-- source: tension -->
""",
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("handoff-review", result.stdout)

    def test_rejects_exclusion_without_reason(self) -> None:
        result = run_validator(
            """# Guide

        <!-- source-contract: example -->
        <!-- source-excluded: example -->
""",
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("without a reason", result.stdout)

    def test_rejects_conflicting_dispositions(self) -> None:
        result = run_validator(
            """# Guide

        <!-- source-contract: tension -->
        <!-- source: tension -->
        <!-- source-facilitator: tension -->
""",
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("multiple dispositions", result.stdout)

    def test_accepts_source_contract(self) -> None:
        result = run_validator(
            """# Guide

<!-- source-contract: outcome-focus, checkpoint-choice -->
<!-- source: outcome-focus -->
<!-- source-facilitator: checkpoint-choice -->
"""
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("2 source item(s): 0 unclassified", result.stdout)

    def test_rejects_missing_source_contract(self) -> None:
        result = run_validator("# Guide\n")

        self.assertEqual(result.returncode, 1)
        self.assertIn("requires a non-empty source-contract", result.stdout)


if __name__ == "__main__":
    unittest.main()