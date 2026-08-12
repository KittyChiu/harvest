# Facilitator-guide design reference

## Teachable-core extraction

Discover the approved source's actual structure without assuming section names, order, or heading level. Extract a concise set of candidate content items. Group repetition and omit meeting logistics or production chatter. Assign stable descriptive IDs, present the extracted items for approval, and treat that approved list as the task-local source contract.

## Source coverage contract

Before takeaway selection, inventory the source in this form:

| Source ID | Source item | Proposed disposition | Approved disposition | Workshop destination or reason |
|---|---|---|---|---|
| `why-this-matters-1` | First item under `Why This Matters` | Participant-facing | Participant-facing | Takeaway 1 teaching and practice |
| `facilitation-risks-1` | First item under `Facilitation Risks` | Facilitator-only | Facilitator-only | Watch-out in Activity 2 |
| `further-reading-*` | Entire `Further Reading` section | Excluded | Excluded | Outside this workshop's purpose |

Create stable source IDs from the source's own labels where useful, or from concise descriptive item labels. Use `<group-slug>-*` to classify a whole approved group as optional or excluded. Every item begins unclassified. Propose dispositions from the workshop purpose, audience, time, and desired behaviour change, explain the choices, and obtain explicit user confirmation.

Use these dispositions:

- **Participant-facing** — participants encounter and apply the item in teaching, demonstration, practice, debrief, or assessment.
- **Facilitator-only** — the facilitator needs the item as preparation, a boundary, a watch-out, or a fallback, but participants do not need it as a learning outcome.
- **Optional** — suitable only if time, audience, or format permits; record the approved reason.
- **Excluded** — deliberately outside this workshop; record the approved reason.

After approval, create a source-to-guide map and record each disposition near its destination:

```markdown
<!-- source: ways-of-working-1 -->
<!-- source-facilitator: caveats-1 -->
<!-- source-optional: related-topics-1 | reason: Only for advanced groups -->
<!-- source-excluded: further-reading-* | reason: Outside this workshop's purpose -->
```

`source` means participant-facing and may also be written as `source-participant`. The legacy `canonical` forms are accepted. Multiple comma-separated IDs may share one marker. Add participant-facing or facilitator-only markers only where the item is conveyed. Optional and excluded markers require a reason confirmed by the user. Whole-group `-*` selectors are allowed only for optional and excluded dispositions.

Embed the complete approved task-local item list once in every guide:

```markdown
<!-- source-contract: outcome-focus, persist-learning, checkpoint-choice -->
```

This declares the approved source boundary for validation, independently of the source's file type or structure.

## Teachable-core design

Then derive only what the workshop needs:

- participant problem and motivation;
- concepts to understand;
- decisions or actions to perform;
- a teachable model or sequence, when supported;
- mistakes and boundaries;
- example or demonstration;
- practice task;
- observable evidence;
- durable participant artifact.

Label audience framing, learning objectives, activities, assessment, and any new model as facilitation design rather than approved source content. The confirmed coverage contract, not a section heading, decides what is participant-facing, facilitator-only, optional, or excluded.

## Three-takeaway menu

Present:

| Key takeaway | Core message | Why it matters | How it changes practice | Example or application |
|---|---|---|---|---|

Derive takeaways from all content classified as participant-facing, plus audience needs, available time, and desired behavior change. The takeaways must collectively organize all participant-facing items. Use a source framework only when one is explicitly present.

Offer:

- **No opinion — recommend the best three**
- **All three**
- **None — reanalyse**

If three takeaways exceed the available duration, ask the user to reduce scope, extend time, or accept less application time.

## Workshop contract

Confirm:

- audience and starting point;
- confirmed source coverage contract;
- three key takeaways;
- duration and format;
- constraints, tools, and prerequisites;
- required examples or demonstrations;
- exclusions and boundaries;
- create or revise mode;
- exact output path;
- read-only source files;
- exact files permitted to change.

## Learning objectives

Derive objectives after takeaway approval. Use observable verbs such as distinguish, diagnose, choose, construct, apply, compare, critique, validate, and transfer. Avoid “know,” “learn,” and “be aware of” unless paired with evidence.

## Learning journey

Prefer:

1. **Experience** — surface the problem.
2. **Explain** — teach the minimum model.
3. **Demonstrate** — apply it to a realistic case.
4. **Practise** — use it on authentic work.
5. **Critique** — compare and expose risks.
6. **Transfer** — create a durable artifact or commitment.

Use short teaching segments followed by active practice.

## Agenda rules

Include opening, instruction, transitions, setup, exercise work, report-back, debrief, breaks when needed, and close. Each row states time, activity, participant action, and outcome. Timings must add up.

## Activity specification

Every activity includes:

- purpose and duration;
- setup and materials;
- facilitator instructions;
- participant instructions;
- expected output;
- debrief questions;
- watch-outs;
- fallback for time, tools, or participation failure.

## Facilitator narrative

Provide concise talk tracks for opening, key concepts, transitions, demonstration setup, debrief synthesis, and close. Use grounded stories and analogies without copying slide notes wholesale.

## Application and assessment

Prefer authentic work over trivia. Define baseline, constraints, steps, measures, critique method, acceptance criteria, take-home artifact, and owner. Use the same measures when comparing approaches.

## Alignment checklist

- Every approved source item has exactly one confirmed disposition.
- Every participant-facing and facilitator-only item appears in its mapped destination.
- Every optional or excluded item has an approved reason.
- Every approved takeaway follows this participant journey: relatable experience → teaching with or without demonstration → practise → debrief and call to action.
- Every objective appears in the agenda.
- Every objective has practice or evidence.
- Activities have outputs and debriefs.
- Terminology matches the source of truth.
- Risks are taught where misuse is possible.
- The guide stands alone without slides.
- Optional slide references are not dependencies.

Run the validator:

```bash
python3 .github/skills/create-facilitator-guide/scripts/validate_guide.py "<guide.md>"
```

The validator checks contract completeness, conflicting dispositions, reasons, and whole-group selectors. It cannot judge approval or semantic fidelity. Perform a reverse coverage review against the confirmed contract: inspect each participant-facing and facilitator-only destination and confirm that it preserves the source item's complete meaning and terminology.

