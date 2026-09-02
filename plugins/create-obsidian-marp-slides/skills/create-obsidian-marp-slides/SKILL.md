---
name: create-obsidian-marp-slides
description: Create or update one Obsidian Marp presentation that shows a knowledge domain as a connected system of reusable patterns and practices. Use when a domain MOC and its atomic notes should become one coherent <domain>.marp.md deck with optional coaching companions.
license: MIT
compatibility: Produces conservative Obsidian-compatible Marp Markdown ending in .marp.md. Python 3 is required for validation.
---

# Create Obsidian Marp Slides

Create or update one domain presentation that moves from the domain challenge through the MOC's authoritative pattern map and workflow, teaches each pattern, applies them together, and closes with one small experiment.

## Artifact contract

Write one file directly beside the approved domain MOC in the target Obsidian vault:

- navigation source: `<domain>-moc.md`;
- knowledge sources: atomic notes linked from the MOC's `Notes` section;
- optional coaching sources: matching `<atomic-stem>.coach.md` files that exist beside those notes;
- output: `<domain>.marp.md`.

The MOC, atomic notes, and coaching companions are read-only. There is only one `.marp.md` file per domain. Use [assets/slides-template.md](assets/slides-template.md) as the presentation schema. Read [references/slides-design.md](references/slides-design.md) and [references/obsidian-marp-compatibility.md](references/obsidian-marp-compatibility.md).

In update mode, revise the same domain presentation: add, change, or remove pattern coverage to match the MOC while preserving confirmed configuration and useful unaffected content. Restore the pattern IDs, maps, scenario, and narrative coherence after every source change.

## Source and write gate

Before analysis, confirm:

- the authoritative domain MOC;
- the MOC, atomic notes, and coaching companions as read-only inputs;
- create or update mode;
- the approved existing knowledge directory in the target Obsidian vault;
- the exact `<domain>.marp.md` filename and that it is the only permitted change;
- the audience, presentation objective, available time, and required example;
- the portable default Marp configuration or confirmed local customization;
- that the target setup renders Mermaid in Marp.

The template requires Mermaid maps and flows. If the target setup does not render Mermaid, stop and explain the incompatibility; do not substitute text maps. If the MOC has no linked atomic notes, stop; do not create knowledge artifacts inside this skill.

## Workflow

1. Read the MOC's scope, `Pattern map`, `Domain workflow`, and `Notes` entries, every linked atomic note, and each available matching coaching companion. In update mode, also read the current deck.
2. Extract each atomic note's Pattern, Practice, Signals, Constraints, and supported Relationships. From companions, extract relevant Conversation questions.
3. Assign every pattern one stable contiguous internal identifier (`P1` through `PN`), one short memorable name, and one cluster. Preserve existing IDs when their pattern remains unless removing a source creates a gap; then minimally renumber the following patterns to restore contiguity.
4. Propose the domain promise, challenges and opportunities, a presentation rendering of the MOC pattern map and workflow, one slide per pattern, optional comparison, combined scenario, expected directional changes, remaining constraint, and closing experiment.
5. Provide a source-to-pattern-ID plan and identify additions, revisions, removals, retained content, and synthesis. Distinguish source-grounded claims from presentation synthesis.
6. Obtain approval for the plan, diagram format, Marp configuration, exact output path, and sole-file write authority.
7. Create or update only `<domain>.marp.md`, replacing every template prompt and placeholder.

Do not ask for information already supplied. Combine confirmations when the user can approve them safely in one decision.

## Presentation rules

- Use the template's narrative sequence: opening, challenges and opportunities, pattern map, one slide per pattern, optional comparison, combined application, what changes, map revisited, and one pattern to try.
- Put the MOC link and deck `Tags:` in the opening slide's speaker notes under `Source:` and `Metadata:`. Keep source links and supporting metadata out of visible slide content.
- Use stable contiguous pattern IDs only in the H6 position metadata: `###### p<n> of <N> · <cluster>`. Do not show identifiers in H1 titles, Mermaid nodes, tables, or prose.
- Give each pattern slide an H1 short name, `### Use when` signals, and one to three `### Do` practices. Put the complete `When X, do Y, because Z.` pattern description in speaker notes.
- Use one speaker-note block per pattern slide in this order: `Pattern description:`, `Coach cue:`, optional `Related:`, and `Source:`.
- Under the pattern slide's `Source:`, link exactly one MOC atomic note. When its coaching companion exists, link it in the same field. Every MOC atomic note maps to exactly one pattern slide.
- Include one `Coach cue:` question ending in `?` on every pattern slide. Coaching companions remain optional source inputs.
- Show only source-supported relationships and preserve the declaring note, linked target, type, and permitted direction. Apply the translation table in [references/slides-design.md](references/slides-design.md); a reversed claim requires its own supporting atomic relationship. In pattern notes, format a relationship as `Related:` followed by `<target short name> (<relationship>)`.
- Omit a `Related:` field when no source-supported relationship exists.
- Preserve the MOC Pattern map's pattern membership, direction, and exact relationship labels in both deck maps. Preserve the MOC Domain workflow's labeled or unlabeled pattern-to-pattern edges in the combined scenario; add scenario signals and outcomes without changing the authoritative pattern sequence.
- Keep each map consistent with pattern short names, MOC clusters, and supported relationships. Use fenced Mermaid diagrams and do not expose internal pattern IDs in node labels.
- Include the comparison slide only when two patterns are genuine alternatives.
- Move narrative, domain questions, domain takeaways, selection rationale, evidence qualifiers, and remaining constraints into speaker notes as shown by the template.
- Treat before/after content and expected outcomes as source-grounded direction or clearly identified synthesis, never as measured results.
- Keep one primary idea and story beat per slide. Preserve source terminology and critical constraints.
- In the opening speaker-note `Metadata:`, use `Tags:` with every MOC domain tag, `#slides`, exactly one workflow tag, and exactly one visibility tag.
- Use standard Markdown, including URL and email autolinks and approved local images. Speaker-note comments are the only arbitrary-HTML exception. Do not use raw layout HTML, JavaScript, remote fonts, unconfirmed plugins, or custom CSS by default.
- Never invent quotes, evidence, relationships, outcomes, or certainty.

## Validate

Run:

```bash
python3 "<skill-directory>/scripts/validate_marp_slides.py" "<domain>.marp.md" "<domain>-moc.md"
```

Fix every error and review density warnings. Then verify qualitatively that internal IDs map sources without leaking into titles or diagrams, each short name is consistent, speaker notes carry the narrative and grounding, visible signals and practices remain concise, relationship labels are source-supported, the scenario combines patterns coherently, and the close offers a proportionate experiment.

## Completion

Complete only when `<domain>.marp.md` is the sole changed file; it follows the template with no prompts or placeholders; it contains one stable pattern slide for every MOC atomic note and no source outside the domain; internal IDs appear only in H6 position metadata; visible slides use short names while speaker notes carry narrative, questions, relationships, and sources; Mermaid maps preserve the MOC's authoritative relationship and workflow topology; tags and portability rules hold; and the validator reports zero errors.
