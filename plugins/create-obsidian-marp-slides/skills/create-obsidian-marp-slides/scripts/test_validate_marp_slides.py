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
TEMPLATE = (
    Path(__file__).parents[1] / "assets" / "slides-template.md"
).read_text(encoding="utf-8")


class ValidateMarpSlidesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.moc = self.root / "platform-moc.md"
        self.note_one = self.root / "platform-golden-paths.md"
        self.note_two = self.root / "platform-feedback-loops.md"
        self.coach = self.root / "platform-golden-paths.coach.md"
        self.deck = self.root / "platform.marp.md"
        self.note_one.write_text(
            "# Golden paths\n\n"
            "## Relationships\n\n"
            "- Extension: [Feedback loops](platform-feedback-loops.md) "
            "keeps the maintained path responsive to real use.\n",
            encoding="utf-8",
        )
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
title: Platform patterns
description: Present platform delivery as a connected learning system
---

<!-- markdownlint-disable MD001 MD024 MD025 -->

# Platform delivery

## Make common delivery work easier to start and improve

Connect maintained defaults with learning from real use.

MOC: [Platform](platform-moc.md)
Tags: #platform #slides #publish #private

---

# Challenges & opportunities

## Challenges

- Teams repeat common setup decisions.
- Repeated choices delay product work.

## Opportunities

- Maintained defaults preserve attention.
- Feedback keeps defaults relevant.

> **Domain question:** How can teams reduce repeated decisions without freezing learning?

---

# Pattern map

```text
Platform delivery
├── Delivery defaults
│   └── P1 · Golden paths
└── Learning loops
    └── P2 · Feedback loops

P1 · Golden paths --enables--> P2 · Feedback loops
```

---

###### PATTERN P1 OF 2 · Delivery defaults

# P1 · Golden paths

> **When teams repeat common setup decisions, provide a maintained default, because it preserves attention for product work.**

## Use it when

- Teams repeatedly rebuild the same delivery setup.
- Product work waits on avoidable platform choices.

## Practices

1. Automate the common path.
2. Document a supported exception.

**Related:** P2 · Feedback loops through **enables**

Source: [Golden paths](platform-golden-paths.md)
Coach: [Golden paths coaching](platform-golden-paths.coach.md)

<!--
Coach cue: Where does repeated setup work consume the most attention?
-->

---

###### PATTERN P2 OF 2 · Learning loops

# P2 · Feedback loops

> **When a default no longer fits current work, collect feedback, because real use reveals where the path needs to change.**

## Use it when

- Teams leave the default for similar reasons.
- Workarounds recur across products.

## Practices

1. Review why teams choose exceptions.
2. Update the common path when evidence repeats.

Source: [Feedback loops](platform-feedback-loops.md)

---

# Apply the patterns together

## Scenario: A team repeatedly rebuilds deployment setup

```text
Repeated setup signal
       ↓
P1 · Golden paths
       ↓ enables
P2 · Feedback loops
       ↓
Maintained default
```

- **Start with:** Automate the repeated setup.
- **Then:** Review why teams use exceptions.
- **Watch for:** A default that no longer reflects current work.

---

# What changes

| Before                    | Pattern | After                         |
| ------------------------- | ------- | ----------------------------- |
| Rebuild delivery setup    | **P1**  | Begin from a maintained path  |
| Ignore recurring feedback | **P2**  | Revise the path from real use |

> **Remaining constraint:** Teams still need a supported way to leave the path.

---

# Pattern map revisited

```text
P1 · Golden paths --enables--> P2 · Feedback loops
P1 · Golden paths --informs--> P2 · Feedback loops
```

> **Domain takeaway:** Defaults and feedback form a learning system.

---

# Choose one pattern to try

- **Signal:** One setup decision recurs across teams.
- **Pattern:** P1 · Golden paths
- **Practice:** Automate one common setup step.
- **Review:** Discuss whether the default removed work without blocking exceptions.

> Start with the pattern that addresses the clearest signal.
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

    def write_deck(self, deck: str) -> None:
        self.deck.write_text(deck, encoding="utf-8")

    def test_accepts_complete_pattern_system_deck(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("2 atomic sources", result.stdout)
        self.assertIn("1 coaching sources", result.stdout)

    def test_template_contains_new_narrative_schema(self) -> None:
        titles = re.findall(r"^#(?!#)\s+(.+?)\s*$", TEMPLATE, re.MULTILINE)
        for title in (
            "[Domain name]",
            "Challenges & opportunities",
            "Pattern map",
            "P1 · [Short pattern name]",
            "P2 · [Short pattern name]",
            "Apply the patterns together",
            "What changes",
            "Pattern map revisited",
            "Choose one pattern to try",
        ):
            self.assertIn(title, titles)
        self.assertIn("###### PATTERN P1 OF [N] · [CLUSTER]", TEMPLATE)
        self.assertIn("Coach:", TEMPLATE)
        self.assertIn("```text", TEMPLATE)
        self.assertNotIn("```mermaid", TEMPLATE)
        self.assertNotIn("<small>", TEMPLATE)
        self.assertTrue(TEMPLATE.endswith("\n"))

    def test_template_is_scaffold_not_completed_deck(self) -> None:
        self.write_deck(
            TEMPLATE.replace("domain-moc.md", "platform-moc.md")
            .replace("domain-atomic-note.md", "platform-golden-paths.md")
            .replace(
                "domain-atomic-note.coach.md",
                "platform-golden-paths.coach.md",
            )
            .replace("#domain", "#platform")
        )
        self.assert_invalid("unreplaced template placeholder(s)")

    def test_rejects_unremoved_template_instructions(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "<!-- markdownlint-disable MD001 MD024 MD025 -->",
                "<!-- markdownlint-disable MD001 MD024 MD025 -->\n"
                "<!-- Repeat one slide for each pattern. -->",
            )
        )
        self.assert_invalid("unreplaced template instruction(s)")

    def test_rejects_filename_not_derived_from_moc(self) -> None:
        wrong_deck = self.root / "slides.marp.md"
        wrong_deck.write_text(self.valid_deck(), encoding="utf-8")
        result = self.run_validator(deck=wrong_deck)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Deck filename must be 'platform.marp.md'", result.stdout)

    def test_requires_each_core_system_slide(self) -> None:
        for title in (
            "Challenges & opportunities",
            "Pattern map",
            "Apply the patterns together",
            "What changes",
            "Pattern map revisited",
            "Choose one pattern to try",
        ):
            with self.subTest(title=title):
                deck = re.sub(
                    rf"\n---\n\n# {re.escape(title)}\n.*?(?=\n---\n|\Z)",
                    "",
                    self.valid_deck(),
                    count=1,
                    flags=re.DOTALL,
                )
                self.write_deck(deck)
                self.assert_invalid(f"exactly one '{title}' slide")

    def test_rejects_core_system_slides_out_of_order(self) -> None:
        deck = self.valid_deck()
        changes = re.search(
            r"\n---\n\n# What changes\n.*?(?=\n---\n)", deck, re.DOTALL
        ).group(0)
        revisited = re.search(
            r"\n---\n\n# Pattern map revisited\n.*?(?=\n---\n)", deck, re.DOTALL
        ).group(0)
        self.write_deck(deck.replace(changes + revisited, revisited + changes))
        self.assert_invalid("do not follow the template order")

    def test_requires_challenges_and_opportunities_sections(self) -> None:
        self.write_deck(self.valid_deck().replace("## Opportunities", "## Potential"))
        self.assert_invalid("requires an Opportunities section")

    def test_requires_domain_question_ending_in_question_mark(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "without freezing learning?",
                "while preserving learning.",
            )
        )
        self.assert_invalid("Domain question ending in ?")

    def test_requires_map_fence(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "```text\nPlatform delivery",
                "Platform delivery",
                1,
            ).replace(
                "P1 · Golden paths --enables--> P2 · Feedback loops\n```",
                "P1 · Golden paths --enables--> P2 · Feedback loops",
                1,
            )
        )
        self.assert_invalid("Pattern map requires a fenced mermaid or text")

    def test_requires_every_pattern_id_in_both_maps(self) -> None:
        self.write_deck(
            self.valid_deck()
            .replace(
                "    └── P2 · Feedback loops",
                "    └── Feedback loops",
                1,
            )
            .replace(
                "P1 · Golden paths --enables--> P2 · Feedback loops",
                "P1 · Golden paths --enables--> Feedback loops",
                1,
            )
        )
        self.assert_invalid("Pattern map is missing pattern ID(s)")

    def test_requires_exact_pattern_names_in_both_maps(self) -> None:
        deck = self.valid_deck()
        revisited = re.search(
            r"\n---\n\n# Pattern map revisited\n.*?(?=\n---\n)",
            deck,
            re.DOTALL,
        ).group(0)
        self.write_deck(
            deck.replace(
                revisited,
                revisited.replace("P2 · Feedback loops", "P2 · Learning loops"),
            )
        )
        self.assert_invalid("Pattern map revisited is missing exact pattern name(s)")

    def test_requires_pattern_clusters_in_first_map(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "└── Learning loops",
                "└── Improvement",
                1,
            )
        )
        self.assert_invalid("Pattern map is missing pattern cluster(s)")

    def test_requires_contiguous_pattern_ids(self) -> None:
        self.write_deck(
            self.valid_deck()
            .replace("PATTERN P2 OF 2", "PATTERN P3 OF 2")
            .replace("# P2 · Feedback loops", "# P3 · Feedback loops", 1)
        )
        self.assert_invalid("contiguous IDs P1 through P2")

    def test_rejects_duplicate_pattern_id(self) -> None:
        self.write_deck(
            self.valid_deck()
            .replace("PATTERN P2 OF 2", "PATTERN P1 OF 2")
            .replace("# P2 · Feedback loops", "# P1 · Feedback loops", 1)
        )
        self.assert_invalid("Pattern ID P1 is used more than once")

    def test_requires_correct_pattern_total(self) -> None:
        self.write_deck(self.valid_deck().replace("OF 2", "OF 3"))
        self.assert_invalid("must declare OF 2")

    def test_requires_pattern_title_to_match_id(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "# P2 · Feedback loops",
                "# P3 · Feedback loops",
                1,
            )
        )
        self.assert_invalid("requires one '# P2 · <short name>' title")

    def test_requires_pattern_statement_shape(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "> **When teams repeat common setup decisions, provide a maintained default, because it preserves attention for product work.**",
                "> **Golden paths preserve attention.**",
            )
        )
        self.assert_invalid("'When X, do Y, because Z.' statement")

    def test_accepts_version_number_inside_pattern_statement(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "provide a maintained default, because it preserves attention",
                "provide a v2.0 default, because it preserves attention",
                1,
            )
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_requires_use_it_when_bullet(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "- Teams repeatedly rebuild the same delivery setup.\n"
                "- Product work waits on avoidable platform choices.",
                "Teams repeatedly rebuild the same delivery setup.",
            )
        )
        self.assert_invalid("Use it when with at least one bullet")

    def test_requires_one_to_three_numbered_practices(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "1. Automate the common path.",
                "Automate the common path.",
            )
        )
        self.assert_invalid("one to three contiguous numbered practices")

    def test_rejects_four_practices(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "2. Document a supported exception.",
                "2. Document a supported exception.\n"
                "3. Review the path.\n"
                "4. Mandate adoption.",
            )
        )
        self.assert_invalid("one to three contiguous numbered practices")

    def test_requires_exactly_one_source_on_pattern_slide(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Source: [Golden paths](platform-golden-paths.md)",
                "Source: [Golden paths](platform-golden-paths.md)\n"
                "Source: [Feedback loops](platform-feedback-loops.md)",
            )
        )
        self.assert_invalid("requires exactly one Source link")

    def test_rejects_source_on_non_pattern_slide(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "# What changes",
                "# What changes\n\nSource: [Golden paths](platform-golden-paths.md)",
            )
        )
        self.assert_invalid("has a Source but is not a PATTERN")

    def test_rejects_missing_atomic_source(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Source: [Feedback loops](platform-feedback-loops.md)",
                "",
            )
        )
        self.assert_invalid("missing atomic Source links")

    def test_rejects_source_outside_moc(self) -> None:
        extra = self.root / "platform-roadmap.md"
        extra.write_text("# Roadmap\n", encoding="utf-8")
        self.write_deck(
            self.valid_deck().replace(
                "Source: [Feedback loops](platform-feedback-loops.md)",
                "Source: [Roadmap](platform-roadmap.md)",
            )
        )
        self.assert_invalid("Source links outside the MOC")

    def test_requires_matching_coach_on_same_pattern_slide(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Coach: [Golden paths coaching](platform-golden-paths.coach.md)",
                "",
            )
        )
        self.assert_invalid("missing available Coach links")

    def test_rejects_coach_on_non_pattern_slide(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "# What changes",
                "# What changes\n\n"
                "Coach: [Golden paths coaching](platform-golden-paths.coach.md)",
            )
        )
        self.assert_invalid("has a Coach link but is not a pattern slide")

    def test_allows_atomic_note_without_coaching_companion(self) -> None:
        self.coach.unlink()
        deck = self.valid_deck().replace(
            "Coach: [Golden paths coaching](platform-golden-paths.coach.md)\n",
            "",
        )
        deck = re.sub(
            r"\n<!--\nCoach cue: Where does repeated setup work consume the most attention\?\n-->\n",
            "\n",
            deck,
        )
        self.write_deck(deck)
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("0 coaching sources", result.stdout)

    def test_requires_coach_cue_question(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Where does repeated setup work consume the most attention?",
                "Discuss repeated setup work.",
            )
        )
        self.assert_invalid("Coach cue question ending in ?")

    def test_rejects_multiple_coach_cues_in_one_comment(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Coach cue: Where does repeated setup work consume the most attention?",
                "Coach cue: Where does repeated setup work consume the most attention?\n"
                "Coach cue: What exception should the team preserve?",
            )
        )
        self.assert_invalid("requires one Coach cue question")

    def test_rejects_unsupported_relationship_label(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "through **enables**",
                "through **causes**",
            )
        )
        self.assert_invalid("Relationship labels must be one of")

    def test_rejects_unsupported_text_map_relationship(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "--informs-->",
                "--causes-->",
                1,
            )
        )
        self.assert_invalid("Relationship labels must be one of")

    def test_rejects_unsupported_scenario_relationship(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "       ↓ enables",
                "       ↓ causes",
            )
        )
        self.assert_invalid("Relationship labels must be one of")

    def test_rejects_relationship_not_found_in_atomic_notes(self) -> None:
        self.note_one.write_text(
            "# Golden paths\n\n## Relationships\n\n"
            "No supported relationships yet.\n",
            encoding="utf-8",
        )
        self.assert_invalid("not permitted by typed, directed atomic-note Relationships")

    def test_rejects_reversed_extension_edge(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "P1 · Golden paths --enables--> P2 · Feedback loops",
                "P2 · Feedback loops --enables--> P1 · Golden paths",
                1,
            )
        )
        self.assert_invalid("not permitted by typed, directed atomic-note Relationships")

    def test_rejects_supported_label_not_permitted_for_extension(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "P1 · Golden paths --enables--> P2 · Feedback loops",
                "P1 · Golden paths --depends on--> P2 · Feedback loops",
                1,
            )
        )
        self.assert_invalid("not permitted by typed, directed atomic-note Relationships")

    def test_rejects_reversed_unquoted_mermaid_extension_edge(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "P1 · Golden paths --enables--> P2 · Feedback loops",
                "P2 -->|enables| P1",
                1,
            )
        )
        self.assert_invalid("not permitted by typed, directed atomic-note Relationships")

    def test_rejects_unquoted_mermaid_label_not_permitted_for_extension(
        self,
    ) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "P1 · Golden paths --enables--> P2 · Feedback loops",
                "P1 -->|depends on| P2",
                1,
            )
        )
        self.assert_invalid("not permitted by typed, directed atomic-note Relationships")

    def test_accepts_unquoted_mermaid_extension_edge(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "P1 · Golden paths --enables--> P2 · Feedback loops",
                "P1 -->|enables| P2",
                1,
            )
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_accepts_spaced_mermaid_extension_edge(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "P1 · Golden paths --enables--> P2 · Feedback loops",
                "P1 -- enables --> P2",
                1,
            )
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_rejects_reversed_spaced_mermaid_extension_edge(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "P1 · Golden paths --enables--> P2 · Feedback loops",
                "P2 -- enables --> P1",
                1,
            )
        )
        self.assert_invalid("not permitted by typed, directed atomic-note Relationships")

    def test_rejects_spaced_mermaid_label_not_permitted_for_extension(
        self,
    ) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "P1 · Golden paths --enables--> P2 · Feedback loops",
                "P1 -- depends on --> P2",
                1,
            )
        )
        self.assert_invalid("not permitted by typed, directed atomic-note Relationships")

    def test_rejects_invalid_second_edge_in_chained_text_map(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "P1 · Golden paths --enables--> P2 · Feedback loops",
                "P1 · Golden paths --enables--> P2 · Feedback loops "
                "--depends on--> P1 · Golden paths",
                1,
            )
        )
        self.assert_invalid("not permitted by typed, directed atomic-note Relationships")

    def test_rejects_invalid_second_edge_in_chained_vertical_path(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "       ↓ enables\n"
                "P2 · Feedback loops\n"
                "       ↓\n"
                "Maintained default",
                "       ↓ enables\n"
                "P2 · Feedback loops\n"
                "       ↓ depends on\n"
                "P1 · Golden paths\n"
                "       ↓\n"
                "Maintained default",
            )
        )
        self.assert_invalid("not permitted by typed, directed atomic-note Relationships")

    def test_accepts_prerequisite_as_source_depends_on_target(self) -> None:
        self.note_one.write_text(
            "# Golden paths\n\n## Relationships\n\n"
            "- Prerequisite: [Feedback loops](platform-feedback-loops.md) "
            "must be understood before selecting a default.\n",
            encoding="utf-8",
        )
        deck = (
            self.valid_deck()
            .replace("--enables-->", "--depends on-->")
            .replace("--informs-->", "--depends on-->")
            .replace("through **enables**", "through **depends on**")
            .replace("       ↓ enables", "       ↓ depends on")
        )
        self.write_deck(deck)
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_accepts_extension_as_source_complements_target(self) -> None:
        deck = (
            self.valid_deck()
            .replace("--enables-->", "--complements-->")
            .replace("--informs-->", "--complements-->")
            .replace("through **enables**", "through **complements**")
            .replace("       ↓ enables", "       ↓ complements")
        )
        self.write_deck(deck)
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_rejects_malformed_related_line(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "**Related:** P2 · Feedback loops through **enables**",
                "**Related to:** P2 · Feedback loops",
            )
        )
        self.assert_invalid("invalid Related relationship")

    def test_rejects_bracketed_related_target(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "**Related:** P2 · Feedback loops through **enables**",
                "**Related:** [P2 · Feedback loops] through **depends on**",
                1,
            )
        )
        self.assert_invalid("invalid Related relationship")

    def test_requires_named_scenario(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "## Scenario: A team repeatedly rebuilds deployment setup",
                "## Scenario",
            )
        )
        self.assert_invalid("requires a named Scenario")

    def test_requires_pattern_slides_between_map_and_application(self) -> None:
        deck = self.valid_deck()
        pattern_two = re.search(
            r"\n---\n\n###### PATTERN P2 OF 2.*?(?=\n---\n)",
            deck,
            re.DOTALL,
        ).group(0)
        deck = deck.replace(pattern_two, "")
        deck = deck.replace(
            "\n---\n\n# What changes",
            pattern_two + "\n---\n\n# What changes",
        )
        self.write_deck(deck)
        self.assert_invalid("Pattern slides must appear between Pattern map")

    def test_requires_application_action_labels(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "- **Then:** Review why teams use exceptions.",
                "- Review why teams use exceptions.",
            )
        )
        self.assert_invalid("requires a 'Then' bullet")

    def test_requires_before_pattern_after_table(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "| Before                    | Pattern | After                         |",
                "| Current | Future |",
            )
        )
        self.assert_invalid("Before | Pattern | After table")

    def test_requires_remaining_constraint(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "> **Remaining constraint:** Teams still need a supported way to leave the path.",
                "",
            )
        )
        self.assert_invalid("requires a Remaining constraint")

    def test_requires_closing_experiment_fields(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "- **Review:** Discuss whether the default removed work without blocking exceptions.",
                "- Discuss the result.",
            )
        )
        self.assert_invalid("requires a 'Review' bullet")

    def test_rejects_unknown_pattern_id_in_closing_experiment(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "- **Pattern:** P1 · Golden paths",
                "- **Pattern:** P99 · Ghost pattern",
            )
        )
        self.assert_invalid("unknown pattern ID(s): [99]")

    def test_rejects_inconsistent_pattern_name_in_closing_experiment(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "- **Pattern:** P1 · Golden paths",
                "- **Pattern:** P1 · Paved roads",
            )
        )
        self.assert_invalid("inconsistent pattern name reference(s)")

    def test_requires_closing_experiment_as_final_slide(self) -> None:
        self.write_deck(
            self.valid_deck()
            + "\n---\n\n# Appendix\n\nAdditional context.\n"
        )
        self.assert_invalid("must be the final slide")

    def test_rejects_wrong_moc_link(self) -> None:
        other_moc = self.root / "other-moc.md"
        other_moc.write_text("# Other\n", encoding="utf-8")
        self.write_deck(self.valid_deck().replace("platform-moc.md", "other-moc.md"))
        self.assert_invalid("only MOC field linking exactly")

    def test_rejects_duplicate_moc_fields(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "MOC: [Platform](platform-moc.md)",
                "MOC: [Platform](platform-moc.md)\n"
                "MOC: [Platform](platform-moc.md)",
            )
        )
        self.assert_invalid("found 2 fields")

    def test_rejects_moc_field_outside_opening_slide(self) -> None:
        self.write_deck(
            self.valid_deck()
            .replace("MOC: [Platform](platform-moc.md)\n", "")
            .replace(
                "# Challenges & opportunities",
                "# Challenges & opportunities\n\nMOC: [Platform](platform-moc.md)",
            )
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
        self.write_deck(
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
            )
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_rejects_missing_domain_tag(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Tags: #platform #slides #publish #private",
                "Tags: #slides #publish #private",
            )
        )
        self.assert_invalid("every MOC domain tag")

    def test_accepts_url_and_email_autolinks(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Connect maintained defaults with learning from real use.",
                "See <https://example.com/docs> or contact <coach@example.com>.",
            )
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_rejects_arbitrary_html(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Connect maintained defaults with learning from real use.",
                "<small>Unsupported layout</small>",
            )
        )
        self.assert_invalid("Arbitrary HTML is not allowed")

    def test_rejects_uppercase_markdown_extension(self) -> None:
        uppercase_note = self.root / "platform-golden-paths.MD"
        uppercase_note.write_text("# Duplicate\n", encoding="utf-8")
        self.write_deck(
            self.valid_deck().replace(
                "platform-golden-paths.md",
                "platform-golden-paths.MD",
                1,
            )
        )
        self.assert_invalid("lowercase '.md' extension")

    def test_separator_inside_fence_does_not_create_slide(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "P1 · Golden paths --enables--> P2 · Feedback loops\n```",
                "P1 · Golden paths --enables--> P2 · Feedback loops\n---\n===\n```",
                1,
            )
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("(9 slides,", result.stdout)

    def test_shorter_fence_does_not_close_longer_fenced_block(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "```text\nPlatform delivery",
                "````text\nPlatform delivery",
                1,
            ).replace(
                "P1 · Golden paths --enables--> P2 · Feedback loops\n```",
                "P1 · Golden paths --enables--> P2 · Feedback loops\n"
                "```\n---\n===\n````",
                1,
            )
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("(9 slides,", result.stdout)

    def test_accepts_tilde_fenced_text_map(self) -> None:
        self.write_deck(
            self.valid_deck().replace("```text", "~~~text").replace("```", "~~~")
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_accepts_fence_aware_equals_slide_separator(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "\n---\n\n# What changes",
                "\n===\n\n# What changes",
            )
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_ignores_fields_links_and_html_inside_fenced_code(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "P1 · Golden paths --enables--> P2 · Feedback loops\n```",
                "P1 · Golden paths --enables--> P2 · Feedback loops\n"
                "Source: [Example](example-note.md)\n"
                "Coach: [Example](example-note.coach.md)\n"
                "<div>Example HTML</div>\n```",
                1,
            )
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
        self.write_deck(
            self.valid_deck().replace(
                "Coach cue: Where does repeated setup work consume the most attention?",
                "Coach cue: Where does repeated setup work consume the most attention?\n"
                "---\n"
                "Keep listening for a concrete example.",
            )
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("(9 slides,", result.stdout)

    def test_rejects_moc_atomic_link_outside_domain(self) -> None:
        other_note = self.root / "leadership-feedback.md"
        other_note.write_text("# Feedback\n", encoding="utf-8")
        self.moc.write_text(
            self.valid_moc().replace(
                "platform-feedback-loops.md",
                "leadership-feedback.md",
            ),
            encoding="utf-8",
        )
        self.assert_invalid("is not an atomic note in domain 'platform'")


if __name__ == "__main__":
    unittest.main()
