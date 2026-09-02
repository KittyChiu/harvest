#!/usr/bin/env python3
"""Regression tests for the coaching-note validator."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


VALIDATOR = Path(__file__).with_name("validate_coaching_note.py")
TEMPLATE = (
    Path(__file__).parents[1] / "assets" / "coaching-note-template.md"
).read_text(encoding="utf-8")

ATOMIC = """# Sharing knowledge creates reusable team memory

Parent: [Culture](culture-moc.md)
Tags: #leadership #draft #private

## Core idea
Shared notes let teams reuse learning.
"""

COACH = """# Coaching: Sharing knowledge creates reusable team memory

Parent: [Culture](culture-moc.md)
Companion to: [Sharing creates team memory](culture-sharing-creates-team-memory.md)
Tags: #leadership #coaching #draft #private

## Coaching intent

Help the team make useful sharing easier and safer.

## Consider

- Explore psychological safety and available time.

## Start, continue, stop

**Start:** Share one useful decision in the team repository.

**Continue:** Recognize constructive peer feedback.

**Stop:** Keeping reusable learning in private folders by default.

## Questions

- What knowledge did the team need twice this month?

## Signals and metrics

- Review reuse and participant sentiment together.

## Resistance and support

Reduce friction with examples and a small experiment before changing policy.
"""


def run_validator(
    atomic: str = ATOMIC,
    coach: str = COACH,
    atomic_name: str = "culture-sharing-creates-team-memory.md",
    coach_name: str = "culture-sharing-creates-team-memory.coach.md",
    separate_directories: bool = False,
) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        atomic_path = root / atomic_name
        coach_directory = root / "other" if separate_directories else root
        coach_directory.mkdir(exist_ok=True)
        coach_path = coach_directory / coach_name
        atomic_path.write_text(atomic, encoding="utf-8")
        coach_path.write_text(coach, encoding="utf-8")
        (root / "culture-moc.md").write_text("# Culture\n", encoding="utf-8")
        return subprocess.run(
            ["python3", str(VALIDATOR), str(atomic_path), str(coach_path)],
            capture_output=True,
            check=False,
            text=True,
        )


class ValidateCoachingNoteTests(unittest.TestCase):
    def test_accepts_coaching_companion(self) -> None:
        result = run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 error(s)", result.stdout)

    def test_shipped_template_contains_valid_questions(self) -> None:
        coach = (
            TEMPLATE.replace("Domain name", "Culture")
            .replace("domain-moc.md", "culture-moc.md")
            .replace("Atomic idea title", "Sharing creates team memory")
            .replace("domain-atomic-note.md", "culture-sharing-creates-team-memory.md")
            .replace("#domain", "#leadership")
        )
        result = run_validator(coach=coach)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_ignores_headings_and_links_inside_fenced_code(self) -> None:
        coach = COACH.replace(
            "- Explore psychological safety and available time.",
            "- Explore psychological safety and available time.\n\n"
            "```markdown\n# Example\n[Missing](missing-note.md)\n```",
        )
        result = run_validator(coach=coach)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_root_absolute_markdown_link(self) -> None:
        coach = COACH.replace(
            "Reduce friction with examples",
            "Use [outside guidance](/etc/guidance.md) and examples",
        )
        result = run_validator(coach=coach)
        self.assertEqual(result.returncode, 1)
        self.assertIn("flat lowercase kebab-case", result.stdout)

    def test_accepts_wiki_style_links_for_compatible_pkm_tools(self) -> None:
        atomic = ATOMIC.replace("[Culture](culture-moc.md)", "[[culture-moc]]")
        coach = COACH.replace("[Culture](culture-moc.md)", "[[culture-moc]]").replace(
            "[Sharing creates team memory](culture-sharing-creates-team-memory.md)",
            "[[culture-sharing-creates-team-memory]]",
        )
        result = run_validator(atomic=atomic, coach=coach)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_tool_specific_wiki_transclusions(self) -> None:
        result = run_validator(
            coach=COACH.replace(
                "[Sharing creates team memory](culture-sharing-creates-team-memory.md)",
                "![[culture-sharing-creates-team-memory]]",
            )
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("wiki transclusions", result.stdout)

    def test_rejects_uppercase_markdown_extension(self) -> None:
        result = run_validator(coach=COACH.replace("culture-moc.md", "culture-moc.MD"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("Markdown .md filename", result.stdout)

    def test_requires_existing_files(self) -> None:
        result = subprocess.run(
            ["python3", str(VALIDATOR), "missing.md", "missing.coach.md"],
            capture_output=True,
            check=False,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertIn("File not found", result.stdout)

    def test_requires_companion_filename(self) -> None:
        result = run_validator(coach_name="culture.coach.md")
        self.assertEqual(result.returncode, 1)
        self.assertIn("filename must be", result.stdout)

    def test_requires_same_knowledge_directory(self) -> None:
        result = run_validator(separate_directories=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn("share a knowledge directory", result.stdout)

    def test_requires_same_parent_moc(self) -> None:
        result = run_validator(
            coach=COACH.replace("[Culture](culture-moc.md)", "[Other](other-moc.md)", 1)
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Parent MOC", result.stdout)

    def test_requires_atomic_companion_link(self) -> None:
        result = run_validator(
            coach=COACH.replace(
                "[Sharing creates team memory](culture-sharing-creates-team-memory.md)",
                "[Another note](another-note.md)",
            )
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Companion to", result.stdout)

    def test_requires_coaching_and_filter_tags(self) -> None:
        result = run_validator(
            coach=COACH.replace(
                "#leadership #coaching #draft #private", "#coaching #draft"
            )
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("visibility tag", result.stdout)
        self.assertIn("domain tag", result.stdout)

    def test_requires_atomic_note_domain_tags(self) -> None:
        result = run_validator(
            coach=COACH.replace(
                "#leadership #coaching #draft #private",
                "#platform #coaching #draft #private",
            )
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("#leadership", result.stdout)

    def test_requires_all_coaching_sections(self) -> None:
        result = run_validator(
            coach=COACH.replace("## Resistance and support", "## Rollout")
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("resistance and support", result.stdout)

    def test_requires_start_continue_stop_labels(self) -> None:
        result = run_validator(coach=COACH.replace("**Continue:**", "**Preserve:**"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("**Continue:**", result.stdout)

    def test_requires_open_question(self) -> None:
        result = run_validator(
            coach=COACH.replace(
                "- What knowledge did the team need twice this month?",
                "- Discuss recent knowledge reuse.",
            )
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("open question", result.stdout)

    def test_rejects_dangling_internal_links(self) -> None:
        result = run_validator(
            coach=COACH.replace(
                "Reduce friction with examples",
                "Use [a missing playbook](missing-playbook.md) to reduce friction with examples",
            )
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("unresolved internal link", result.stdout)


if __name__ == "__main__":
    unittest.main()
