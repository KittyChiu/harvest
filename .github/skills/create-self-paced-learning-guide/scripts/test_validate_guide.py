#!/usr/bin/env python3
"""Regression tests for the learning-module validator."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


VALIDATOR = Path(__file__).with_name("validate_guide.py")


def run_validator(
    participant: str,
    coach: str,
    participant_name: str = "focus.participant.guide.md",
    coach_name: str = "focus.coach.guide.md",
) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as directory:
        participant_path = Path(directory) / participant_name
        coach_path = Path(directory) / coach_name
        participant_path.write_text(participant, encoding="utf-8")
        coach_path.write_text(coach, encoding="utf-8")
        return subprocess.run(
            ["python3", str(VALIDATOR), str(participant_path), str(coach_path)],
            capture_output=True,
            check=False,
            text=True,
        )


PARTICIPANT = """# Focus

## Experience

<!-- source: tension -->
Try the task.
"""

COACH = """# Focus: Coach guide

## Coach the journey

<!-- source-coach: caveat -->
Ask what changed.

<!-- source-contract: tension, caveat, further-reading -->
<!-- source-excluded: further-reading | reason: Outside this module's purpose -->
"""


class ValidateModuleTests(unittest.TestCase):
    def test_accepts_matching_participant_and_coach_guides(self) -> None:
        result = run_validator(PARTICIPANT, COACH)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("3 source item(s): 0 unclassified", result.stdout)

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

    def test_rejects_learner_content_in_coach_guide(self) -> None:
        result = run_validator(
            PARTICIPANT,
            COACH + "\n<!-- source: extra -->\n",
        )

        self.assertEqual(result.returncode, 1)
        self.assertIn("learner source markers", result.stdout.lower())

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