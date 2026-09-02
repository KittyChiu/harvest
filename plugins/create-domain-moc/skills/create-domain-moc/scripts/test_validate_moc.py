#!/usr/bin/env python3
"""Regression tests for the domain-MOC validator."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


VALIDATOR = Path(__file__).with_name("validate_moc.py")
TEMPLATE = (
    Path(__file__).parents[1] / "assets" / "domain-moc-template.md"
).read_text(encoding="utf-8")

EMPTY_MOC = """# AI and engineering

Tags: #ai #moc #draft #private

## Scope

Reusable ideas about how AI changes engineering work. Product setup belongs elsewhere.

## Notes

No atomic notes yet.
"""

LINKED_MOC = """# AI and engineering

Tags: #ai #moc #review #public

## Scope

Reusable ideas about how AI changes engineering work. Product setup belongs elsewhere.

## Notes

- [Unit of work changes](ai-engineering-unit-of-work-changes.md) — How AI changes the unit of engineering work.
"""


def run_validator(
    moc: str = EMPTY_MOC,
    moc_name: str = "ai-engineering-moc.md",
    linked_files: tuple[str, ...] = (),
) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        moc_path = root / moc_name
        moc_path.write_text(moc, encoding="utf-8")
        for filename in linked_files:
            (root / filename).write_text("# Existing note\n", encoding="utf-8")
        return subprocess.run(
            ["python3", str(VALIDATOR), str(moc_path)],
            capture_output=True,
            check=False,
            text=True,
        )


class ValidateMocTests(unittest.TestCase):
    def test_accepts_new_moc_with_empty_state(self) -> None:
        result = run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 error(s)", result.stdout)

    def test_rejects_untouched_template_scaffold(self) -> None:
        result = run_validator(moc=TEMPLATE, moc_name="domain-moc.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("unreplaced template prompt(s)", result.stdout)

    def test_rejects_template_prompt_left_in_completed_moc(self) -> None:
        moc = EMPTY_MOC.replace(
            "Reusable ideas about how AI changes engineering work. Product setup belongs elsewhere.",
            "State what belongs in this domain. State the closest material that belongs elsewhere.",
        )
        result = run_validator(moc=moc)
        self.assertEqual(result.returncode, 1)
        self.assertIn("unreplaced template prompt(s)", result.stdout)

    def test_accepts_descriptive_link_to_existing_note(self) -> None:
        result = run_validator(
            moc=LINKED_MOC,
            linked_files=("ai-engineering-unit-of-work-changes.md",),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_accepts_full_marp_markdown_link_outside_notes(self) -> None:
        moc = (
            LINKED_MOC
            + "\n## Presentation\n\n"
            "[Domain presentation](ai-engineering.marp.md) — Presents these ideas together.\n"
        )
        result = run_validator(
            moc=moc,
            linked_files=(
                "ai-engineering-unit-of-work-changes.md",
                "ai-engineering.marp.md",
            ),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_ignores_headings_and_links_inside_fenced_code(self) -> None:
        moc = LINKED_MOC.replace(
            "Reusable ideas about how AI changes engineering work.",
            "Reusable ideas about how AI changes engineering work.\n\n"
            "```markdown\n# Example\n[Missing](missing-note.md)\n```",
        )
        result = run_validator(
            moc=moc,
            linked_files=("ai-engineering-unit-of-work-changes.md",),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_root_absolute_markdown_link(self) -> None:
        result = run_validator(
            moc=LINKED_MOC.replace(
                "ai-engineering-unit-of-work-changes.md",
                "/elsewhere/other.marp.md",
            )
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("flat lowercase kebab-case", result.stdout)

    def test_accepts_wiki_style_links_for_compatible_pkm_tools(self) -> None:
        result = run_validator(
            moc=LINKED_MOC.replace(
                "[Unit of work changes](ai-engineering-unit-of-work-changes.md)",
                "[[ai-engineering-unit-of-work-changes]]",
            ),
            linked_files=("ai-engineering-unit-of-work-changes.md",),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_tool_specific_wiki_transclusions(self) -> None:
        result = run_validator(
            moc=LINKED_MOC.replace(
                "[Unit of work changes](ai-engineering-unit-of-work-changes.md)",
                "![[ai-engineering-unit-of-work-changes]]",
            ),
            linked_files=("ai-engineering-unit-of-work-changes.md",),
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("wiki transclusions", result.stdout)

    def test_rejects_uppercase_markdown_extension(self) -> None:
        result = run_validator(
            moc=LINKED_MOC.replace(".md)", ".MD)"),
            linked_files=("ai-engineering-unit-of-work-changes.md",),
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("flat lowercase kebab-case", result.stdout)

    def test_requires_existing_file(self) -> None:
        result = subprocess.run(
            ["python3", str(VALIDATOR), "missing-moc.md"],
            capture_output=True,
            check=False,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("File not found", result.stdout)

    def test_requires_lowercase_kebab_case_filename(self) -> None:
        result = run_validator(moc_name="AI Engineering MOC.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("lowercase kebab-case", result.stdout)

    def test_requires_one_title(self) -> None:
        result = run_validator(moc=EMPTY_MOC + "\n# Another title\n")
        self.assertEqual(result.returncode, 1)
        self.assertIn("exactly one", result.stdout)

    def test_requires_moc_and_filter_tags(self) -> None:
        result = run_validator(moc=EMPTY_MOC.replace("#ai #moc #draft #private", "#draft"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("#moc", result.stdout)
        self.assertIn("visibility tag", result.stdout)
        self.assertIn("domain tag", result.stdout)

    def test_requires_scope_and_notes(self) -> None:
        result = run_validator(
            moc=EMPTY_MOC.replace("## Scope", "## Purpose").replace(
                "## Notes", "## Index"
            )
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("scope", result.stdout)
        self.assertIn("notes", result.stdout)

    def test_rejects_duplicate_required_section(self) -> None:
        moc = EMPTY_MOC.replace(
            "## Notes",
            "## Scope\n\nAnother boundary.\n\n## Notes",
        )
        result = run_validator(moc=moc)
        self.assertEqual(result.returncode, 1)
        self.assertIn("repeats section(s): scope", result.stdout)

    def test_rejects_required_sections_out_of_order(self) -> None:
        moc = """# AI and engineering

Tags: #ai #moc #draft #private

## Notes

No atomic notes yet.

## Scope

Reusable ideas about AI engineering. Product setup belongs elsewhere.
"""
        result = run_validator(moc=moc)
        self.assertEqual(result.returncode, 1)
        self.assertIn("must follow this order", result.stdout)

    def test_rejects_bare_internal_link(self) -> None:
        result = run_validator(
            moc=LINKED_MOC.replace(
                "- [Unit of work changes](ai-engineering-unit-of-work-changes.md) — How AI changes the unit of engineering work.",
                "- [Unit of work changes](ai-engineering-unit-of-work-changes.md)",
            ),
            linked_files=("ai-engineering-unit-of-work-changes.md",),
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("explanatory prose", result.stdout)

    def test_rejects_unresolved_internal_link(self) -> None:
        result = run_validator(moc=LINKED_MOC)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Unresolved MOC internal link", result.stdout)

    def test_rejects_path_components_in_internal_link(self) -> None:
        result = run_validator(
            moc=LINKED_MOC.replace(
                "(ai-engineering-unit-of-work-changes.md)",
                "(../unit-of-work-changes.md)",
            )
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("flat lowercase kebab-case", result.stdout)

    def test_rejects_non_atomic_note_entries(self) -> None:
        result = run_validator(
            moc=LINKED_MOC.replace(
                "(ai-engineering-unit-of-work-changes.md)",
                "(ai-engineering-unit-of-work-changes.coach.md)",
            ),
            linked_files=("ai-engineering-unit-of-work-changes.coach.md",),
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("only to atomic notes", result.stdout)

    def test_rejects_atomic_note_from_another_domain(self) -> None:
        result = run_validator(
            moc=LINKED_MOC.replace(
                "(ai-engineering-unit-of-work-changes.md)",
                "(leadership-unit-of-work-changes.md)",
            ),
            linked_files=("leadership-unit-of-work-changes.md",),
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("this domain", result.stdout)

    def test_rejects_empty_state_with_note_entries(self) -> None:
        result = run_validator(
            moc=LINKED_MOC.replace(
                "## Notes\n",
                "## Notes\n\nNo atomic notes yet.\n",
            ),
            linked_files=("ai-engineering-unit-of-work-changes.md",),
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("cannot combine", result.stdout)


if __name__ == "__main__":
    unittest.main()
