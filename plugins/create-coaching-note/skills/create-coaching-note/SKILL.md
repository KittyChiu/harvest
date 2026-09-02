---
name: create-coaching-note
description: Create or revise the coaching companion for one approved atomic pattern. Use when a coach needs concise teaching, recognition signals, discovery questions, an experiential exercise, adoption practices, progress signals, and resistance support.
license: MIT
compatibility: Produces portable Markdown for file-based PKM tools. Python 3 is required for validation.
---

# Create Coaching Note

Create one concise companion that helps a coach teach, explore, practise, and support adoption of one approved atomic pattern without turning it into a rigid rollout plan.

## Companion contract

The source atomic note and its MOC are read-only. Write the companion directly beside them in the approved existing knowledge directory:

- source: `<domain>-<pattern-slug>.md`
- output: `<domain>-<pattern-slug>.coach.md`

The companion uses the atomic note's parent MOC and links back with `Companion to: [<atomic-note-title>](<atomic-stem>.md)`. It produces no participant guide, course sequence, module folder, policy, or duplicate atomic note.

Use [assets/coaching-note-template.md](assets/coaching-note-template.md) as the artifact schema. Read [references/coaching-design.md](references/coaching-design.md) for grounding and facilitation decisions.

## Source and write gate

Before analysis, confirm:

- the authoritative atomic note;
- the atomic note and MOC as read-only inputs;
- create or revise mode;
- the intended coaching audience and context;
- the approved existing knowledge directory;
- the exact `<atomic-stem>.coach.md` output filename;
- the coaching note as the only file permitted to change.

If no approved atomic note exists, offer an available atomic-note specialist or stop. Invoke another skill only with explicit consent. Never create or revise the atomic note inside this skill.

## Workflow

1. Read the atomic note and its parent MOC. In revise mode, read the existing coaching companion.
2. Extract the pattern, practice, explanation of why it works, signals, learning, constraints, and supported relationships. Do not reopen the atomic note's original sources.
3. Propose a template-aligned coaching plan:
   - a plain-language explanation and misconception to correct;
   - observable situations that indicate the pattern may help;
   - three open discovery questions;
   - one small three-step experiential exercise and its expected outcome;
   - one or more Start, Continue, and Stop behaviours;
   - balanced progress signals, including what they cannot prove;
   - likely resistance and a supportive response.
4. Distinguish source-grounded guidance from synthesis. Flag any recommendation not directly present in the atomic note.
5. Obtain explicit approval for the plan, tags, exact output path, and permitted file.
6. Create or revise only the coaching note.

Do not ask for information already supplied. Combine confirmations when the user can approve them safely in one decision.

## Authoring rules

- Teach the pattern in simple language without copying whole source sections.
- Use observable behaviour in `Watch for`; do not diagnose motives or people.
- Write three genuine, open questions in `Conversation`, each ending in `?`.
- Keep `Exercise` small and safe. Provide exactly three populated numbered steps and a concrete expected outcome.
- Give `Start`, `Continue`, and `Stop` their own level-three headings under `Adoption`, with at least one practical bullet each.
- Use at least three balanced `Progress signals`: what to observe, what improvement could look like, and what the signals cannot prove.
- Pair every entry in `Common resistance` with a non-coercive response in the template's Markdown table.
- Invite reflection and choice. Prefer enabling conditions, recognition, examples, and small experiments over mandates, surveillance, punishment, or shame.
- Include the atomic note's domain tags, `#coaching`, exactly one workflow tag, and exactly one visibility tag.
- Keep the parent MOC and companion links explicit.
- Use portable relative Markdown links by default. Wiki-style links are allowed when the selected PKM tool uses them.
- Use the template's sections and adoption subsections once each and in their defined order. Replace every instructional prompt and placeholder.
- Do not invent learning, evidence, outcomes, quotes, causality, or certainty.

## Validate

Run:

```bash
python3 "<skill-directory>/scripts/validate_coaching_note.py" "<atomic-note.md>" "<atomic-note.coach.md>"
```

Resolve `<skill-directory>` from this `SKILL.md`. Fix every error. Then confirm qualitatively that the teaching is faithful, the questions support discovery, the exercise creates useful experience, the adoption guidance preserves choice, the progress signals are not targets, and resistance is treated as information.

## Completion

Complete only when the coaching note is the sole changed file; it sits beside and links to the approved atomic note; it uses the same parent MOC and required tags; every template prompt and placeholder has been replaced; its teaching, questions, exercise, adoption guidance, progress signals, and resistance support are grounded and usable; and the validator reports zero errors.
