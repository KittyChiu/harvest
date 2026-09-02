#!/usr/bin/env python3
"""Regression tests for the coaching-companion validator."""

from __future__ import annotations

import re
import subprocess
import tempfile
import unittest
from pathlib import Path


VALIDATOR = Path(__file__).with_name("validate_coaching_note.py")
TEMPLATE = (
    Path(__file__).parents[1] / "assets" / "coaching-note-template.md"
).read_text(encoding="utf-8")
REQUIRED_SECTIONS = (
    "Teach",
    "Watch for",
    "Conversation",
    "Exercise",
    "Adoption",
    "Progress signals",
    "Common resistance",
)
ADOPTION_SUBSECTIONS = ("Start", "Continue", "Stop")

ATOMIC = """# Sharing knowledge creates reusable team memory

Parent: [Culture](culture-moc.md)
Tags: #leadership #draft #private

## Pattern

When teams repeatedly rediscover knowledge, capture reusable decisions together, because shared context reduces avoidable relearning.

## Practice

- Record one reusable decision where the team can find it.

## Why it works

Shared context lets later work start from established learning.

## Signals

- The same question is answered repeatedly.

## Learning

Teams reused concise decision notes more often than private meeting records.

## Constraints

- Sensitive information still requires access controls.

## Relationships

No supported relationships yet.
"""

COACH = """# Coaching companion: Sharing knowledge creates reusable team memory

Parent: [Culture](culture-moc.md)
Companion to: [Sharing knowledge creates reusable team memory](culture-sharing-creates-team-memory.md)

Tags: #leadership #coaching #draft #private

## Teach

Shared notes preserve decisions that a team would otherwise have to rediscover.

- The idea is to capture reusable learning together.
- It matters when repeated discovery consumes attention.
- It corrects the misconception that every written record is equally reusable.

## Watch for

- The same question is answered in multiple meetings.
- Decisions live only in private notes.
- New team members repeat resolved investigations.

## Conversation

- Which knowledge did the team need more than once this month?
- What makes a note safe and useful for this team to reuse?
- Where could one small sharing experiment fit current work?

## Exercise

Turn one recent decision into a reusable note.

Steps:
1. Choose a decision the team is likely to revisit.
2. Capture the decision, context, and constraint in a shared location.
3. Ask a teammate whether the note answers their likely follow-up question.

Expected outcome:

One concise note and one piece of feedback about its reusability.

## Adoption

### Start

- Share one reusable decision each week.

### Continue

- Preserve access controls for sensitive context.

### Stop

- Treating private meeting notes as the default team memory.

## Progress signals

- Observe whether teammates can find prior decisions.
- Improvement looks like fewer repeated investigations.
- Reuse alone cannot prove that the notes are accurate or safe.

## Common resistance

Explore the cost or concern behind resistance before changing the practice.

| Resistance | Response |
|------------|----------|
| Writing takes too long. | Start with one decision and remove unnecessary formatting. |
"""


def run_validator(
    atomic: str = ATOMIC,
    coach: str = COACH,
    atomic_name: str = "culture-sharing-creates-team-memory.md",
    coach_name: str = "culture-sharing-creates-team-memory.coach.md",
    separate_directories: bool = False,
    linked_files: tuple[str, ...] = (),
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
        for filename in linked_files:
            (root / filename).write_text("# Existing artifact\n", encoding="utf-8")
        return subprocess.run(
            ["python3", str(VALIDATOR), str(atomic_path), str(coach_path)],
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


class ValidateCoachingNoteTests(unittest.TestCase):
    def assert_invalid(
        self, coach: str, message: str, **kwargs: object
    ) -> None:
        result = run_validator(coach=coach, **kwargs)
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn(message, result.stdout)

    def test_accepts_completed_coaching_companion(self) -> None:
        result = run_validator()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("0 error(s)", result.stdout)

    def test_template_defines_exact_schema(self) -> None:
        h2 = re.findall(r"^##\s+(.+?)\s*$", TEMPLATE, re.MULTILINE)
        h3 = re.findall(r"^###\s+(.+?)\s*$", TEMPLATE, re.MULTILINE)
        self.assertEqual(h2, list(REQUIRED_SECTIONS))
        self.assertEqual(h3, list(ADOPTION_SUBSECTIONS))
        self.assertTrue(TEMPLATE.endswith("\n"))

    def test_template_is_scaffold_not_completed_note(self) -> None:
        coach = (
            TEMPLATE.replace(
                "Atomic pattern title",
                "Sharing knowledge creates reusable team memory",
            )
            .replace("Domain name", "Culture")
            .replace("domain-moc.md", "culture-moc.md")
            .replace(
                "domain-atomic-note.md",
                "culture-sharing-creates-team-memory.md",
            )
            .replace("#domain", "#leadership")
        )
        result = run_validator(coach=coach)
        self.assertEqual(result.returncode, 1)
        self.assertIn("unreplaced template prompt(s)", result.stdout)
        self.assertIn("Conversation requires", result.stdout)
        self.assertIn("three populated steps", result.stdout)
        self.assertIn("populated Expected outcome", result.stdout)
        self.assertIn("at least one populated row", result.stdout)

    def test_rejects_prompt_left_in_completed_structure(self) -> None:
        coach = COACH.replace(
            "- The same question is answered in multiple meetings.",
            "- Observable behaviour",
        )
        self.assert_invalid(coach, "unreplaced template prompt(s)")

    def test_rejects_each_missing_required_section(self) -> None:
        for section in REQUIRED_SECTIONS:
            with self.subTest(section=section):
                result = run_validator(coach=remove_section(COACH, section))
                self.assertEqual(result.returncode, 1)
                self.assertIn(section.lower(), result.stdout)

    def test_rejects_each_empty_required_section(self) -> None:
        for section in REQUIRED_SECTIONS:
            with self.subTest(section=section):
                coach = replace_section_body(COACH, section, "")
                result = run_validator(coach=coach)
                self.assertEqual(result.returncode, 1)
                self.assertIn(
                    f'Coaching-note section "{section.lower()}" must not be empty.',
                    result.stdout,
                )

    def test_rejects_required_sections_out_of_order(self) -> None:
        watch = re.search(
            r"\n## Watch for\n.*?(?=\n## )", COACH, re.DOTALL
        ).group(0)
        conversation = re.search(
            r"\n## Conversation\n.*?(?=\n## )", COACH, re.DOTALL
        ).group(0)
        coach = COACH.replace(watch + conversation, conversation + watch)
        self.assert_invalid(coach, "must follow this order")

    def test_rejects_duplicate_required_section(self) -> None:
        coach = COACH.replace(
            "\n## Common resistance",
            "\n## Progress signals\n\n- A duplicate.\n\n## Common resistance",
        )
        self.assert_invalid(coach, "repeats section(s): progress signals")

    def test_rejects_unexpected_section(self) -> None:
        coach = COACH.replace(
            "\n## Common resistance",
            "\n## Rollout\n\nDeploy everywhere.\n\n## Common resistance",
        )
        self.assert_invalid(coach, "unexpected section(s): rollout")

    def test_requires_coaching_companion_title(self) -> None:
        self.assert_invalid(
            COACH.replace(
                "# Coaching companion:",
                "# Coaching:",
                1,
            ),
            'must use "Coaching companion:',
        )

    def test_requires_watch_for_bullet(self) -> None:
        coach = replace_section_body(
            COACH,
            "Watch for",
            "The same question is answered repeatedly.\n",
        )
        self.assert_invalid(coach, '"watch for" requires at least one bullet')

    def test_requires_exactly_three_conversation_questions(self) -> None:
        coach = COACH.replace(
            "- Where could one small sharing experiment fit current work?\n",
            "",
        )
        self.assert_invalid(coach, "exactly three bullet questions")

    def test_requires_question_marks_on_conversation_questions(self) -> None:
        coach = COACH.replace(
            "- What makes a note safe and useful for this team to reuse?",
            "- Describe what makes a note safe and useful for this team.",
        )
        self.assert_invalid(coach, "questions ending in ?")

    def test_requires_three_populated_exercise_steps(self) -> None:
        coach = COACH.replace(
            "2. Capture the decision, context, and constraint in a shared location.",
            "2.",
        )
        self.assert_invalid(coach, "three populated steps numbered 1, 2, 3")

    def test_requires_steps_label(self) -> None:
        coach = COACH.replace("Steps:", "Actions:", 1)
        self.assert_invalid(coach, "three populated steps numbered 1, 2, 3")

    def test_rejects_extra_exercise_step(self) -> None:
        coach = COACH.replace(
            "\nExpected outcome:",
            "\n4. Publish the note to every team.\n\nExpected outcome:",
        )
        self.assert_invalid(coach, "three populated steps numbered 1, 2, 3")

    def test_requires_populated_expected_outcome(self) -> None:
        coach = re.sub(
            r"Expected outcome:\n\n.*?(?=\n## Adoption)",
            "Expected outcome:\n",
            COACH,
            flags=re.DOTALL,
        )
        self.assert_invalid(coach, "populated Expected outcome")

    def test_requires_each_adoption_subsection(self) -> None:
        coach = re.sub(
            r"\n### Continue\n.*?(?=\n### |\n## )",
            "",
            COACH,
            flags=re.DOTALL,
        )
        self.assert_invalid(coach, "Adoption is missing subsection(s): continue")

    def test_requires_adoption_subsections_in_order(self) -> None:
        adoption = re.search(
            r"\n## Adoption\n.*?(?=\n## )", COACH, re.DOTALL
        ).group(0)
        start = re.search(
            r"\n### Start\n.*?(?=\n### )", adoption, re.DOTALL
        ).group(0)
        continuing = re.search(
            r"\n### Continue\n.*?(?=\n### )", adoption, re.DOTALL
        ).group(0)
        coach = COACH.replace(
            start + continuing,
            continuing + start,
        )
        self.assert_invalid(coach, "Adoption subsections must follow this order")

    def test_rejects_duplicate_adoption_subsection(self) -> None:
        coach = COACH.replace(
            "\n### Stop",
            "\n### Continue\n\n- Preserve another behaviour.\n\n### Stop",
        )
        self.assert_invalid(coach, "Adoption repeats subsection(s): continue")

    def test_rejects_unexpected_adoption_subsection(self) -> None:
        coach = COACH.replace(
            "\n### Stop",
            "\n### Mandate\n\n- Force adoption.\n\n### Stop",
        )
        self.assert_invalid(coach, "Adoption has unexpected subsection(s): mandate")

    def test_requires_populated_adoption_bullet(self) -> None:
        coach = COACH.replace(
            "- Preserve access controls for sensitive context.",
            "Preserve access controls for sensitive context.",
        )
        self.assert_invalid(
            coach,
            'Adoption subsection "continue" requires at least one populated bullet',
        )

    def test_requires_three_progress_signal_bullets(self) -> None:
        coach = COACH.replace(
            "- Reuse alone cannot prove that the notes are accurate or safe.\n",
            "",
        )
        self.assert_invalid(coach, "Progress signals requires at least three bullets")

    def test_requires_resistance_response_table(self) -> None:
        coach = replace_section_body(
            COACH,
            "Common resistance",
            "Explore resistance through conversation.\n",
        )
        self.assert_invalid(coach, "Resistance | Response table")

    def test_requires_populated_resistance_response_row(self) -> None:
        coach = COACH.replace(
            "| Writing takes too long. | Start with one decision and remove unnecessary formatting. |",
            "| | |",
        )
        self.assert_invalid(coach, "at least one populated row")

    def test_ignores_headings_and_links_inside_fenced_code(self) -> None:
        coach = COACH.replace(
            "Shared notes preserve decisions that a team would otherwise have to rediscover.",
            "Shared notes preserve decisions that a team would otherwise have to rediscover.\n\n"
            "```markdown\n# Example\n[Missing](missing-note.md)\n```",
        )
        result = run_validator(coach=coach)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_accepts_standard_url_and_email_autolinks(self) -> None:
        coach = COACH.replace(
            "Explore the cost or concern behind resistance before changing the practice.",
            "Explore the concern with <https://example.com> or <coach@example.com>.",
        )
        result = run_validator(coach=coach)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_root_absolute_markdown_link(self) -> None:
        coach = COACH.replace(
            "Explore the cost or concern behind resistance",
            "Use [outside guidance](/etc/guidance.md) and explore resistance",
        )
        self.assert_invalid(coach, "flat lowercase kebab-case")

    def test_accepts_wiki_style_links_for_compatible_pkm_tools(self) -> None:
        atomic = ATOMIC.replace("[Culture](culture-moc.md)", "[[culture-moc]]")
        coach = COACH.replace("[Culture](culture-moc.md)", "[[culture-moc]]").replace(
            "[Sharing knowledge creates reusable team memory](culture-sharing-creates-team-memory.md)",
            "[[culture-sharing-creates-team-memory|Sharing knowledge creates reusable team memory]]",
        )
        result = run_validator(atomic=atomic, coach=coach)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_accepts_full_marp_markdown_link(self) -> None:
        coach = COACH.replace(
            "Shared notes preserve decisions that a team would otherwise have to rediscover.",
            "The [domain presentation](culture.marp.md) introduces the pattern.",
        )
        result = run_validator(
            coach=coach,
            linked_files=("culture.marp.md",),
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_tool_specific_wiki_transclusions(self) -> None:
        coach = COACH.replace(
            "[Sharing knowledge creates reusable team memory](culture-sharing-creates-team-memory.md)",
            "![[culture-sharing-creates-team-memory]]",
        )
        self.assert_invalid(coach, "wiki transclusions")

    def test_rejects_uppercase_markdown_extension(self) -> None:
        coach = COACH.replace("culture-moc.md", "culture-moc.MD")
        self.assert_invalid(coach, "Markdown .md filename")

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
        coach = COACH.replace(
            "[Culture](culture-moc.md)",
            "[Other](other-moc.md)",
            1,
        )
        self.assert_invalid(coach, "Parent MOC")

    def test_requires_atomic_companion_link(self) -> None:
        coach = COACH.replace(
            "[Sharing knowledge creates reusable team memory](culture-sharing-creates-team-memory.md)",
            "[Another note](another-note.md)",
        )
        self.assert_invalid(coach, "Companion to")

    def test_requires_coaching_and_filter_tags(self) -> None:
        coach = COACH.replace(
            "#leadership #coaching #draft #private",
            "#coaching #draft",
        )
        result = run_validator(coach=coach)
        self.assertEqual(result.returncode, 1)
        self.assertIn("visibility tag", result.stdout)
        self.assertIn("domain tag", result.stdout)

    def test_rejects_multiple_workflow_tags(self) -> None:
        coach = COACH.replace(
            "#leadership #coaching #draft #private",
            "#leadership #coaching #draft #review #private",
        )
        self.assert_invalid(coach, "exactly one workflow tag")

    def test_requires_atomic_note_domain_tags(self) -> None:
        coach = COACH.replace(
            "#leadership #coaching #draft #private",
            "#platform #coaching #draft #private",
        )
        self.assert_invalid(coach, "#leadership")

    def test_rejects_dangling_internal_links(self) -> None:
        coach = COACH.replace(
            "Explore the cost or concern behind resistance",
            "Use [a missing playbook](missing-playbook.md) to explore resistance",
        )
        self.assert_invalid(coach, "unresolved internal link")


if __name__ == "__main__":
    unittest.main()
