---
name: create-atomic-note
description: Create or revise one atomic knowledge note and place it in a file-based PKM graph. Use when turning source material into a single reusable idea that belongs to a Map of Content (MOC), uses meaningful internal links, and carries domain, workflow, and visibility tags.
license: MIT
compatibility: Produces portable Markdown for file-based PKM tools. Python 3 is required for validation.
---

# Create Atomic Note

Create one atomic note and make it navigable from one domain Map of Content (MOC). The capability is complete only when the note and MOC point to the same idea.

## Graph contract

Use these four building blocks only:

1. Domain MOCs provide navigation.
2. Atomic notes hold knowledge.
3. Internal links express relationships.
4. Tags support filtering.

The source MOC and output note live directly in the approved existing knowledge directory:

- `<domain>-moc.md`
- `<domain>-<idea-slug>.md`

Use lowercase kebab-case filenames. The atomic note must belong to exactly one primary MOC. The MOC must already exist before this workflow writes. Do not create folders, MOCs, indexes, metadata registries, extraction maps, or graph databases.

Read [references/graph-authoring.md](references/graph-authoring.md) before proposing content. Use [assets/atomic-note-template.md](assets/atomic-note-template.md).

## Source and write gate

Before analysis, confirm:

- the authoritative source and which inputs remain read-only;
- create or revise mode;
- the approved existing knowledge directory;
- the domain and approved existing MOC;
- the exact atomic-note and MOC filenames;
- every file permitted to change.

If no MOC fits, offer to invoke an available domain-MOC specialist with the proposed domain, approved knowledge directory, and continuation context, or stop. Invoke it only with explicit consent and resume this workflow only after the MOC is approved and complete. Never create a MOC inside this skill or leave an atomic note orphaned.

## Interaction flow

1. Read the approved source and the chosen MOC. Inspect nearby notes only to detect duplication and supported relationships.
2. Extract up to three candidate atomic ideas. Each candidate must be one reusable claim, not a topic, source summary, or collection.
3. Ask the user to select one candidate or reframe it. Create separate notes in separate runs for other ideas.
4. Propose:
   - a claim-style title;
   - exact filenames;
   - one parent MOC;
   - domain, workflow, and visibility tags;
   - only relationships that can be explained in a sentence.
5. Obtain explicit approval for the content contract and permitted files.
6. Write or revise the atomic note, then add or update one descriptive entry in the existing MOC.

Do not ask for information already supplied. Combine confirmations when the user can approve them safely in one decision.

## Authoring rules

- Make the title express the reusable idea, not the broad topic.
- Keep the note self-contained and concise; remove transcript chronology, repetition, and production commentary.
- Preserve distinctive source terminology and meaningful uncertainty.
- Use `Parent: [<domain name>](<domain>-moc.md)`.
- Use `Tags:` with at least one domain tag, one workflow tag (`#draft`, `#review`, or `#publish`), and one visibility tag (`#private` or `#public`).
- Give the MOC the domain tag, `#moc`, one workflow tag, and one visibility tag too.
- Use the five sections in the atomic-note template.
- Use portable relative Markdown links by default. Wiki-style links are allowed when the selected PKM tool uses them.
- In `Relationships`, explain why each internal link matters. Never produce a list of unexplained links.
- Add the MOC entry as `- [<atomic-note-title>](<atomic-note>.md) — <navigation description>`.
- Do not invent quotes, evidence, causality, or related notes.

## Validate

Run:

```bash
python3 "<skill-directory>/scripts/validate_atomic_note.py" "<atomic-note.md>" "<domain-moc.md>"
```

Resolve `<skill-directory>` from this `SKILL.md`. Fix every error, then qualitatively confirm that the note contains one idea and every relationship sentence states a real connection.

## Companion assets

After validation, report:

- whether `<atomic-stem>.coach.md` exists;
- whether the shared `<domain>.marp.md` presentation exists;
- when that presentation exists, whether it already has a `Source:` link for this atomic note.

Offer to invoke available specialist skills only with explicit consent. The coaching specialist creates or updates the atomic note's companion. The Obsidian Marp specialist creates or updates the domain's single shared presentation. Pass the approved atomic note, MOC, knowledge directory, and exact target filename. Do not generate either asset inside this skill.

## Completion

Complete only when the atomic note is in the approved knowledge directory, names one parent MOC, carries all three tag categories, contains one reusable idea, uses only meaningful internal links, has a descriptive entry in the MOC, changes only approved files, and the validator reports zero errors.
