#!/usr/bin/env python3
"""Regression tests for the atomic-note validator."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


VALIDATOR = Path(__file__).with_name("validate_atomic_note.py")

NOTE = """# Golden paths reduce cognitive load

Parent: [Platform](platform-moc.md)
Tags: #platform #draft #private

## Core idea

Golden paths reduce repeated decisions without removing escape hatches.

## Why it matters

Teams can spend attention on product-specific work.

## Practices

- Automate the common path and document exceptions.

## Constraints

- A golden path becomes harmful when teams cannot leave it.

## Relationships

This practice supports [platform teams as products](platform-team-as-a-product.md) because both optimize for user needs.
"""

MOC = """# Platform

Tags: #platform #moc #draft #private

## Scope

Reusable ideas about internal platforms.

## Notes

- [Golden paths reduce cognitive load](platform-golden-paths-reduce-cognitive-load.md) — How paved roads preserve team attention.
"""


def run_validator(
    note: str = NOTE,
    moc: str = MOC,
    note_name: str = "platform-golden-paths-reduce-cognitive-load.md",
    moc_name: str = "platform-moc.md",
    separate_directories: bool = False,
    linked_files: tuple[str, ...] = ("platform-team-as-a-product.md",),
) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        note_path = root / note_name
        moc_directory = root / "other" if separate_directories else root
        moc_directory.mkdir(exist_ok=True)
        moc_path = moc_directory / moc_name
        note_path.write_text(note, encoding="utf-8")
        moc_path.write_text(moc, encoding="utf-8")
        for filename in linked_files:
            (root / filename).write_text("# Existing note\n", encoding="utf-8")
        return subprocess.run(
            ["python3", str(VALIDATOR), str(note_path), str(moc_path)],
            capture_output=True,
            check=False,
            text=True,
        )


class ValidateAtomicNoteTests(unittest.TestCase):
    def test_accepts_atomic_note_linked_from_moc(self) -> None:
        result = run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 error(s)", result.stdout)

    def test_accepts_full_marp_markdown_link_in_moc(self) -> None:
        moc = (
            MOC
            + "\n## Presentation\n\n"
            "[Domain presentation](platform.marp.md) — Presents these ideas together.\n"
        )
        result = run_validator(
            moc=moc,
            linked_files=("platform-team-as-a-product.md", "platform.marp.md"),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_ignores_headings_and_links_inside_fenced_code(self) -> None:
        note = NOTE.replace(
            "Golden paths reduce repeated decisions without removing escape hatches.",
            "Golden paths reduce repeated decisions without removing escape hatches.\n\n"
            "```markdown\n# Example\n[Missing](missing-note.md)\n```",
        )
        result = run_validator(note=note)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_root_absolute_markdown_link(self) -> None:
        note = NOTE.replace(
            "platform-team-as-a-product.md",
            "/elsewhere/platform-team-as-a-product.md",
        )
        result = run_validator(note=note)
        self.assertEqual(result.returncode, 1)
        self.assertIn("flat lowercase kebab-case", result.stdout)

    def test_accepts_wiki_style_links_for_compatible_pkm_tools(self) -> None:
        note = NOTE.replace("[Platform](platform-moc.md)", "[[platform-moc]]").replace(
            "[platform teams as products](platform-team-as-a-product.md)",
            "[[platform-team-as-a-product]]",
        )
        moc = MOC.replace(
            "[Golden paths reduce cognitive load](platform-golden-paths-reduce-cognitive-load.md)",
            "[[platform-golden-paths-reduce-cognitive-load]]",
        )
        result = run_validator(note=note, moc=moc)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_tool_specific_wiki_transclusions(self) -> None:
        result = run_validator(
            note=NOTE.replace(
                "[platform teams as products](platform-team-as-a-product.md)",
                "![[platform-team-as-a-product]]",
            )
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("wiki transclusions", result.stdout)

    def test_rejects_uppercase_markdown_extension(self) -> None:
        result = run_validator(note=NOTE.replace("platform-moc.md", "platform-moc.MD"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("Markdown .md filename", result.stdout)

    def test_requires_existing_files(self) -> None:
        result = subprocess.run(
            ["python3", str(VALIDATOR), "missing-note.md", "missing-moc.md"],
            capture_output=True,
            check=False,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("File not found", result.stdout)

    def test_requires_same_knowledge_directory(self) -> None:
        result = run_validator(separate_directories=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("same knowledge directory", result.stdout)

    def test_requires_domain_filename_prefix(self) -> None:
        result = run_validator(note_name="leadership-golden-paths.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("MOC domain stem", result.stdout)

    def test_requires_lowercase_kebab_case_filenames(self) -> None:
        result = run_validator(
            note_name="Platform-Golden-Paths.md",
            moc_name="Platform-moc.md",
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("lowercase kebab-case", result.stdout)

    def test_requires_parent_moc(self) -> None:
        result = run_validator(
            note=NOTE.replace("[Platform](platform-moc.md)", "[Other](other-moc.md)", 1)
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Parent must contain exactly", result.stdout)

    def test_rejects_multiple_parent_mocs(self) -> None:
        result = run_validator(
            note=NOTE.replace(
                "Parent: [Platform](platform-moc.md)",
                "Parent: [Platform](platform-moc.md) [Leadership](leadership-moc.md)",
            ),
            linked_files=("platform-team-as-a-product.md", "leadership-moc.md"),
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("exactly the supplied MOC", result.stdout)

    def test_requires_tag_categories(self) -> None:
        result = run_validator(note=NOTE.replace("#platform #draft #private", "#draft"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("visibility tag", result.stdout)
        self.assertIn("domain tag", result.stdout)

    def test_rejects_multiple_workflow_tags(self) -> None:
        result = run_validator(
            note=NOTE.replace("#platform #draft #private", "#platform #draft #review #private")
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("exactly one workflow", result.stdout)

    def test_requires_moc_filter_tags(self) -> None:
        result = run_validator(moc=MOC.replace(" #draft #private", ""))
        self.assertEqual(result.returncode, 1)
        self.assertIn("MOC tags must include one workflow", result.stdout)
        self.assertIn("MOC tags must include one visibility", result.stdout)

    def test_requires_all_atomic_sections(self) -> None:
        result = run_validator(note=NOTE.replace("## Constraints", "## Boundaries"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("constraints", result.stdout)

    def test_rejects_bare_relationship_links(self) -> None:
        note = NOTE.replace(
            "This practice supports [platform teams as products](platform-team-as-a-product.md) because both optimize for user needs.",
            "- [Platform teams as products](platform-team-as-a-product.md)",
        )
        result = run_validator(note=note)
        self.assertEqual(result.returncode, 1)
        self.assertIn("explanatory prose", result.stdout)

    def test_rejects_dangling_relationship_links(self) -> None:
        result = run_validator(linked_files=())
        self.assertEqual(result.returncode, 1)
        self.assertIn("unresolved internal link", result.stdout)

    def test_requires_descriptive_moc_entry(self) -> None:
        result = run_validator(
            moc=MOC.replace(
                "- [Golden paths reduce cognitive load](platform-golden-paths-reduce-cognitive-load.md) — How paved roads preserve team attention.",
                "- [Golden paths reduce cognitive load](platform-golden-paths-reduce-cognitive-load.md)",
            )
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("navigation description", result.stdout)

    def test_requires_moc_entry_inside_notes_section(self) -> None:
        moc = MOC.replace(
            "Reusable ideas about internal platforms.",
            "Reusable ideas about [golden paths](platform-golden-paths-reduce-cognitive-load.md).",
        ).replace(
            "- [Golden paths reduce cognitive load](platform-golden-paths-reduce-cognitive-load.md) — How paved roads preserve team attention.",
            "- [Platform teams as products](platform-team-as-a-product.md) — How to run a platform team.",
        )
        result = run_validator(moc=moc)
        self.assertEqual(result.returncode, 1)
        self.assertIn("MOC must link to the atomic note", result.stdout)

    def test_rejects_empty_state_with_atomic_note_entry(self) -> None:
        result = run_validator(
            moc=MOC.replace(
                "## Notes\n",
                "## Notes\n\nNo atomic notes yet.\n",
            )
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("cannot combine", result.stdout)

    def test_rejects_non_atomic_moc_entries(self) -> None:
        result = run_validator(
            moc=MOC
            + "\n- [Coaching guidance](platform-golden-paths-reduce-cognitive-load.coach.md) — Coaching guidance.\n",
            linked_files=(
                "platform-team-as-a-product.md",
                "platform-golden-paths-reduce-cognitive-load.coach.md",
            ),
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("only to atomic notes", result.stdout)


if __name__ == "__main__":
    unittest.main()
