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

## Pattern map

No pattern map yet.

## Domain workflow

No supported domain workflow yet.

## Notes

No atomic notes yet.
"""

LINKED_MOC = """# AI and engineering

Tags: #ai #moc #review #public

## Scope

Reusable ideas about how AI changes engineering work. Product setup belongs elsewhere.

## Pattern map

The pattern currently stands alone in this domain.

```mermaid
flowchart TD
    A["Unit of work changes"]
```

## Domain workflow

The pattern is the current entry point for the domain workflow.

```mermaid
flowchart TD
    A["Unit of work changes"]
```

## Notes

- [Unit of work changes](ai-engineering-unit-of-work-changes.md) — How AI changes the unit of engineering work.
"""


def run_validator(
    moc: str = EMPTY_MOC,
    moc_name: str = "ai-engineering-moc.md",
    linked_files: tuple[str, ...] = (),
    linked_contents: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        moc_path = root / moc_name
        moc_path.write_text(moc, encoding="utf-8")
        for filename in linked_files:
            title = (
                "Unit of work changes"
                if filename == "ai-engineering-unit-of-work-changes.md"
                else "Second pattern"
                if filename == "ai-engineering-second-pattern.md"
                else "Existing note"
            )
            content = (linked_contents or {}).get(filename, f"# {title}\n")
            (root / filename).write_text(content, encoding="utf-8")
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

    def test_requires_empty_map_and_workflow_for_empty_moc(self) -> None:
        result = run_validator(
            moc=EMPTY_MOC.replace(
                "No pattern map yet.",
                "Patterns will be mapped later.",
            )
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn('must be exactly "No pattern map yet."', result.stdout)

    def test_requires_mermaid_map_for_linked_moc(self) -> None:
        moc = LINKED_MOC.replace(
            "```mermaid\nflowchart TD\n    A[\"Unit of work changes\"]\n```",
            "A prose-only diagram.",
            1,
        )
        result = run_validator(
            moc=moc,
            linked_files=("ai-engineering-unit-of-work-changes.md",),
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Pattern Map requires exactly one fenced Mermaid diagram", result.stdout)

    def test_accepts_populated_moc_without_supported_workflow(self) -> None:
        moc = LINKED_MOC.replace(
            "The pattern is the current entry point for the domain workflow.\n\n"
            "```mermaid\nflowchart TD\n    A[\"Unit of work changes\"]\n```",
            "No supported domain workflow yet.",
        )
        result = run_validator(
            moc=moc,
            linked_files=("ai-engineering-unit-of-work-changes.md",),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_requires_every_note_title_in_both_diagrams(self) -> None:
        moc = LINKED_MOC.replace(
            'A["Unit of work changes"]',
            'A["Different title"]',
            1,
        )
        result = run_validator(
            moc=moc,
            linked_files=("ai-engineering-unit-of-work-changes.md",),
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "Pattern Map is missing exact atomic-note title(s): Unit of work changes",
            result.stdout,
        )

    def test_rejects_partial_pattern_title_match(self) -> None:
        moc = LINKED_MOC.replace(
            'A["Unit of work changes"]',
            'A["Unit of work changes unexpectedly"]',
            1,
        )
        result = run_validator(
            moc=moc,
            linked_files=("ai-engineering-unit-of-work-changes.md",),
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing exact atomic-note title", result.stdout)
        self.assertIn("not listed in Notes", result.stdout)

    def test_rejects_extra_pattern_node(self) -> None:
        moc = LINKED_MOC.replace(
            '    A["Unit of work changes"]\n```',
            '    A["Unit of work changes"]\n    B["Invented pattern"]\n```',
            1,
        )
        result = run_validator(
            moc=moc,
            linked_files=("ai-engineering-unit-of-work-changes.md",),
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("not listed in Notes: Invented pattern", result.stdout)

    def test_rejects_note_label_that_differs_from_atomic_title(self) -> None:
        moc = LINKED_MOC.replace(
            "[Unit of work changes]",
            "[Changed display title]",
        ).replace(
            'A["Unit of work changes"]',
            'A["Changed display title"]',
        )
        result = run_validator(
            moc=moc,
            linked_files=("ai-engineering-unit-of-work-changes.md",),
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("must match atomic-note title", result.stdout)

    def test_rejects_unsupported_pattern_map_relationship(self) -> None:
        moc = LINKED_MOC.replace(
            '    A["Unit of work changes"]\n```',
            '    A["Unit of work changes"]\n'
            '    B["Second pattern"]\n'
            '    A -->|enables| B\n```',
            1,
        ).replace(
            "- [Unit of work changes]",
            "- [Second pattern](ai-engineering-second-pattern.md) — A second decision.\n"
            "- [Unit of work changes]",
        )
        result = run_validator(
            moc=moc,
            linked_files=(
                "ai-engineering-unit-of-work-changes.md",
                "ai-engineering-second-pattern.md",
            ),
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("not supported by the atomic notes", result.stdout)

    def test_rejects_unsupported_inline_pattern_map_relationship(self) -> None:
        moc = LINKED_MOC.replace(
            '    A["Unit of work changes"]',
            '    A["Unit of work changes"] -->|causes| B["Second pattern"]',
            1,
        ).replace(
            "- [Unit of work changes]",
            "- [Second pattern](ai-engineering-second-pattern.md) — A second decision.\n"
            "- [Unit of work changes]",
        )
        result = run_validator(
            moc=moc,
            linked_files=(
                "ai-engineering-unit-of-work-changes.md",
                "ai-engineering-second-pattern.md",
            ),
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("unsupported relationship label: causes", result.stdout)

    def test_rejects_backward_pattern_map_relationship(self) -> None:
        moc = LINKED_MOC.replace(
            '    A["Unit of work changes"]',
            '    A["Unit of work changes"]\n'
            '    B["Second pattern"]\n'
            '    A <--|enables| B',
            1,
        ).replace(
            "- [Unit of work changes]",
            "- [Second pattern](ai-engineering-second-pattern.md) — A second decision.\n"
            "- [Unit of work changes]",
        )
        result = run_validator(
            moc=moc,
            linked_files=(
                "ai-engineering-unit-of-work-changes.md",
                "ai-engineering-second-pattern.md",
            ),
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "ai-engineering-second-pattern.md --enables--> "
            "ai-engineering-unit-of-work-changes.md",
            result.stdout,
        )

    def test_rejects_atomic_note_without_exactly_one_title(self) -> None:
        result = run_validator(
            moc=LINKED_MOC,
            linked_files=("ai-engineering-unit-of-work-changes.md",),
            linked_contents={"ai-engineering-unit-of-work-changes.md": "No title\n"},
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("requires exactly one level-one title", result.stdout)

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
                "[[ai-engineering-unit-of-work-changes|Unit of work changes]]",
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

    def test_does_not_treat_slides_as_a_domain_tag(self) -> None:
        result = run_validator(
            moc=EMPTY_MOC.replace("#ai #moc #draft #private", "#slides #moc #draft #private")
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("domain tag", result.stdout)

    def test_requires_all_domain_sections(self) -> None:
        result = run_validator(
            moc=EMPTY_MOC.replace("## Scope", "## Purpose").replace(
                "## Pattern map", "## System view"
            )
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("scope", result.stdout)
        self.assertIn("pattern map", result.stdout)

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

## Pattern map

No pattern map yet.

## Domain workflow

No supported domain workflow yet.
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

    def test_rejects_arbitrary_notes_prose_without_atomic_links(self) -> None:
        result = run_validator(
            moc=EMPTY_MOC.replace(
                "No atomic notes yet.",
                "Patterns will be added after the next workshop.",
            )
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("must contain atomic-note links or exactly", result.stdout)

    def test_rejects_modified_empty_state(self) -> None:
        result = run_validator(
            moc=EMPTY_MOC.replace(
                "No atomic notes yet.",
                "No atomic notes yet. Add one soon.",
            )
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("must contain atomic-note links or exactly", result.stdout)


if __name__ == "__main__":
    unittest.main()
