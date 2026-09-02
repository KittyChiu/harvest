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
SKILL = (Path(__file__).parents[1] / "SKILL.md").read_text(encoding="utf-8")
DESIGN = (
    Path(__file__).parents[1] / "references" / "slides-design.md"
).read_text(encoding="utf-8")
COMPATIBILITY = (
    Path(__file__).parents[1] / "references" / "obsidian-marp-compatibility.md"
).read_text(encoding="utf-8")
PLUGIN = (Path(__file__).parents[3] / "plugin.json").read_text(encoding="utf-8")


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
        self.note_two.write_text(
            "# Feedback loops\n\n## Relationships\n\n"
            "No supported relationships yet.\n",
            encoding="utf-8",
        )
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

<!--
Narrative:
Repeated delivery decisions consume attention that could go to product work.

Domain question:
How can teams reduce repeated decisions without freezing learning?

Source:
[Platform](platform-moc.md)

Metadata:
Tags: #platform #slides #publish #private
-->

---

# Challenges & opportunities

## Challenges

- Teams repeat common setup decisions.
- Repeated choices delay product work.

## Opportunities

- Maintained defaults preserve attention.
- Feedback keeps defaults relevant.

<!--
Narrative:
The opportunity is to remove repeated work without removing adaptation.

Domain question:
How can a maintained path continue learning from real use?

Source:
[Platform](platform-moc.md)
-->

---

# Pattern map

```mermaid
flowchart LR
    subgraph C1["Delivery defaults"]
        A["Golden paths"]
    end
    subgraph C2["Learning loops"]
        B["Feedback loops"]
    end
    A -->|enables| B
```

<!--
Narrative:
Defaults and feedback form one learning system.

Domain question:
Which connection keeps the default relevant?

Related:
- Golden paths enables Feedback loops

Source:
[Platform](platform-moc.md)
-->

---

###### P1 of 2 · Delivery defaults

# Golden paths

### Use when

- Teams repeatedly rebuild the same delivery setup.
- Product work waits on avoidable platform choices.

### Do

- Automate the common path.
- Document a supported exception.

<!--
Pattern description:
When teams repeat common setup decisions, provide a maintained default, because it preserves attention for product work.

Coach cue:
Where does repeated setup work consume the most attention?

Related:
Feedback loops (enables)

Source:
[Golden paths](platform-golden-paths.md)
[Golden paths coaching](platform-golden-paths.coach.md)
-->

---

###### p2 of 2 · Learning loops

# Feedback loops

### Use when

- Teams leave the default for similar reasons.
- Workarounds recur across products.

### Do

- Review why teams choose exceptions.
- Update the common path when evidence repeats.

<!--
Pattern description:
When a default no longer fits current work, collect feedback, because real use reveals where the path needs to change.

Coach cue:
Which repeated exception suggests the default should change?

Source:
[Feedback loops](platform-feedback-loops.md)
-->

---

# Apply the patterns together

## Scenario: A team repeatedly rebuilds deployment setup

```mermaid
flowchart LR
    S["Repeated setup signal"]
    A["Golden paths"]
    B["Feedback loops"]
    O["Maintained default"]
    S --> A
    A -->|enables| B
    B --> O
```

- **Start with:** Automate the repeated setup.
- **Then:** Review why teams use exceptions.
- **Watch for:** A default that no longer reflects current work.

<!--
Narrative:
Start with the repeated work, then use exceptions as learning.

Coach cue:
Where might this sequence branch or fail?

Related:
- Golden paths enables Feedback loops

Source:
[Platform](platform-moc.md)
[Golden paths](platform-golden-paths.md)
[Feedback loops](platform-feedback-loops.md)
-->

---

# What changes

| Before | Pattern | After |
| --- | --- | --- |
| Rebuild delivery setup | **Golden paths** | Begin from a maintained path |
| Ignore recurring feedback | **Feedback loops** | Revise the path from real use |

<!--
Narrative:
The expected direction is less repeated setup and more deliberate learning.

Evidence:
These are source-grounded expected directions, not measured results.

Coach cue:
Which change would provide the earliest useful evidence?

Remaining constraint:
Teams still need a supported way to leave the path.

Source:
[Platform](platform-moc.md)
[Golden paths](platform-golden-paths.md)
[Feedback loops](platform-feedback-loops.md)
-->

---

# Pattern map revisited

```mermaid
flowchart LR
    subgraph C1["Delivery defaults"]
        A["Golden paths"]
    end
    subgraph C2["Learning loops"]
        B["Feedback loops"]
    end
    A -->|enables| B
```

<!--
Domain takeaway:
Defaults and feedback form a learning system.

Coach cue:
Which relationship should the audience retain?

Related:
- Golden paths enables Feedback loops

Source:
[Platform](platform-moc.md)
-->

---

# Choose one pattern to try

- **Signal:** One setup decision recurs across teams.
- **Pattern:** Golden paths
- **Practice:** Automate one common setup step.
- **Review:** Discuss whether the default removed work without blocking exceptions.

<!--
Narrative:
Start with the pattern that addresses the clearest observable signal.

Coach cue:
What is the smallest action that could produce useful evidence?

Source:
[Golden paths](platform-golden-paths.md)
[Golden paths coaching](platform-golden-paths.coach.md)
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
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(message, result.stdout)

    def write_deck(self, deck: str) -> None:
        self.deck.write_text(deck, encoding="utf-8")

    def deck_with_comparison(self) -> str:
        comparison = """---

# Choosing between Golden paths and Feedback loops

| Situation | Use |
| --- | --- |
| Repeated setup | **Golden paths** |
| Recurring exceptions | **Feedback loops** |

<!--
Selection rule:
When setup repeats, prefer Golden paths, because defaults remove repeated work.

Coach cue:
Which observable condition distinguishes these choices?

Related:
Golden paths enables Feedback loops

Source:
[Golden paths](platform-golden-paths.md)
[Feedback loops](platform-feedback-loops.md)
-->

"""
        return self.valid_deck().replace(
            "---\n\n# Apply the patterns together",
            comparison + "---\n\n# Apply the patterns together",
        )

    def test_accepts_complete_pattern_system_deck(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("2 atomic sources", result.stdout)
        self.assertIn("1 coaching sources", result.stdout)

    def test_template_and_contract_share_new_schema(self) -> None:
        titles = re.findall(r"^#(?!#)\s+(.+?)\s*$", TEMPLATE, re.MULTILINE)
        for title in (
            "[Domain name]",
            "Challenges & opportunities",
            "Pattern map",
            "[Short pattern name]",
            "Apply the patterns together",
            "What changes",
            "Pattern map revisited",
            "Choose one pattern to try",
        ):
            self.assertIn(title, titles)
        self.assertIn("###### P[1] of [N] · [Cluster]", TEMPLATE)
        self.assertIn("Pattern description:\nWhen [condition]", TEMPLATE)
        self.assertIn("Do not show identifiers in slide titles or Mermaid nodes.", TEMPLATE)
        self.assertGreaterEqual(TEMPLATE.count("```mermaid"), 3)
        self.assertNotIn("```text", TEMPLATE)
        self.assertIn("pattern IDs only in the H6 position metadata", SKILL)
        self.assertIn("fenced Mermaid", DESIGN)
        self.assertIn("does not render Mermaid", COMPATIBILITY)
        self.assertIn("optional coaching companions", PLUGIN)
        self.assertNotIn("optional coaching questions", PLUGIN)
        self.assertIn("P1, p2, p3", TEMPLATE)
        self.assertNotIn("P1, P2, P3", TEMPLATE)
        self.assertIn("Omit Related when no source-supported relationship exists.", TEMPLATE)
        self.assertIn(
            "Coach cue: What changes when the audience applies this idea?",
            COMPATIBILITY,
        )

    def test_template_is_scaffold_not_completed_deck(self) -> None:
        self.write_deck(TEMPLATE.replace("domain-moc.md", "platform-moc.md"))
        self.assert_invalid("unreplaced template")

    def test_rejects_unremoved_authoring_instructions(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "# Platform delivery",
                "<!--\nAUTHORING RULES\n-->\n\n# Platform delivery",
            )
        )
        self.assert_invalid("unreplaced template instruction")

    def test_requires_front_matter_fields(self) -> None:
        for field in ("marp", "theme", "paginate", "size", "title", "description"):
            with self.subTest(field=field):
                self.write_deck(
                    re.sub(rf"^{field}:.*\n", "", self.valid_deck(), count=1, flags=re.MULTILINE)
                )
                self.assert_invalid(f"'{field}'")

    def test_rejects_internal_pattern_id_in_front_matter(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "title: Platform patterns",
                "title: Platform P1 patterns",
                1,
            )
        )
        self.assert_invalid("Pattern IDs may appear only")

    def test_requires_marp_true(self) -> None:
        self.write_deck(self.valid_deck().replace("marp: true", "marp: false"))
        self.assert_invalid("must be 'true'")

    def test_requires_filename_derived_from_moc(self) -> None:
        wrong = self.root / "slides.marp.md"
        wrong.write_text(self.valid_deck(), encoding="utf-8")
        result = self.run_validator(deck=wrong)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Deck filename must be 'platform.marp.md'", result.stdout)

    def test_requires_same_directory(self) -> None:
        other = self.root / "other"
        other.mkdir()
        deck = other / "platform.marp.md"
        deck.write_text(self.valid_deck(), encoding="utf-8")
        result = self.run_validator(deck=deck)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("same knowledge directory", result.stdout)

    def test_requires_each_core_slide(self) -> None:
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

    def test_rejects_core_slides_out_of_order(self) -> None:
        deck = self.valid_deck()
        changes = re.search(
            r"\n---\n\n# What changes\n.*?(?=\n---\n)", deck, re.DOTALL
        ).group(0)
        revisited = re.search(
            r"\n---\n\n# Pattern map revisited\n.*?(?=\n---\n)", deck, re.DOTALL
        ).group(0)
        self.write_deck(deck.replace(changes + revisited, revisited + changes))
        self.assert_invalid("do not follow the template order")

    def test_requires_opening_speaker_note_fields(self) -> None:
        self.write_deck(self.valid_deck().replace("Narrative:\nRepeated", "Story:\nRepeated", 1))
        self.assert_invalid("Opening slide speaker notes require")

    def test_requires_domain_question_in_speaker_notes(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "How can teams reduce repeated decisions without freezing learning?",
                "Teams should reduce repeated decisions.",
                1,
            )
        )
        self.assert_invalid("Domain question' ending in ?")

    def test_requires_opening_moc_source(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "[Platform](platform-moc.md)",
                "[Golden paths](platform-golden-paths.md)",
                1,
            )
        )
        self.assert_invalid("Opening slide speaker-note Source")

    def test_rejects_internal_pattern_id_in_link_label(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "[Platform](platform-moc.md)",
                "[P1](platform-moc.md)",
                1,
            )
        )
        self.assert_invalid("Pattern IDs may appear only")

    def test_rejects_plain_text_system_source(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "The opportunity is to remove repeated work without removing adaptation.\n\n"
                "Domain question:\n"
                "How can a maintained path continue learning from real use?\n\n"
                "Source:\n"
                "[Platform](platform-moc.md)",
                "The opportunity is to remove repeated work without removing adaptation.\n\n"
                "Domain question:\n"
                "How can a maintained path continue learning from real use?\n\n"
                "Source:\n"
                "No source.",
            )
        )
        self.assert_invalid("speaker-note Source must link exactly")

    def test_rejects_extra_external_source_link(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "[Platform](platform-moc.md)\n\nMetadata:",
                "[Platform](platform-moc.md)\n"
                "[External reference](https://example.com/reference)\n\nMetadata:",
                1,
            )
        )
        self.assert_invalid("Source links must use local Markdown files")

    def test_rejects_prose_in_source_field(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "[Platform](platform-moc.md)\n\nMetadata:",
                "[Platform](platform-moc.md)\nGrounded in the domain.\n\nMetadata:",
                1,
            )
        )
        self.assert_invalid("Source must contain only one")

    def test_rejects_visible_note_only_field(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Connect maintained defaults with learning from real use.",
                "Connect maintained defaults with learning from real use.\n\n"
                "Coach cue: What should the audience notice?",
                1,
            )
        )
        self.assert_invalid("must remain in speaker notes")

    def test_rejects_visible_duplicate_of_note_only_question(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Connect maintained defaults with learning from real use.",
                "Connect maintained defaults with learning from real use.\n\n"
                "How can teams reduce repeated decisions without freezing learning?",
                1,
            )
        )
        self.assert_invalid("duplicates speaker-note-only field content visibly")

    def test_requires_tags_in_opening_metadata(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Tags: #platform #slides #publish #private",
                "Tags: #slides #private",
            )
        )
        self.assert_invalid("every MOC domain tag")
        self.assert_invalid("exactly one workflow tag")

    def test_rejects_visible_source_link(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Connect maintained defaults with learning from real use.",
                "Connect learning from [Platform](platform-moc.md).",
            )
        )
        self.assert_invalid("only in speaker notes")

    def test_rejects_source_outside_domain(self) -> None:
        extra = self.root / "external-note.md"
        extra.write_text("# External\n", encoding="utf-8")
        self.write_deck(
            self.valid_deck().replace(
                "[Platform](platform-moc.md)",
                "[External](external-note.md)",
                1,
            )
        )
        self.assert_invalid("source links outside the MOC domain")

    def test_requires_lowercase_internal_links(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "platform-golden-paths.md", "platform-golden-paths.MD", 1
            )
        )
        self.assert_invalid("lowercase '.md' extension")

    def test_requires_flat_internal_links(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "platform-golden-paths.md", "notes/platform-golden-paths.md", 1
            )
        )
        self.assert_invalid("flat filename")

    def test_accepts_wiki_links_in_speaker_notes(self) -> None:
        deck = (
            self.valid_deck()
            .replace("[Platform](platform-moc.md)", "[[platform-moc|Platform]]")
            .replace(
                "[Golden paths](platform-golden-paths.md)",
                "[[platform-golden-paths|Golden paths]]",
            )
            .replace(
                "[Feedback loops](platform-feedback-loops.md)",
                "[[platform-feedback-loops|Feedback loops]]",
            )
            .replace(
                "[Golden paths coaching](platform-golden-paths.coach.md)",
                "[[platform-golden-paths.coach|Golden paths coaching]]",
            )
        )
        self.write_deck(deck)
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_accepts_url_and_email_autolinks(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Connect maintained defaults with learning from real use.",
                "See <https://example.com> or contact <coach@example.com>.",
            )
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_rejects_arbitrary_html(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Connect maintained defaults with learning from real use.",
                "<div>Layout content</div>",
            )
        )
        self.assert_invalid("Arbitrary HTML is not allowed")

    def test_requires_lowercase_pattern_metadata(self) -> None:
        self.write_deck(self.valid_deck().replace("###### P1 of 2", "###### P1 OF 2"))
        self.assert_invalid("pattern metadata must use")

    def test_requires_contiguous_pattern_ids(self) -> None:
        self.write_deck(self.valid_deck().replace("###### p2 of 2", "###### p3 of 2"))
        self.assert_invalid("contiguous internal IDs")

    def test_rejects_duplicate_pattern_id(self) -> None:
        self.write_deck(self.valid_deck().replace("###### p2 of 2", "###### P1 of 2"))
        self.assert_invalid("used more than once")

    def test_requires_correct_pattern_total(self) -> None:
        self.write_deck(self.valid_deck().replace("###### P1 of 2", "###### P1 of 3"))
        self.assert_invalid("declare of 2")

    def test_rejects_pattern_id_in_title(self) -> None:
        self.write_deck(self.valid_deck().replace("# Golden paths", "# P1 · Golden paths", 1))
        self.assert_invalid("must not expose its internal pattern ID")

    def test_rejects_pattern_id_in_mermaid_node(self) -> None:
        self.write_deck(self.valid_deck().replace('A["Golden paths"]', 'A["P1 · Golden paths"]', 1))
        self.assert_invalid("Pattern IDs may appear only")

    def test_rejects_pattern_id_in_speaker_notes(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Repeated delivery decisions consume attention",
                "P1 shows that repeated delivery decisions consume attention",
                1,
            )
        )
        self.assert_invalid("Pattern IDs may appear only")

    def test_requires_unique_pattern_names(self) -> None:
        self.write_deck(self.valid_deck().replace("# Feedback loops", "# Golden paths", 1))
        self.assert_invalid("short names must be unique")

    def test_requires_pattern_description_in_speaker_notes(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Pattern description:\nWhen teams repeat common setup decisions",
                "Pattern summary:\nWhen teams repeat common setup decisions",
                1,
            )
        )
        self.assert_invalid("Pattern description")

    def test_requires_when_do_because_description(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "When teams repeat common setup decisions, provide a maintained default, because it preserves attention for product work.",
                "Golden paths preserve attention.",
                1,
            )
        )
        self.assert_invalid("When X, do Y, because Z")

    def test_rejects_visible_complete_pattern_description(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "# Golden paths\n\n### Use when",
                "# Golden paths\n\n"
                "When teams repeat decisions, provide a default, because it saves attention.\n\n"
                "### Use when",
            )
        )
        self.assert_invalid("complete pattern description in speaker notes")

    def test_requires_use_when_bullets(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "- Teams repeatedly rebuild the same delivery setup.",
                "Teams repeatedly rebuild the same delivery setup.",
                1,
            ).replace(
                "- Product work waits on avoidable platform choices.",
                "Product work waits on avoidable platform choices.",
                1,
            )
        )
        self.assert_invalid("'Use when' bullets")

    def test_requires_one_to_three_do_bullets(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "- Document a supported exception.",
                "- Document a supported exception.\n"
                "- Review usage.\n"
                "- Mandate adoption.",
                1,
            )
        )
        self.assert_invalid("'Do' bullets")

    def test_requires_atomic_source_on_pattern_slide(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "[Feedback loops](platform-feedback-loops.md)",
                "",
                1,
            )
        )
        self.assert_invalid("exactly one MOC atomic note")

    def test_rejects_duplicate_atomic_pattern_source(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "[Feedback loops](platform-feedback-loops.md)",
                "[Golden paths](platform-golden-paths.md)",
                1,
            )
        )
        self.assert_invalid("duplicates")

    def test_requires_matching_coaching_companion(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "[Golden paths coaching](platform-golden-paths.coach.md)",
                "",
                1,
            )
        )
        self.assert_invalid("matching coaching companion")

    def test_allows_pattern_without_coaching_companion(self) -> None:
        self.coach.unlink()
        self.write_deck(
            self.valid_deck().replace(
                "[Golden paths coaching](platform-golden-paths.coach.md)\n",
                "",
            )
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_requires_pattern_note_field_order(self) -> None:
        deck = self.valid_deck()
        related = "Related:\nFeedback loops (enables)\n\n"
        source = (
            "Source:\n[Golden paths](platform-golden-paths.md)\n"
            "[Golden paths coaching](platform-golden-paths.coach.md)\n"
        )
        self.write_deck(deck.replace(related + source, source + "\n" + related, 1))
        self.assert_invalid("speaker-note fields must follow")

    def test_requires_coach_cue_question(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Where does repeated setup work consume the most attention?",
                "Notice repeated setup work.",
                1,
            )
        )
        self.assert_invalid("Coach cue' ending in ?")

    def test_requires_mermaid_pattern_maps(self) -> None:
        self.write_deck(
            self.valid_deck().replace("```mermaid", "```text", 1)
        )
        self.assert_invalid("requires exactly one fenced Mermaid diagram")

    def test_hidden_mermaid_does_not_satisfy_pattern_map(self) -> None:
        diagram = """```mermaid
flowchart LR
    subgraph C1["Delivery defaults"]
        A["Golden paths"]
    end
    subgraph C2["Learning loops"]
        B["Feedback loops"]
    end
    A -->|enables| B
```"""
        deck = self.valid_deck().replace(diagram, "", 1)
        deck = deck.replace(
            "Narrative:\nDefaults and feedback form one learning system.",
            diagram + "\n\nNarrative:\nDefaults and feedback form one learning system.",
            1,
        )
        self.write_deck(deck)
        self.assert_invalid("requires exactly one fenced Mermaid diagram")

    def test_requires_mermaid_scenario_flow(self) -> None:
        marker = "# Apply the patterns together"
        before, after = self.valid_deck().split(marker, 1)
        after = after.replace("```mermaid", "```text", 1)
        self.write_deck(before + marker + after)
        self.assert_invalid("requires exactly one fenced Mermaid flow")

    def test_hidden_mermaid_does_not_satisfy_scenario_flow(self) -> None:
        marker = "# Apply the patterns together"
        before, after = self.valid_deck().split(marker, 1)
        diagram = re.search(r"```mermaid\n.*?\n```", after, re.DOTALL).group(0)
        after = after.replace(diagram, "", 1).replace(
            "Narrative:\nStart with the repeated work",
            diagram + "\n\nNarrative:\nStart with the repeated work",
            1,
        )
        self.write_deck(before + marker + after)
        self.assert_invalid("requires exactly one fenced Mermaid flow")

    def test_requires_every_pattern_name_in_both_maps(self) -> None:
        deck = self.valid_deck()
        second_map = deck.rfind('B["Feedback loops"]')
        self.write_deck(
            deck[:second_map]
            + deck[second_map:].replace('B["Feedback loops"]', 'B["Learning"]', 1)
        )
        self.assert_invalid("Pattern map revisited is missing exact pattern name")

    def test_requires_clusters_in_first_map(self) -> None:
        self.write_deck(
            self.valid_deck().replace('C1["Delivery defaults"]', 'C1["Defaults"]', 1)
        )
        self.assert_invalid("Pattern map is missing pattern cluster")

    def test_rejects_unsupported_mermaid_relationship(self) -> None:
        self.write_deck(
            self.valid_deck().replace("A -->|enables| B", "A -->|causes| B", 1)
        )
        self.assert_invalid("Relationship labels must be one of")

    def test_rejects_unlabelled_pattern_relationship(self) -> None:
        self.write_deck(
            self.valid_deck().replace("A -->|enables| B", "A --> B", 1)
        )
        self.assert_invalid("edges between patterns require")

    def test_rejects_every_unlabelled_mermaid_pattern_edge_form(self) -> None:
        for connector in ("-->", "---", "==>", "===", "-.->", "-.-", "~~~"):
            with self.subTest(connector=connector):
                self.write_deck(
                    self.valid_deck().replace(
                        "A -->|enables| B",
                        f"A {connector} B",
                        1,
                    )
                )
                self.assert_invalid("edges between patterns require")

    def test_rejects_unlabelled_pattern_edge_in_mermaid_chain(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "A -->|enables| B",
                "A -->|enables| B --> A",
                1,
            )
        )
        self.assert_invalid("edges between patterns require")

    def test_rejects_empty_related_field(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Source:\n[Feedback loops](platform-feedback-loops.md)",
                "Related:\n\nSource:\n[Feedback loops](platform-feedback-loops.md)",
                1,
            )
        )
        self.assert_invalid("must omit Related")

    def test_requires_closing_source_to_match_selected_pattern(self) -> None:
        source = (
            "Source:\n"
            "[Golden paths](platform-golden-paths.md)\n"
            "[Golden paths coaching](platform-golden-paths.coach.md)\n"
            "-->\n"
        )
        before, separator, _after = self.valid_deck().rpartition(source)
        self.assertTrue(separator)
        self.write_deck(
            before
            + "Source:\n[Feedback loops](platform-feedback-loops.md)\n-->\n"
        )
        self.assert_invalid("Source must match the selected pattern")

    def test_rejects_slide_outside_template_sequence(self) -> None:
        extra = """---

# Appendix

- Additional material

<!--
Source:
[Platform](platform-moc.md)
-->

"""
        self.write_deck(
            self.valid_deck().replace(
                "---\n\n# Choose one pattern to try",
                extra + "---\n\n# Choose one pattern to try",
                1,
            )
        )
        self.assert_invalid("outside the template sequence")

    def test_rejects_reversed_extension_relationship(self) -> None:
        self.write_deck(
            self.valid_deck().replace("A -->|enables| B", "B -->|enables| A", 1)
        )
        self.assert_invalid("not permitted by typed, directed")

    def test_rejects_valid_label_for_wrong_atomic_type(self) -> None:
        self.write_deck(
            self.valid_deck().replace("A -->|enables| B", "A -->|depends on| B", 1)
        )
        self.assert_invalid("not permitted by typed, directed")

    def test_rejects_unsupported_related_claim(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Feedback loops (enables)", "Feedback loops (depends on)", 1
            )
        )
        self.assert_invalid("not permitted by typed, directed")

    def test_rejects_unparseable_related_claim(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Feedback loops (enables)", "Something vaguely related", 1
            )
        )
        self.assert_invalid("unparseable Related claim")

    def test_accepts_prerequisite_translation(self) -> None:
        self.note_one.write_text(
            "# Golden paths\n\n## Relationships\n\n"
            "- Prerequisite: [Feedback loops](platform-feedback-loops.md) "
            "must be understood first.\n",
            encoding="utf-8",
        )
        deck = self.valid_deck().replace("enables", "depends on")
        self.write_deck(deck)
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_accepts_extension_complements_translation(self) -> None:
        self.write_deck(self.valid_deck().replace("enables", "complements"))
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_accepts_domain_without_supported_relationships(self) -> None:
        self.note_one.write_text(
            "# Golden paths\n\n## Relationships\n\n"
            "No supported relationships yet.\n",
            encoding="utf-8",
        )
        deck = self.valid_deck().replace("    A -->|enables| B\n", "")
        deck = deck.replace(
            "    A -->|enables| B\n    B --> O",
            "    A --> O\n    S --> B\n    B --> O",
        )
        deck = deck.replace("Related:\nFeedback loops (enables)\n\n", "", 1)
        deck = deck.replace("Related:\n- Golden paths enables Feedback loops\n\n", "")
        self.write_deck(deck)
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_requires_named_scenario(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "## Scenario: A team repeatedly rebuilds deployment setup",
                "## Scenario",
            )
        )
        self.assert_invalid("requires a named Scenario")

    def test_requires_application_bullets(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "- **Watch for:** A default that no longer reflects current work.",
                "",
            )
        )
        self.assert_invalid("requires a 'Watch for' bullet")

    def test_requires_before_pattern_after_table(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "| Before | Pattern | After |",
                "| Current | Pattern | Future |",
            )
        )
        self.assert_invalid("Before | Pattern | After table")

    def test_rejects_unknown_pattern_name_in_changes_table(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "**Feedback loops**", "**Learning reviews**", 1
            )
        )
        self.assert_invalid("Pattern column must use exact pattern short names")

    def test_requires_remaining_constraint_in_speaker_notes(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Remaining constraint:\nTeams still need a supported way to leave the path.",
                "",
            )
        )
        self.assert_invalid("'Remaining constraint' field")

    def test_requires_exact_pattern_name_in_close(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "- **Pattern:** Golden paths",
                "- **Pattern:** P1",
            )
        )
        self.assert_invalid("exact pattern short name")

    def test_requires_close_as_final_slide(self) -> None:
        self.write_deck(self.valid_deck() + "\n---\n\n# Appendix\n")
        self.assert_invalid("must be the final slide")

    def test_comparison_requires_two_atomic_sources(self) -> None:
        comparison = """---

# Choosing between Golden paths and Feedback loops

| Situation | Use |
| --- | --- |
| Repeated setup | **Golden paths** |
| Recurring exceptions | **Feedback loops** |

<!--
Selection rule:
When setup repeats, prefer Golden paths, because defaults remove repeated work.

Coach cue:
Which observable condition distinguishes these choices?

Related:
Golden paths contrasts with Feedback loops

Source:
[Golden paths](platform-golden-paths.md)
-->

"""
        self.write_deck(
            self.valid_deck().replace(
                "---\n\n# Apply the patterns together",
                comparison + "---\n\n# Apply the patterns together",
            )
        )
        self.assert_invalid("requires exactly two atomic notes")

    def test_comparison_title_uses_source_linked_names(self) -> None:
        self.write_deck(
            self.deck_with_comparison().replace(
                "# Choosing between Golden paths and Feedback loops",
                "# Choosing between Defaults and Reviews",
            )
        )
        self.assert_invalid("title must use its two source-linked pattern short names")

    def test_comparison_table_uses_source_linked_names(self) -> None:
        self.write_deck(
            self.deck_with_comparison().replace(
                "| Recurring exceptions | **Feedback loops** |",
                "| Recurring exceptions | **Learning reviews** |",
            )
        )
        self.assert_invalid("table must use its two source-linked pattern short names")

    def test_scenario_uses_source_linked_pattern_names(self) -> None:
        marker = "# Apply the patterns together"
        before, after = self.valid_deck().split(marker, 1)
        after = after.replace('B["Feedback loops"]', 'B["Learning reviews"]', 1)
        self.write_deck(before + marker + after)
        self.assert_invalid("Mermaid flow is missing source-linked pattern name")

    def test_accepts_fence_aware_equals_separator(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "\n---\n\n# What changes",
                "\n===\n\n# What changes",
            )
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_separator_inside_fence_does_not_create_slide(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "A -->|enables| B\n```",
                "A -->|enables| B\n---\n===\n```",
                1,
            )
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_separator_inside_speaker_notes_does_not_create_slide(self) -> None:
        self.write_deck(
            self.valid_deck().replace(
                "Where does repeated setup work consume the most attention?",
                "---\n===\n"
                "Where does repeated setup work consume the most attention?",
            )
        )
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_rejects_moc_without_atomic_notes(self) -> None:
        self.moc.write_text(
            self.valid_moc().replace(
                "- [Golden paths](platform-golden-paths.md) - paved routes for common work.\n"
                "- [Feedback loops](platform-feedback-loops.md) - use learning to improve routes.",
                "No atomic notes yet.",
            ),
            encoding="utf-8",
        )
        self.assert_invalid("must link at least one atomic note")

    def test_rejects_moc_atomic_link_outside_domain(self) -> None:
        other_note = self.root / "leadership-feedback.md"
        other_note.write_text("# Feedback\n", encoding="utf-8")
        self.moc.write_text(
            self.valid_moc().replace(
                "platform-feedback-loops.md", "leadership-feedback.md"
            ),
            encoding="utf-8",
        )
        self.assert_invalid("is not an atomic note in domain")


if __name__ == "__main__":
    unittest.main()
