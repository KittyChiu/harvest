#!/usr/bin/env python3
"""Regression tests for the learning-module validator."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


VALIDATOR = Path(__file__).with_name("validate_module.py")


def run_validator(
    participant: str,
    coach: str,
    participant_name: str = "focus.participant.guide.md",
    coach_name: str = "focus.coach.guide.md",
    coach_subdirectory: str | None = None,
) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        participant_path = Path(directory) / participant_name
        coach_directory = Path(directory)
        if coach_subdirectory:
            coach_directory /= coach_subdirectory
            coach_directory.mkdir()
        coach_path = coach_directory / coach_name
        participant_path.write_text(participant, encoding="utf-8")
        coach_path.write_text(coach, encoding="utf-8")
        return subprocess.run(
            ["python3", str(VALIDATOR), str(participant_path), str(coach_path)],
            capture_output=True,
            check=False,
            text=True,
        )


PARTICIPANT = """# Focus

## Scenario

<!-- source: tension -->
Try the task.

## Exercise

Follow the steps to learn the key idea.

## Reflection

Connect the idea to your experience.

## Takeaways and next step

Choose one action.
"""

COACH = """# Focus: Coach guide

## Coach the journey

### 1. Scenario

<!-- source-coach: caveat -->

- Ask what changed.

### 2. Exercise

- Listen for the key idea.

### 3. Reflection

- Check the learner's output.

### 4. Takeaways and next step

- Ask for one next action.

<!-- source-contract: tension, caveat, further-reading -->
<!-- source-excluded: further-reading | reason: Outside this module's purpose -->
"""


class ValidateModuleTests(unittest.TestCase):
    def test_accepts_matching_participant_and_coach_guides(self) -> None:
        result = run_validator(PARTICIPANT, COACH)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("3 source item(s): 0 unclassified", result.stdout)

    def test_accepts_brief_participant_tip(self) -> None:
        result = run_validator(
            PARTICIPANT + "\n> **Tip:** Use a current task.\n",
            COACH,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_requires_participant_guide_extension(self) -> None:
        result = run_validator(
            PARTICIPANT,
            COACH,
            participant_name="focus.guide.md",
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn(".participant.guide.md", result.stdout)

    def test_requires_coach_guide_extension(self) -> None:
        result = run_validator(PARTICIPANT, COACH, coach_name="focus.guide.md")

        self.assertEqual(result.returncode, 1)
        self.assertIn(".coach.guide.md", result.stdout)

    def test_requires_matching_module_stems(self) -> None:
        result = run_validator(
            PARTICIPANT,
            COACH,
            coach_name="another.coach.guide.md",
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("matching module stems", result.stdout)

    def test_requires_same_output_directory(self) -> None:
        result = run_validator(
            PARTICIPANT,
            COACH,
            coach_subdirectory="coach",
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("same output directory", result.stdout)

    def test_rejects_contract_in_participant_guide(self) -> None:
        result = run_validator(
            PARTICIPANT + "\n<!-- source-contract: tension -->\n",
            COACH,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("participant guide must not contain", result.stdout.lower())

    def test_rejects_coach_content_in_participant_guide(self) -> None:
        result = run_validator(
            PARTICIPANT + "\n<!-- source-coach: caveat -->\n",
            COACH,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("coach source markers", result.stdout.lower())

    def test_rejects_visible_coaching_sections_in_participant_guide(self) -> None:
        result = run_validator(
            PARTICIPANT + "\n## Appendix: Coach guide\n",
            COACH,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("coaching sections", result.stdout.lower())

    def test_rejects_learner_content_in_coach_guide(self) -> None:
        result = run_validator(
            PARTICIPANT,
            COACH + "\n<!-- source: extra -->\n",
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("learner source markers", result.stdout.lower())

    def test_rejects_coach_stage_table(self) -> None:
        result = run_validator(
            PARTICIPANT,
            COACH
            + "\n| Stage | Ask | Listen for |\n|---|---|---|\n| Apply | Why? | Evidence |\n",
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("stage table", result.stdout.lower())

    def test_requires_numbered_coach_stage_headings(self) -> None:
        result = run_validator(
            PARTICIPANT,
            COACH.replace(
                "### 3. Reflection\n",
                "### Reflection\n",
            ),
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("### 3. Reflection", result.stdout)

    def test_requires_plain_english_participant_headings(self) -> None:
        result = run_validator(
            PARTICIPANT.replace(
                "## Reflection\n", "## Apply\n"
            ),
            COACH,
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("## Reflection", result.stdout)

    def test_rejects_unclassified_source_item_across_pair(self) -> None:
        result = run_validator(
            PARTICIPANT,
            COACH.replace("<!-- source-coach: caveat -->\n", ""),
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("caveat", result.stdout)

    def test_accepts_legacy_disposition_aliases(self) -> None:
        participant = PARTICIPANT.replace("source: tension", "canonical: tension")
        coach = COACH.replace(
            "source-coach: caveat", "canonical-facilitator: caveat"
        )
        result = run_validator(participant, coach)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_rejects_exclusion_without_reason(self) -> None:
        result = run_validator(
            PARTICIPANT,
            COACH.replace(
                "source-excluded: further-reading | reason: Outside this module's purpose",
                "source-excluded: further-reading",
            ),
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("without a reason", result.stdout)

    def test_rejects_conflicting_dispositions(self) -> None:
        result = run_validator(
            PARTICIPANT,
            COACH + "\n<!-- source-coach: tension -->\n",
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("multiple dispositions", result.stdout)

    def test_rejects_missing_source_contract(self) -> None:
        result = run_validator(
            PARTICIPANT,
            COACH.replace(
                "<!-- source-contract: tension, caveat, further-reading -->\n", ""
            ),
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("requires a non-empty source-contract", result.stdout)


if __name__ == "__main__":
    unittest.main()