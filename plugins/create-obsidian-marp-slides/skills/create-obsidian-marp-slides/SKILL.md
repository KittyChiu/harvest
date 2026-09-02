---
name: create-obsidian-marp-slides
description: Create or update one Obsidian Marp presentation that shows a knowledge domain as a connected system of reusable patterns and practices. Use when a domain MOC and its atomic notes should become one coherent <domain>.marp.md deck with optional coaching questions.
license: MIT
compatibility: Produces conservative Obsidian-compatible Marp Markdown ending in .marp.md. Python 3 is required for validation.
---

# Create Obsidian Marp Slides

Create or update one domain presentation that moves from the domain challenge to a map of its atomic patterns, teaches each pattern, applies them together, and closes with one small experiment.

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
- whether the target setup renders Mermaid in Marp.

If Mermaid support is not confirmed, use readable fenced `text` maps instead. If the MOC has no linked atomic notes, stop; do not create knowledge artifacts inside this skill.

## Workflow

1. Read the MOC's scope and `Notes` entries, every linked atomic note, and each available matching coaching companion. In update mode, also read the current deck.
2. Extract each atomic note's Pattern, Practice, Signals, Constraints, and supported Relationships. From companions, extract relevant Conversation questions.
3. Assign every pattern one stable contiguous identifier (`P1` through `PN`), one short memorable name, and one cluster. Preserve existing IDs when their pattern remains.
4. Propose the domain promise, challenges and opportunities, pattern clusters, supported relationship map, one slide per pattern, optional comparison, combined scenario, expected directional changes, remaining constraint, and closing experiment.
5. Provide a source-to-pattern-ID plan and identify additions, revisions, removals, retained content, and synthesis. Distinguish source-grounded claims from presentation synthesis.
6. Obtain approval for the plan, diagram format, Marp configuration, exact output path, and sole-file write authority.
7. Create or update only `<domain>.marp.md`, replacing every template prompt and placeholder.

Do not ask for information already supplied. Combine confirmations when the user can approve them safely in one decision.

## Presentation rules

- Use the template's narrative sequence: opening, challenges and opportunities, pattern map, one slide per pattern, optional comparison, combined application, what changes, map revisited, and one pattern to try.
- Use `MOC: [<domain name>](<domain>-moc.md)` once on the opening slide.
- Use stable contiguous pattern IDs. Each pattern slide uses `PATTERN Pn OF N`, `# Pn · <short name>`, one `When X, do Y, because Z.` statement, observable signals, and one to three numbered practices.
- Put exactly one `Source: [<atomic-note-title>](<atomic-stem>.md)` on each pattern slide. Every MOC atomic note appears exactly once and nowhere else.
- When the matching coaching companion exists, put `Coach: [<coaching-title>](<atomic-stem>.coach.md)` on that pattern slide and add one HTML-comment `Coach cue:` question ending in `?`.
- A pattern without a coaching companion does not require `Coach:` or a speaker note.
- Show only source-supported relationships and preserve the declaring note, linked target, type, and permitted direction. Apply the translation table in [references/slides-design.md](references/slides-design.md); a reversed claim requires its own supporting atomic relationship. Format a pattern-slide relationship as `**Related:** P<n> · <name> through **<relationship>**`.
- Keep each map consistent with the pattern IDs, names, clusters, and supported relationships. Use Mermaid only when confirmed; otherwise use a portable fenced `text` map.
- Include the comparison slide only when two patterns are genuine alternatives.
- Treat before/after content and expected outcomes as source-grounded direction or clearly identified synthesis, never as measured results.
- Keep one primary idea and story beat per slide. Preserve source terminology and critical constraints.
- Use `Tags:` with every MOC domain tag, `#slides`, exactly one workflow tag, and exactly one visibility tag.
- Use standard Markdown, including URL and email autolinks and approved local images. Speaker-note comments are the only arbitrary-HTML exception. Do not use raw layout HTML, JavaScript, remote fonts, unconfirmed plugins, or custom CSS by default.
- Never invent quotes, evidence, relationships, outcomes, or certainty.

## Validate

Run:

```bash
python3 "<skill-directory>/scripts/validate_marp_slides.py" "<domain>.marp.md" "<domain>-moc.md"
```

Fix every error and review density warnings. Then verify qualitatively that IDs and maps agree, each pattern is understandable without notes, practices remain separate from the pattern, relationship labels are source-supported, the scenario combines patterns coherently, and the close offers a proportionate experiment.

## Completion

Complete only when `<domain>.marp.md` is the sole changed file; it follows the template with no prompts or placeholders; it contains one stable pattern slide for every MOC atomic note and no other source; every available companion provides one coaching question; maps and relationships are consistent and supported; tags and portability rules hold; and the validator reports zero errors.
