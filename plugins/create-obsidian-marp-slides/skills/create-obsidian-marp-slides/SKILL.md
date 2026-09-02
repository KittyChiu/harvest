---
name: create-obsidian-marp-slides
description: Create or update the single Obsidian Marp presentation for a knowledge domain. Use when turning a domain MOC and its atomic notes into one coherent <domain>.marp.md file, adding coaching speaker notes when coaching companions exist.
license: MIT
compatibility: Produces conservative Obsidian-compatible Marp Markdown ending in .marp.md. Python 3 is required for validation.
---

# Create Obsidian Marp Slides

Create or update one presentation for one knowledge domain. The domain MOC defines the presentation boundary; its linked atomic notes supply the ideas, and available coaching companions inform the speaker notes.

## Domain presentation contract

Write one file directly beside the domain MOC in the approved existing knowledge directory within the target Obsidian vault:

- navigation source: `<domain>-moc.md`
- knowledge sources: atomic notes linked from the MOC's `Notes` section
- optional coaching sources: `<atomic-stem>.coach.md` files that exist beside those notes
- output: `<domain>.marp.md`

There must be only one `.marp.md` file for the domain.

In create mode, initialize `<domain>.marp.md`. In update mode, read and revise that same file:

- add or update coverage for atomic notes currently linked from the MOC;
- remove source references and slides that no longer belong to the MOC;
- preserve useful configuration, narrative structure, and unaffected content;
- restore coherence after every addition, removal, or reorder.

The MOC, atomic notes, and coaching notes are always read-only. Read [references/slides-design.md](references/slides-design.md) and [references/obsidian-marp-compatibility.md](references/obsidian-marp-compatibility.md). Use [assets/slides-template.md](assets/slides-template.md).

## Source and write gate

Before analysis, confirm:

- the authoritative domain MOC;
- the MOC, atomic notes, and coaching notes that remain read-only;
- create or update mode;
- the approved existing knowledge directory in the target Obsidian vault;
- the exact `<domain>.marp.md` output filename;
- that no other file may be created or changed;
- audience, presentation objective, available time, and any required example;
- whether to use the portable default Marp configuration or confirmed local customization.

If the MOC has no linked atomic notes, stop and explain that the domain has no knowledge to present. Do not create notes inside this skill.

## Interaction flow

1. Read the MOC's scope and `Notes` entries, then read every linked atomic note and each available matching coaching note.
2. In update mode, read the existing domain presentation and compare its `Source:` and `Coach source:` lines with the current MOC.
3. Propose one domain throughline and a source-to-slide plan. Every atomic note must have a visible destination; related notes may share a slide only when one primary idea remains clear.
4. Identify additions, revisions, removals, retained slides, and any presentation or coaching synthesis.
5. Confirm the plan, configuration, exact output path, and sole-file write authority.
6. Create or update only `<domain>.marp.md`.

## Slide rules

- Use `MOC: [<domain name>](<domain>-moc.md)` once on the opening slide.
- Put `Source: [<atomic-note-title>](<atomic-stem>.md)` on the slide where each atomic idea is visibly conveyed.
- When a coaching companion exists, put `Coach source: [<coaching-note-title>](<atomic-stem>.coach.md)` on a relevant slide and add a speaker-note comment grounded in that companion.
- Cover every atomic note currently listed in the MOC exactly as a domain source; do not retain sources outside the MOC.
- Reference every available coaching companion at least once.
- Use portable relative Markdown links by default. Obsidian wiki-style links are also accepted.
- Keep one primary idea and one story beat per slide.
- Use one domain throughline that makes the sequence more useful than a collection of mini-decks.
- Preserve each atomic note's terminology and critical constraints.
- Use `Tags:` with the MOC's domain tags, `#slides`, exactly one workflow tag, and exactly one visibility tag.
- Speaker notes are optional when no coaching companion supports the slide.
- When a slide has a `Coach source:`, include a non-empty HTML-comment speaker note beginning with `Coach cue:` and make it useful for prompting, listening, explaining, or transitioning.
- Use standard Markdown, including URL and email autolinks, and approved local images. Do not use arbitrary HTML, JavaScript, remote fonts, unconfirmed plugins, or custom CSS by default.
- Never invent quotes, evidence, outcomes, or certainty.

## Validate

Run:

```bash
python3 "<skill-directory>/scripts/validate_marp_slides.py" "<domain>.marp.md" "<domain>-moc.md"
```

The validator resolves atomic and coaching sources from the MOC and knowledge directory. Fix every error and review density warnings. Then confirm that every atomic idea remains understandable without speaker notes and that the domain narrative opens, develops, and closes coherently.

## Completion

Complete only when the single `<domain>.marp.md` file is beside its MOC, includes exactly the MOC's atomic-note source set, references every available coaching companion with a grounded speaker note, carries the required tags, changes no other file, and the validator reports zero errors.
