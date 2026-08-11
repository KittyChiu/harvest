#!/usr/bin/env python3
"""Regression tests for the bundled Marp validator."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


VALIDATOR = Path(__file__).with_name("validate_marp.py")


def run_validator(deck: str) -> subprocess.CompletedProcess[str]:
    with tempfile.NamedTemporaryFile("w", suffix=".md", encoding="utf-8") as file:
        file.write(deck)
        file.flush()
        return subprocess.run(
            ["python3", str(VALIDATOR), file.name],
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


if __name__ == "__main__":
    unittest.main()