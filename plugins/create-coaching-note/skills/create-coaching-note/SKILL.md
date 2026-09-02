---
name: create-coaching-note
description: Create or revise the companion coaching note for one atomic knowledge note. Use when turning an approved atomic idea into supportive coaching guidance with considerations, start-continue-stop practices, questions, metrics, and resistance support.
license: MIT
compatibility: Produces portable Markdown for file-based PKM tools. Python 3 is required for validation.
---

# Create Coaching Note

Create one concise coaching companion for one approved atomic note. The coaching note helps someone explore and apply the idea without turning it into a rigid implementation playbook.

## Companion contract

The source atomic note is read-only. Write the companion directly beside it in the approved existing knowledge directory:

- source: `<domain>-<idea-slug>.md`
- output: `<domain>-<idea-slug>.coach.md`

The coaching note belongs to the same MOC as the atomic note and links back with `Companion to: [<atomic-note-title>](<atomic-stem>.md)`.

This command intentionally produces no participant guide, course sequence, module folder, or duplicate explanation of the atomic idea.

Read [references/coaching-design.md](references/coaching-design.md) and use [assets/coaching-note-template.md](assets/coaching-note-template.md).

## Source and write gate

Before analysis, confirm:

- the authoritative atomic note;
- the atomic note and MOC are read-only;
- create or revise mode;
- the approved existing knowledge directory;
- the exact `<atomic-stem>.coach.md` output filename;
- every file permitted to change;
- the intended coaching audience and context.

If no approved atomic note exists, offer to invoke an available atomic-note specialist or stop. Do not create an atomic note inside this skill.

## Interaction flow

1. Read the atomic note and its parent MOC. Read an existing coaching companion only in revise mode.
2. Extract the idea, practices, constraints, and supported relationships without reopening the atomic note's original sources.
3. Propose a compact coaching plan:
   - the coaching intent;
   - one or two considerations;
   - start, continue, and stop practices;
   - two or three open questions;
   - observable signals or metrics;
   - a supportive response to likely resistance.
4. Flag recommendations that are synthesis rather than claims from the atomic note.
5. Obtain explicit approval for the plan, tags, exact output path, and permitted files.
6. Write or revise only the coaching note.

## Coaching rules

- Invite reflection and choice; do not prescribe a universal rollout.
- Make `Start`, `Continue`, and `Stop` practical and proportionate.
- Prefer enabling conditions, recognition, examples, and small experiments over mandates or punishment.
- Use metrics as learning signals, not targets that encourage performative behavior.
- Include the source note's domain tags, exactly one workflow tag, exactly one visibility tag, and `#coaching`.
- Keep the parent MOC and companion links explicit.
- Use portable relative Markdown links by default. Wiki-style links are allowed when the selected PKM tool uses them.
- Do not copy whole sections from the atomic note.
- Do not invent evidence, outcomes, quotes, or certainty.

## Validate

Run:

```bash
python3 "<skill-directory>/scripts/validate_coaching_note.py" "<atomic-note.md>" "<atomic-note.coach.md>"
```

Resolve `<skill-directory>` from this `SKILL.md`. Fix every error, then qualitatively check that the guidance is humane, non-coercive, grounded in the atomic note, and useful in the named coaching context.

## Completion

Complete only when one coaching note is written beside the atomic note, uses the required companion filename, belongs to the same MOC, links to the atomic note, includes all coaching sections and tag categories, changes only approved files, and the validator reports zero errors.
