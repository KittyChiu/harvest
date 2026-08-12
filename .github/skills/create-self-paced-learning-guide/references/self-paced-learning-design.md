# Self-paced learning design reference

## Source coverage contract

Discover the approved source's structure without assuming section names, order, or heading level. Extract a concise set of candidate content items, group repetition, and omit production chatter. Assign stable descriptive IDs and confirm the task-local source contract.

Use these dispositions:

- **Learner-facing** — the learner encounters and applies the item in an explanation, example, practice, reflection, or self-check.
- **Coach-only** — an optional coaching note uses the item to reinforce a key point, ask a useful question, or notice a misconception.
- **Optional** — include only when time, learner needs, or format permits; record the approved reason.
- **Excluded** — deliberately outside the guide; record the approved reason.

Record each disposition near its destination with HTML comments:

```markdown
<!-- source: outcome-focus -->
<!-- source-coach: reset-caveat -->
<!-- source-optional: advanced-patterns-* | reason: Advanced learners only -->
<!-- source-excluded: further-reading-* | reason: Outside this guide's purpose -->
```

`source` means learner-facing and may also be written as `source-learner`. Legacy `canonical`, `source-participant`, and `source-facilitator` forms remain accepted. Multiple comma-separated IDs may share one marker. Optional and excluded markers require a user-approved reason. Whole-group `-*` selectors are allowed only for optional and excluded dispositions.

Embed the complete approved item list once in the coach appendix:

```markdown
<!-- source-contract: outcome-focus, persist-learning, checkpoint-choice -->
```

Keep the complete contract out of the learner flow. Disposition markers remain invisible beside mapped content. Include a visible coverage table in the coach appendix only when it helps review or maintenance.

## Teachable core

Derive only what the learner needs:

- a relatable problem and reason to care;
- concepts or decisions to understand;
- a realistic example;
- an authentic practice task;
- mistakes and boundaries;
- observable evidence;
- a reusable output or next action.

Label learner framing, activities, self-checks, and any new model as learning design rather than approved source content. The confirmed contract, not source structure, decides each disposition.

## Key learning points

Propose up to three points in this form:

| Key learning point | Message | Why it matters | Practice change | Application |
|---|---|---|---|---|

Together they must organize all learner-facing items without narrowing or repeating them. Use a source framework only when one is explicitly present.

## Learning contract

Confirm:

- learner and starting point;
- desired change and reusable output;
- approved source coverage;
- key learning points;
- available time and format;
- tools, prerequisites, exclusions, and boundaries;
- create or revise mode;
- exact `.guide.md` output path;
- read-only sources and files permitted to change.

## Learner journey

For each learning point, use:

1. **Relate** — surface a familiar situation.
2. **Explain** — teach the minimum useful model.
3. **Show** — give one concrete example.
4. **Practise** — apply it to authentic work.
5. **Check** — verify understanding or inspect the output.

The guide must supply all instructions, inputs, examples, and checks needed for independent completion. Do not require a coach, cohort, presentation, breakout room, or live demonstration.

## Section coaching notes

Add a short `> **Coaching notes (optional):**` block only when coaching adds value. A note may:

- name the key point to reinforce;
- suggest one probing question;
- identify one likely misconception;
- offer one concise fallback.

Do not put required explanations, steps, answers, or source content only in coaching notes. Removing every coaching note must leave a complete guide.

## Conciseness rules

- Use one explanation, one example, one practice, and one self-check per learning point by default.
- State an instruction once, where the learner needs it.
- Prefer short paragraphs, direct steps, and worked examples over scripts or narration.
- Do not add agendas, timing tables, alignment tables, talk tracks, room setup, report-backs, or delivery logistics.
- Do not repeat learning points in multiple planning sections.
- Omit empty, irrelevant, or purely administrative sections.

## Practice and self-checks

Prefer authentic work over trivia. Every practice names its input, steps, expected output, and completion check. Self-checks may use a checklist, comparison, reflection prompt, worked answer, or acceptance criteria. Keep answers close enough for independent feedback without hiding essential learning in the coach notes.

## Alignment checklist

- Every approved source item has exactly one disposition.
- Every learner-facing and coach-only item appears in its mapped destination.
- Every optional or excluded item has an approved reason.
- Every learning point follows relate → explain → show → practise → check.
- The learner can complete all practices and checks independently.
- Coaching notes are optional, brief, and focused on key learning points.
- Terminology matches the source of truth.
- The learner leaves with a reusable output or next action.
- The complete source contract and any visible coverage table appear only in the coach appendix.
- The filename ends in `.guide.md`.

Run the validator:

```bash
python3 .github/skills/create-self-paced-learning-guide/scripts/validate_guide.py "<learning.guide.md>"
```

The validator checks filename and contract completeness, conflicting dispositions, reasons, and whole-group selectors. It cannot judge approval, conciseness, independent usability, or semantic fidelity. Review the finished guide as a learner and reverse-check each mapped source item.