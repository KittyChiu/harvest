#!/usr/bin/env python3
"""Regression tests for the domain Marp presentation validator."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("validate_marp_slides.py")


class ValidateMarpSlidesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.moc = self.root / "platform-moc.md"
        self.note_one = self.root / "platform-golden-paths.md"
        self.note_two = self.root / "platform-feedback-loops.md"
        self.coach = self.root / "platform-golden-paths.coach.md"
        self.deck = self.root / "platform.marp.md"
        self.note_one.write_text("# Golden paths\n", encoding="utf-8")
        self.note_two.write_text("# Feedback loops\n", encoding="utf-8")
        self.coach.write_text("# Golden paths coaching\n", encoding="utf-8")
        self.moc.write_text(self.valid_moc(), encoding="utf-8")
        self.deck.write_text(self.valid_deck(), encoding="utf-8")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    @staticmethod
    def valid_moc() -> str:
        return """# Platform

## Scope

Platform practices.

## Notes

- [Golden paths](platform-golden-paths.md) - paved routes for common work.
- [Feedback loops](platform-feedback-loops.md) - use learning to improve routes.

## Related domains

No related domains yet.

Tags: #platform #moc #publish #private
"""

    @staticmethod
    def valid_deck() -> str:
        return """---
marp: true
theme: default
paginate: true
size: 16:9
title: Platform
description: Connect platform practices
---

# Platform as a learning system

MOC: [Platform](platform-moc.md)
Tags: #platform #slides #publish #private

<!--
Coach cue: Ask what makes a platform useful over time.
-->

---

# Golden paths reduce repeated decisions

Source: [Golden paths](platform-golden-paths.md)
Coach source: [Golden paths coaching](platform-golden-paths.coach.md)

<!--
Coach cue: Ask where teams need a paved route rather than another mandate.
-->

---

# Feedback keeps the path relevant

Source: [Feedback loops](platform-feedback-loops.md)

<!--
Coach cue: Invite the audience to identify the signal that would trigger a change.
-->

---

# Connect guidance with learning

<!--
Coach cue: Ask for one next experiment that joins the two ideas.
-->
"""

    def run_validator(
        self, deck: Path | None = None, moc: Path | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(deck or self.deck), str(moc or self.moc)],
            capture_output=True,
            text=True,
            check=False,
        )

    def assert_invalid(self, message: str) -> None:
        result = self.run_validator()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(message, result.stdout)

    def test_accepts_domain_deck_with_all_moc_sources(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("2 atomic sources", result.stdout)
        self.assertIn("1 coaching sources", result.stdout)

    def test_rejects_filename_not_derived_from_moc(self) -> None:
        wrong_deck = self.root / "slides.marp.md"
        wrong_deck.write_text(self.valid_deck(), encoding="utf-8")
        result = self.run_validator(deck=wrong_deck)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Deck filename must be 'platform.marp.md'", result.stdout)

    def test_rejects_missing_atomic_source(self) -> None:
        self.deck.write_text(
            self.valid_deck().replace(
                "Source: [Feedback loops](platform-feedback-loops.md)", ""
            ),
            encoding="utf-8",
        )
        self.assert_invalid("missing atomic Source links")

    def test_rejects_source_outside_moc(self) -> None:
        extra = self.root / "platform-roadmap.md"
        extra.write_text("# Roadmap\n", encoding="utf-8")
        self.deck.write_text(
            self.valid_deck().replace(
                "# Feedback keeps the path relevant",
                "# Feedback keeps the path relevant\n\n"
                "Source: [Roadmap](platform-roadmap.md)",
            ),
            encoding="utf-8",
        )
        self.assert_invalid("Source links outside the MOC")

    def test_rejects_missing_available_coaching_source(self) -> None:
        self.deck.write_text(
            self.valid_deck().replace(
                "Coach source: [Golden paths coaching]"
                "(platform-golden-paths.coach.md)",
                "",
            ),
            encoding="utf-8",
        )
        self.assert_invalid("missing available Coach source links")

    def test_allows_atomic_note_without_coaching_companion(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertNotIn("platform-feedback-loops.coach.md", result.stdout)

    def test_rejects_wrong_moc_link(self) -> None:
        other_moc = self.root / "other-moc.md"
        other_moc.write_text("# Other\n", encoding="utf-8")
        self.deck.write_text(
            self.valid_deck().replace("platform-moc.md", "other-moc.md"),
            encoding="utf-8",
        )
        self.assert_invalid("only MOC field linking exactly")

    def test_rejects_duplicate_moc_fields(self) -> None:
        self.deck.write_text(
            self.valid_deck().replace(
                "MOC: [Platform](platform-moc.md)",
                "MOC: [Platform](platform-moc.md)\n"
                "MOC: [Platform](platform-moc.md)",
            ),
            encoding="utf-8",
        )
        self.assert_invalid("found 2 fields")

    def test_rejects_moc_field_outside_opening_slide(self) -> None:
        self.deck.write_text(
            self.valid_deck()
            .replace("MOC: [Platform](platform-moc.md)\n", "")
            .replace(
                "# Golden paths reduce repeated decisions",
                "# Golden paths reduce repeated decisions\n\n"
                "MOC: [Platform](platform-moc.md)",
            ),
            encoding="utf-8",
        )
        self.assert_invalid("Opening slide must contain")

    def test_accepts_wiki_links_with_markdown_extensions(self) -> None:
        self.moc.write_text(
            self.valid_moc()
            .replace(
                "[Golden paths](platform-golden-paths.md)",
                "[[platform-golden-paths.md|Golden paths]]",
            )
            .replace(
                "[Feedback loops](platform-feedback-loops.md)",
                "[[platform-feedback-loops.md|Feedback loops]]",
            ),
            encoding="utf-8",
        )
        self.deck.write_text(
            self.valid_deck()
            .replace("[Platform](platform-moc.md)", "[[platform-moc.md|Platform]]")
            .replace(
                "[Golden paths](platform-golden-paths.md)",
                "[[platform-golden-paths.md|Golden paths]]",
            )
            .replace(
                "[Golden paths coaching](platform-golden-paths.coach.md)",
                "[[platform-golden-paths.coach.md|Golden paths coaching]]",
            )
            .replace(
                "[Feedback loops](platform-feedback-loops.md)",
                "[[platform-feedback-loops.md|Feedback loops]]",
            ),
            encoding="utf-8",
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_rejects_missing_domain_tag(self) -> None:
        self.deck.write_text(
            self.valid_deck().replace(
                "Tags: #platform #slides #publish #private",
                "Tags: #slides #publish #private",
            ),
            encoding="utf-8",
        )
        self.assert_invalid("every MOC domain tag")

    def test_rejects_coach_source_slide_without_coach_cue(self) -> None:
        self.deck.write_text(
            self.valid_deck().replace(
                "Coach cue: Ask where teams need a paved route rather than another mandate.",
                "Presenter note: Ask where teams need a paved route rather than another mandate.",
            ),
            encoding="utf-8",
        )
        self.assert_invalid("has a Coach source and requires a non-empty")

    def test_accepts_no_speaker_notes_without_coaching_companions(self) -> None:
        self.coach.unlink()
        deck = self.valid_deck().replace(
            "Coach source: [Golden paths coaching](platform-golden-paths.coach.md)\n",
            "",
        )
        deck = re.sub(r"\n?<!--.*?-->\n?", "\n", deck, flags=re.DOTALL)
        self.deck.write_text(deck, encoding="utf-8")
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("0 coaching sources", result.stdout)

    def test_accepts_url_and_email_autolinks(self) -> None:
        self.deck.write_text(
            self.valid_deck().replace(
                "# Connect guidance with learning",
                "# Connect guidance with learning\n\n"
                "See <https://example.com/docs> or contact <coach@example.com>.",
            ),
            encoding="utf-8",
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_rejects_arbitrary_html(self) -> None:
        self.deck.write_text(
            self.valid_deck().replace(
                "# Connect guidance with learning",
                "# Connect guidance with learning\n\n<div>Unsupported layout</div>",
            ),
            encoding="utf-8",
        )
        self.assert_invalid("Arbitrary HTML is not allowed")

    def test_rejects_uppercase_markdown_extension(self) -> None:
        uppercase_note = self.root / "platform-golden-paths.MD"
        uppercase_note.write_text("# Duplicate\n", encoding="utf-8")
        self.deck.write_text(
            self.valid_deck().replace(
                "platform-golden-paths.md", "platform-golden-paths.MD", 1
            ),
            encoding="utf-8",
        )
        self.assert_invalid("lowercase '.md' extension")

    def test_separator_inside_fence_does_not_create_slide(self) -> None:
        self.deck.write_text(
            self.valid_deck().replace(
                "# Connect guidance with learning",
                "# Connect guidance with learning\n\n```\n---\n===\n```",
            ),
            encoding="utf-8",
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("(4 slides,", result.stdout)

    def test_accepts_fence_aware_equals_slide_separator(self) -> None:
        self.deck.write_text(
            self.valid_deck().replace(
                "\n---\n\n# Feedback keeps the path relevant",
                "\n===\n\n# Feedback keeps the path relevant",
            ),
            encoding="utf-8",
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("(4 slides,", result.stdout)

    def test_ignores_fields_links_and_html_inside_fenced_code(self) -> None:
        self.deck.write_text(
            self.valid_deck().replace(
                "# Connect guidance with learning",
                "# Connect guidance with learning\n\n"
                "```markdown\n"
                "MOC: [Example](example-moc.md)\n"
                "Source: [Example](example-note.md)\n"
                "<div>Example HTML</div>\n"
                "```",
            ),
            encoding="utf-8",
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_accepts_case_insensitive_moc_notes_heading(self) -> None:
        self.moc.write_text(
            self.valid_moc().replace("## Notes", "## notes"),
            encoding="utf-8",
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_separator_inside_speaker_note_does_not_create_slide(self) -> None:
        self.deck.write_text(
            self.valid_deck().replace(
                "Coach cue: Ask where teams need a paved route rather than another mandate.",
                "Coach cue: Ask where teams need a paved route.\n"
                "---\n"
                "Then continue the discussion.",
            ),
            encoding="utf-8",
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("(4 slides,", result.stdout)

    def test_rejects_moc_atomic_link_outside_domain(self) -> None:
        other_note = self.root / "leadership-feedback.md"
        other_note.write_text("# Feedback\n", encoding="utf-8")
        self.moc.write_text(
            self.valid_moc().replace(
                "platform-feedback-loops.md", "leadership-feedback.md"
            ),
            encoding="utf-8",
        )
        self.assert_invalid("is not an atomic note in domain 'platform'")


if __name__ == "__main__":
    unittest.main()
