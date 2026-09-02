---
name: create-atomic-note
description: Create or revise one reusable knowledge pattern in a file-based PKM graph. Use when source material contains a repeatable rule that should be grounded in learning, connected to one domain MOC, and expressed with practical signals, actions, constraints, and relationships.
license: MIT
compatibility: Produces portable Markdown for file-based PKM tools. Python 3 is required for validation.
---

# Create Atomic Note

Create or revise one self-contained, reusable pattern and make it navigable from exactly one domain Map of Content (MOC).

## Artifact contract

Write the note and update its MOC directly in the approved existing knowledge directory:

- source MOC: `<domain>-moc.md`
- atomic note: `<domain>-<pattern-slug>.md`

Use lowercase kebab-case filenames. The MOC must already exist and remain the note's only parent. Do not create folders, MOCs, coaching notes, presentations, indexes, registries, or graph databases.

Use [assets/atomic-note-template.md](assets/atomic-note-template.md) as the artifact schema. Read [references/graph-authoring.md](references/graph-authoring.md) for selection, grounding, graph, and relationship decisions.

## Source and write gate

Before analysis, confirm:

- the authoritative source and every read-only input;
- create or revise mode;
- the approved existing knowledge directory;
- the domain and approved existing MOC;
- the exact atomic-note and MOC filenames;
- the atomic note and MOC as the only files permitted to change.

If no existing MOC fits, offer an available domain-MOC specialist with the proposed domain and continuation context, or stop. Invoke another skill only with explicit consent. Never create a MOC inside this skill or leave an atomic note orphaned.

## Workflow

1. Read the approved source and MOC. In revise mode, read the existing atomic note. Inspect nearby note titles only to detect duplication and supported relationships.
2. Extract no more than three candidate patterns. Before presenting them, replace customer, organization, and team names with neutral role descriptions and remove source attribution. Each candidate must include:
   - one reusable “When X, do Y, because Z” rule;
   - the learning from the source that supports it;
   - the smallest practical action;
   - observable situations that signal when it applies;
   - known constraints.
3. Ask the user to select or reframe one candidate. Handle other patterns in separate runs.
4. Propose the title, exact filenames, parent MOC, tags, template-aligned content outline, and supported typed relationships.
5. Obtain explicit approval for the content contract and permitted files.
6. Create or revise the atomic note, then add or update its one descriptive MOC entry.

Do not ask for information already supplied. Combine confirmations when the user can approve them safely in one decision.

## Authoring rules

- Express one reusable pattern, not a topic, source summary, broad principle collection, or implementation plan.
- Preserve distinctive non-identifying terminology, uncertainty, and boundaries from the source.
- Obfuscate customer, organization, and team names with stable neutral roles such as `a customer`, `a product team`, or `an enablement group`. Remove identifying combinations of project names, locations, dates, and organizational details when they could reveal the source.
- Use source material only for grounding. Do not put source names, filenames, meeting or transcript references, citations, attribution fields, or external source URLs in the atomic note or its MOC entry.
- Separate what was learned from what the pattern recommends.
- Explain why the pattern works through cause and effect, not unsupported benefits.
- Keep the practice observable and signals recognizable before or during application.
- Use `Parent: [<domain name>](<domain>-moc.md)`.
- Use `Tags:` with at least one domain tag, exactly one workflow tag (`#draft`, `#review`, or `#publish`), and exactly one visibility tag (`#private` or `#public`).
- Use the template's sections once each and in their defined order. Replace every instructional prompt and placeholder.
- Use portable relative Markdown links by default. Wiki-style links are allowed when the selected PKM tool uses them.
- In `Relationships`, use only supported prerequisite, extension, contrast, or example links and explain each connection. If none exist, state that explicitly.
- Add the MOC entry as `- [<atomic-note-title>](<atomic-note>.md) — <navigation description>`.
- Do not invent learning, evidence, causality, examples, outcomes, or relationships.

## Validate

Run:

```bash
python3 "<skill-directory>/scripts/validate_atomic_note.py" "<atomic-note.md>" "<domain-moc.md>"
```

Fix every error. Then confirm qualitatively that the source supports the learning without being named or linked, customer and team identities are obfuscated, the learning supports the pattern, the mechanism explains the recommendation, the signals indicate when to use it, and the constraints prevent overgeneralization.

## Companion assets

After validation, report:

- whether `<atomic-stem>.coach.md` exists;
- whether `<domain>.marp.md` exists;
- when the presentation exists, whether it has a `Source:` link for this note.

Offer available coaching or presentation specialists only with explicit consent. Pass the approved atomic note, MOC, knowledge directory, and exact target filename. Do not create companion assets inside this skill.

## Completion

Complete only when the approved atomic note and MOC are the only changed files; the note follows the template with no prompts or placeholders left, has one parent MOC and a descriptive MOC entry, carries all tag categories, contains one source-grounded reusable pattern without source attribution or external source URLs, obfuscates customer and team identities, uses only meaningful and resolvable relationships, and the validator reports zero errors.
