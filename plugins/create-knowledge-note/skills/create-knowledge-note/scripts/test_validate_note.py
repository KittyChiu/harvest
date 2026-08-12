#!/usr/bin/env python3
"""Regression tests for the knowledge-note validator."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


VALIDATOR = Path(__file__).with_name("validate_note.py")

NOTE = """# Focus

## Core Idea

Use attention deliberately.

## Guiding Principles

- Choose before reacting.

## Practices

- Protect one useful pause.

## Examples

A team pauses before committing.

## Constraints

Urgency can narrow the available choices.

## Related Ideas

See [reflection](https://example.com/reflection).
"""


def run_validator(
    note: str, *arguments: str, filename: str = "focus.md"
) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        note_path = Path(directory) / filename
        note_path.write_text(note, encoding="utf-8")
        return subprocess.run(
            ["python3", str(VALIDATOR), *arguments, str(note_path)],
            capture_output=True,
            check=False,
            text=True,
        )


class ValidateNoteTests(unittest.TestCase):
    def test_accepts_compliant_note(self) -> None:
        result = run_validator(NOTE)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("6 level-two section(s), 0 error(s)", result.stdout)

    def test_requires_existing_file(self) -> None:
        result = subprocess.run(
            ["python3", str(VALIDATOR), "missing.md"],
            capture_output=True,
            check=False,
            text=True,
        )

        self.assertEqual(result.returncode, 2)
        self.assertIn("File not found", result.stdout)

    def test_requires_at_least_five_sections(self) -> None:
        result = run_validator(
            """# Focus

## One
Content.
## Two
Content.
## Three
Content.
## Four
Content.
"""
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("5-8 level-two sections; found 4", result.stdout)

    def test_rejects_more_than_eight_sections(self) -> None:
        result = run_validator(
            "# Focus\n\n"
            + "\n".join(f"## Section {index}\nContent." for index in range(1, 10))
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("5-8 level-two sections; found 9", result.stdout)

    def test_rejects_empty_section(self) -> None:
        result = run_validator(NOTE.replace("Use attention deliberately.", "<!-- TODO -->"))

        self.assertEqual(result.returncode, 1)
        self.assertIn('"Core Idea" must not be empty', result.stdout)

    def test_rejects_more_than_300_visible_words(self) -> None:
        result = run_validator(NOTE + "\n" + "word " * 275)

        self.assertEqual(result.returncode, 1)
        self.assertIn("at most 300 visible words", result.stdout)

    def test_counts_link_labels_but_not_destinations_or_markdown(self) -> None:
        result = run_validator(NOTE)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("33 visible word(s)", result.stdout)

    def test_counts_a_visible_url_as_one_word(self) -> None:
        result = run_validator(NOTE + "\nhttps://example.com/a/long/path\n")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("34 visible word(s)", result.stdout)

    def test_excludes_comments_from_word_count(self) -> None:
        result = run_validator(NOTE + "\n<!-- " + "hidden " * 300 + "-->\n")

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_front_matter_by_default(self) -> None:
        result = run_validator("---\ntags: [focus]\n---\n" + NOTE)

        self.assertEqual(result.returncode, 1)
        self.assertIn("must not contain front matter", result.stdout)

    def test_allows_requested_front_matter_without_counting_it(self) -> None:
        result = run_validator(
            "---\ntitle: " + "metadata " * 300 + "\n---\n" + NOTE,
            "--allow-front-matter",
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("33 visible word(s)", result.stdout)


if __name__ == "__main__":
    unittest.main()
