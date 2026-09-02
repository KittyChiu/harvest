#!/usr/bin/env python3
"""Regression tests for the atomic-pattern validator."""

from __future__ import annotations

import re
import subprocess
import tempfile
import unittest
from pathlib import Path


VALIDATOR = Path(__file__).with_name("validate_atomic_note.py")
TEMPLATE = (
    Path(__file__).parents[1] / "assets" / "atomic-note-template.md"
).read_text(encoding="utf-8")
SKILL = (Path(__file__).parents[1] / "SKILL.md").read_text(encoding="utf-8")
AUTHORING_GUIDE = (
    Path(__file__).parents[1] / "references" / "graph-authoring.md"
).read_text(encoding="utf-8")
REQUIRED_SECTIONS = (
    "Pattern",
    "Practice",
    "Why it works",
    "Signals",
    "Learning",
    "Constraints",
    "Relationships",
)

NOTE = """# Golden paths reduce cognitive load

Parent: [Platform](platform-moc.md)
Tags: #platform #draft #private

## Pattern

When teams repeat common delivery decisions, provide a golden path, because it preserves attention without removing escape hatches.

## Practice

- Automate the common path.
- Document how teams can choose an exception.

## Why it works

A maintained default removes avoidable choices while documented escape hatches preserve autonomy.

## Signals

- Teams repeatedly solve the same delivery setup problems.
- Product work is delayed by avoidable platform decisions.

## Learning

Teams adopted maintained defaults when those defaults removed setup work without blocking legitimate exceptions.

## Constraints

- The default must be maintained as user needs change.
- Teams need a supported way to leave the path.

## Relationships

- Extension: [Platform teams as products](platform-team-as-a-product.md) explains why the path needs product ownership.
"""

MOC = """# Platform

Tags: #platform #moc #draft #private

## Scope

Reusable patterns for internal platforms.

## Notes

- [Golden paths reduce cognitive load](platform-golden-paths-reduce-cognitive-load.md) — Decide when a maintained default can remove repeated delivery choices.
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


def remove_section(note: str, section: str) -> str:
    return re.sub(
        rf"\n## {re.escape(section)}\n.*?(?=\n## |\Z)",
        "",
        note,
        flags=re.DOTALL,
    )


def replace_section_body(note: str, section: str, body: str) -> str:
    return re.sub(
        rf"(## {re.escape(section)}\n\n).*?(?=\n## |\Z)",
        rf"\1{body}",
        note,
        flags=re.DOTALL,
    )


class ValidateAtomicNoteTests(unittest.TestCase):
    def assert_invalid(self, note: str, message: str, **kwargs: object) -> None:
        result = run_validator(note=note, **kwargs)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(message, result.stdout)

    def test_accepts_atomic_pattern_linked_from_moc(self) -> None:
        result = run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 error(s)", result.stdout)

    def test_accepts_explicit_no_relationships_state(self) -> None:
        note = replace_section_body(
            NOTE, "Relationships", "No supported relationships yet.\n"
        )
        result = run_validator(note=note, linked_files=())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_template_defines_exact_section_schema(self) -> None:
        headings = re.findall(r"^##\s+(.+?)\s*$", TEMPLATE, re.MULTILINE)
        self.assertEqual(headings, list(REQUIRED_SECTIONS))
        self.assertTrue(TEMPLATE.endswith("\n"))

    def test_contract_obfuscates_names_and_removes_sources(self) -> None:
        self.assertIn(
            "Replace customer, organization, and team names with neutral roles.",
            TEMPLATE,
        )
        self.assertIn("Do not include source attribution", TEMPLATE)
        self.assertIn("Obfuscate customer, organization, and team names", SKILL)
        self.assertIn("`a customer`, `a product team`, or `an enablement group`", SKILL)
        self.assertNotIn("customer ABC", SKILL)
        self.assertNotIn("product team XYZ", SKILL)
        self.assertIn("Obfuscate identities and remove sources", AUTHORING_GUIDE)
        self.assertIn("Do not use reversible pseudonyms", AUTHORING_GUIDE)

    def test_template_is_scaffold_not_completed_note(self) -> None:
        result = run_validator(note=TEMPLATE)
        self.assertEqual(result.returncode, 1)
        self.assertIn("unreplaced template prompt(s)", result.stdout)
        self.assertIn('one "When X, do Y, because Z." sentence', result.stdout)

    def test_rejects_prompt_left_in_completed_structure(self) -> None:
        note = NOTE.replace(
            "- Automate the common path.",
            "- Use concrete, observable behaviours.",
        )
        self.assert_invalid(note, "unreplaced template prompt(s)")

    def test_rejects_source_attribution_field(self) -> None:
        note = NOTE.replace(
            "Tags: #platform #draft #private",
            "Tags: #platform #draft #private\n"
            "Source: Customer discovery interview",
        )
        self.assert_invalid(note, "must not include source, reference, citation")

    def test_rejects_source_heading(self) -> None:
        note = NOTE + "\n## Sources\n\nCustomer discovery notes.\n"
        self.assert_invalid(note, "must not include source, reference, citation")

    def test_rejects_bold_source_attribution(self) -> None:
        note = replace_section_body(
            NOTE,
            "Learning",
            "A product team learned from repeated setup failures.\n\n"
            "**Source:** Customer discovery interview.\n",
        )
        self.assert_invalid(note, "must not include source, reference, citation")

    def test_rejects_attribution_field(self) -> None:
        note = replace_section_body(
            NOTE,
            "Learning",
            "A product team learned from repeated setup failures.\n\n"
            "Attribution: Customer discovery interview.\n",
        )
        self.assert_invalid(note, "must not include source, reference, citation")

    def test_rejects_based_on_field(self) -> None:
        note = replace_section_body(
            NOTE,
            "Learning",
            "A product team learned from repeated setup failures.\n\n"
            "Based on: Customer discovery interview.\n",
        )
        self.assert_invalid(note, "must not include source, reference, citation")

    def test_rejects_external_source_url(self) -> None:
        note = replace_section_body(
            NOTE,
            "Learning",
            "A product team adopted maintained defaults after repeated setup "
            "failures documented at https://example.com/customer-report.\n",
        )
        self.assert_invalid(note, "must not include external source URLs")

    def test_rejects_external_source_url_inside_fenced_content(self) -> None:
        note = replace_section_body(
            NOTE,
            "Learning",
            "A product team learned from repeated setup failures.\n\n"
            "```text\nhttps://example.com/customer-report\n```\n",
        )
        self.assert_invalid(note, "must not include external source URLs")

    def test_rejects_external_source_url_in_moc_entry(self) -> None:
        moc = MOC.replace(
            "— Decide when a maintained default can remove repeated delivery choices.",
            "— Decide when a maintained default can remove repeated delivery choices "
            "from https://example.com/customer-report.",
        )
        result = run_validator(moc=moc)
        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "MOC entry for the atomic note must not include external source URLs",
            result.stdout,
        )

    def test_rejects_source_attribution_in_moc_entry(self) -> None:
        moc = MOC.replace(
            "— Decide when a maintained default can remove repeated delivery choices.",
            "— Decide when a maintained default can remove repeated delivery choices. "
            "Based on: customer interview.",
        )
        result = run_validator(moc=moc)
        self.assertEqual(result.returncode, 1)
        self.assertIn(
            "MOC entry for the atomic note must not include source attribution",
            result.stdout,
        )

    def test_rejects_each_missing_required_section(self) -> None:
        for section in REQUIRED_SECTIONS:
            with self.subTest(section=section):
                result = run_validator(note=remove_section(NOTE, section))
                self.assertEqual(result.returncode, 1)
                self.assertIn(section.lower(), result.stdout)

    def test_rejects_each_empty_required_section(self) -> None:
        for section in REQUIRED_SECTIONS:
            with self.subTest(section=section):
                note = replace_section_body(NOTE, section, "")
                result = run_validator(note=note)
                self.assertEqual(result.returncode, 1)
                self.assertIn(
                    f'Atomic-note section "{section.lower()}" must not be empty.',
                    result.stdout,
                )

    def test_rejects_required_sections_out_of_order(self) -> None:
        practice = re.search(
            r"\n## Practice\n.*?(?=\n## )", NOTE, re.DOTALL
        ).group(0)
        mechanism = re.search(
            r"\n## Why it works\n.*?(?=\n## )", NOTE, re.DOTALL
        ).group(0)
        note = NOTE.replace(practice + mechanism, mechanism + practice)
        self.assert_invalid(note, "must follow this order")

    def test_rejects_duplicate_required_section(self) -> None:
        note = NOTE.replace(
            "\n## Relationships",
            "\n## Constraints\n\n- A second constraint.\n\n## Relationships",
        )
        self.assert_invalid(note, "repeats section(s): constraints")

    def test_rejects_unexpected_section(self) -> None:
        note = NOTE.replace(
            "\n## Constraints",
            "\n## Benefits\n\nFaster setup.\n\n## Constraints",
        )
        self.assert_invalid(note, "unexpected section(s): benefits")

    def test_requires_when_do_because_pattern_form(self) -> None:
        note = replace_section_body(
            NOTE,
            "Pattern",
            "Golden paths reduce repeated decisions for delivery teams.\n",
        )
        self.assert_invalid(note, 'one "When X, do Y, because Z." sentence')

    def test_rejects_multiple_lines_in_pattern(self) -> None:
        note = replace_section_body(
            NOTE,
            "Pattern",
            "When teams repeat decisions, provide a default, because it saves attention.\n"
            "This is a second sentence.\n",
        )
        self.assert_invalid(note, 'one "When X, do Y, because Z." sentence')

    def test_rejects_multiple_sentences_on_one_pattern_line(self) -> None:
        note = replace_section_body(
            NOTE,
            "Pattern",
            "When teams repeat decisions, provide a default, because it saves attention. Keep it maintained.\n",
        )
        self.assert_invalid(note, 'one "When X, do Y, because Z." sentence')

    def test_accepts_blockquoted_pattern(self) -> None:
        note = replace_section_body(
            NOTE,
            "Pattern",
            "> When teams repeat decisions, provide a default, because it saves attention.\n",
        )
        result = run_validator(note=note)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_requires_bullets_in_structured_action_sections(self) -> None:
        for section in ("Practice", "Signals", "Constraints"):
            with self.subTest(section=section):
                note = replace_section_body(
                    NOTE, section, "Describe this only as prose.\n"
                )
                self.assert_invalid(
                    note,
                    f'Atomic-note section "{section.lower()}" requires at least one bullet.',
                )

    def test_requires_typed_relationship(self) -> None:
        note = NOTE.replace("- Extension:", "- Related:")
        self.assert_invalid(note, "requires a supported type")

    def test_requires_relationship_explanation(self) -> None:
        note = replace_section_body(
            NOTE,
            "Relationships",
            "- Extension: [Platform teams as products](platform-team-as-a-product.md)\n",
        )
        self.assert_invalid(note, "requires explanatory prose")

    def test_rejects_relationship_placeholders(self) -> None:
        note = replace_section_body(
            NOTE,
            "Relationships",
            "- Prerequisite:\n- Extension:\n- Contrast:\n- Example:\n",
        )
        self.assert_invalid(note, "typed links or state")

    def test_rejects_dangling_relationship_link(self) -> None:
        result = run_validator(linked_files=())
        self.assertEqual(result.returncode, 1)
        self.assertIn("unresolved internal link", result.stdout)

    def test_accepts_full_marp_markdown_link_in_moc(self) -> None:
        moc = (
            MOC
            + "\n## Presentation\n\n"
            "[Domain presentation](platform.marp.md) presents these patterns together.\n"
        )
        result = run_validator(
            moc=moc,
            linked_files=("platform-team-as-a-product.md", "platform.marp.md"),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_ignores_headings_and_links_inside_fenced_code(self) -> None:
        note = replace_section_body(
            NOTE,
            "Learning",
            "Teams learned from repeated setup failures.\n\n"
            "```markdown\n# Example\n[Missing](missing-note.md)\n```\n",
        )
        result = run_validator(note=note)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_root_absolute_markdown_link(self) -> None:
        note = NOTE.replace(
            "platform-team-as-a-product.md",
            "/elsewhere/platform-team-as-a-product.md",
        )
        self.assert_invalid(note, "flat lowercase kebab-case")

    def test_accepts_wiki_style_links_for_compatible_pkm_tools(self) -> None:
        note = NOTE.replace("[Platform](platform-moc.md)", "[[platform-moc]]").replace(
            "[Platform teams as products](platform-team-as-a-product.md)",
            "[[platform-team-as-a-product|Platform teams as products]]",
        )
        moc = MOC.replace(
            "[Golden paths reduce cognitive load](platform-golden-paths-reduce-cognitive-load.md)",
            "[[platform-golden-paths-reduce-cognitive-load|Golden paths reduce cognitive load]]",
        )
        result = run_validator(note=note, moc=moc)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_tool_specific_wiki_transclusions(self) -> None:
        note = NOTE.replace(
            "[Platform teams as products](platform-team-as-a-product.md)",
            "![[platform-team-as-a-product]]",
        )
        self.assert_invalid(note, "wiki transclusions")

    def test_rejects_uppercase_markdown_extension(self) -> None:
        note = NOTE.replace("platform-moc.md", "platform-moc.MD")
        self.assert_invalid(note, "Markdown .md filename")

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

    def test_requires_exact_parent_moc(self) -> None:
        note = NOTE.replace(
            "[Platform](platform-moc.md)", "[Other](other-moc.md)", 1
        )
        self.assert_invalid(note, "Parent must contain exactly")

    def test_rejects_multiple_parent_mocs(self) -> None:
        note = NOTE.replace(
            "Parent: [Platform](platform-moc.md)",
            "Parent: [Platform](platform-moc.md) [Leadership](leadership-moc.md)",
        )
        self.assert_invalid(
            note,
            "exactly the supplied MOC",
            linked_files=("platform-team-as-a-product.md", "leadership-moc.md"),
        )

    def test_requires_tag_categories(self) -> None:
        note = NOTE.replace("#platform #draft #private", "#draft")
        result = run_validator(note=note)
        self.assertEqual(result.returncode, 1)
        self.assertIn("visibility tag", result.stdout)
        self.assertIn("domain tag", result.stdout)

    def test_does_not_treat_coaching_as_a_domain_tag(self) -> None:
        note = NOTE.replace(
            "#platform #draft #private",
            "#coaching #draft #private",
        )
        self.assert_invalid(note, "domain tag")

    def test_rejects_multiple_workflow_tags(self) -> None:
        note = NOTE.replace(
            "#platform #draft #private", "#platform #draft #review #private"
        )
        self.assert_invalid(note, "exactly one workflow")

    def test_requires_moc_filter_tags(self) -> None:
        result = run_validator(moc=MOC.replace(" #draft #private", ""))
        self.assertEqual(result.returncode, 1)
        self.assertIn("MOC tags must include one workflow", result.stdout)
        self.assertIn("MOC tags must include one visibility", result.stdout)

    def test_requires_descriptive_moc_entry(self) -> None:
        moc = MOC.replace(
            "- [Golden paths reduce cognitive load](platform-golden-paths-reduce-cognitive-load.md) — Decide when a maintained default can remove repeated delivery choices.",
            "- [Golden paths reduce cognitive load](platform-golden-paths-reduce-cognitive-load.md)",
        )
        result = run_validator(moc=moc)
        self.assertEqual(result.returncode, 1)
        self.assertIn("navigation description", result.stdout)

    def test_requires_moc_entry_inside_notes_section(self) -> None:
        moc = MOC.replace(
            "Reusable patterns for internal platforms.",
            "Reusable patterns such as [golden paths](platform-golden-paths-reduce-cognitive-load.md).",
        ).replace(
            "- [Golden paths reduce cognitive load](platform-golden-paths-reduce-cognitive-load.md) — Decide when a maintained default can remove repeated delivery choices.",
            "- [Platform teams as products](platform-team-as-a-product.md) — Run the platform with product ownership.",
        )
        result = run_validator(moc=moc)
        self.assertEqual(result.returncode, 1)
        self.assertIn("MOC must link to the atomic note", result.stdout)

    def test_rejects_empty_state_with_atomic_note_entry(self) -> None:
        result = run_validator(
            moc=MOC.replace("## Notes\n", "## Notes\n\nNo atomic notes yet.\n")
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("cannot combine", result.stdout)

    def test_rejects_non_atomic_moc_entries(self) -> None:
        moc = (
            MOC
            + "\n- [Coaching guidance]"
            "(platform-golden-paths-reduce-cognitive-load.coach.md) "
            "supports applying the pattern.\n"
        )
        result = run_validator(
            moc=moc,
            linked_files=(
                "platform-team-as-a-product.md",
                "platform-golden-paths-reduce-cognitive-load.coach.md",
            ),
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("only to atomic notes", result.stdout)


if __name__ == "__main__":
    unittest.main()
