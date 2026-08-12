---
name: create-facilitator-guide
description: Interactively create a practical workshop facilitator guide from a canonical knowledge note, existing thought-leadership IP, raw notes, or a transcript. Recommend creating a knowledge note when none exists, while allowing direct use of approved raw sources. Confirm source coverage and three key takeaways, then tailor teaching, exercises, demonstrations, debriefs, and assessment.
compatibility: Produces self-contained Markdown. Python 3 is used only by the bundled validator.
---

# Create Facilitator Guide

Create a guide another facilitator can run reliably. Expand the approved source's **what** into a practical **how** without changing its meaning.

## Input and source rules

Require an IP source. Before analysis, confirm the source files and their authority, files that remain read-only, create or revise mode, the exact output path, and the exact files permitted to change. Develop audience, duration, format, and constraints through the takeaway conversation when absent.

Check whether the user supplied or identified an approved knowledge note. Use user-provided paths and project conventions discovered from local documentation; do not assume a storage directory. Confirm authority before using a discovered file; a matching filename alone does not make it authoritative. If no approved note is available, ask which path to use:

- **Create a knowledge note first (recommended)** — discover an available specialist skill whose description matches creating a concise knowledge note, invoke it with the approved raw sources and continuation context, preserve its approval gates, and resume this workflow only after the note is approved and complete.
- **Continue from raw sources** — keep the skill atomic and do not create a knowledge note. Extract and confirm a task-local content contract from the approved IP, notes, or transcript before workshop design.
- **Choose an existing knowledge note** — let the user identify another note.

Do not invoke another skill automatically. The recommendation is a user choice, not a prerequisite. If no matching specialist is available, offer raw-source mode rather than implementing knowledge-note creation inside this skill.

Use source precedence: approved knowledge note, approved IP, transcript/notes, then clearly separated facilitation design. Discover the source's actual structure without assuming section names, order, or heading level. Extract only candidate claims, principles, practices, examples, and boundaries that may belong in the workshop; do not classify every source paragraph as required content. Assign stable descriptive IDs and confirm the task-local content contract with the user. Preserve approved terminology and claims. Treat a framework, audience problem, learning objectives, and assessment criteria as facilitation design unless the source states them explicitly.

Begin with every item in the approved source contract unclassified. Propose one disposition for each: participant-facing, facilitator-only, optional, or excluded. The workshop purpose, audience, time, and user-approved coverage contract determine the disposition; never infer it from a heading name. Allow the user to classify a whole source group or override individual items.

Do not expect the knowledge note to contain separate objectives, rationale, glossary, metadata, provenance, or an extraction map. Do not reopen its original sources merely to reconstruct omitted detail unless the user approves those sources for this task.

Read [references/workshop-design-guide.md](references/workshop-design-guide.md) for coverage and takeaway formatting, contract fields, learning design, activity requirements, assessment, and alignment checks.

## Mandatory takeaway gate

**Do not design or modify the guide immediately after reading the source.**

1. Resolve the source path: use the supplied knowledge note, delegate note creation only with user approval, or confirm atomic raw-source mode. Inventory every item in the resulting source contract.
2. Propose a coverage contract with a disposition and reason for each item. Let the user change dispositions at section or item level, then confirm it.
3. Extract the teachable core from the confirmed participant-facing content and the boundaries facilitators must retain.
4. Propose three memorable, coherent takeaways—not activities or formal objectives. Together they must organize, not replace or narrow, all participant-facing content.
5. Explain each takeaway's message, importance, practice change, application, and source coverage.
6. Ask what to keep, change, replace, or combine. Offer **No opinion — recommend**, **All three**, and **None — reanalyse**.
7. Refine one focused question at a time: audience, desired change, takeaway wording, duration, mode, group size, tools, exclusions, and intended depth.
8. Surface scope/time trade-offs rather than silently compressing practice or dropping approved content.
9. Present the workshop contract, including the confirmed coverage contract and write authority, and obtain explicit approval.

## Design and authoring

After approval:

1. Derive observable learning objectives and evidence from the takeaways.
2. Create a source-to-guide map showing the destination for every participant-facing and facilitator-only item. Participant-facing content must appear in teaching, demonstration, practice, debrief, or assessment; facilitator-only content must appear in preparation, a boundary, a watch-out, or a fallback.
3. Map each approved takeaway through a relatable experience, teaching with or without demonstration, practise, and debrief with a call to action.
4. Design the experience → explain → demonstrate → practise → critique → transfer journey.
5. Build a realistic agenda whose timings add up.
6. Fully specify every activity, facilitator talk track, fallback, debrief, application, and assessment.
7. Write from [assets/facilitator-guide-template.md](assets/facilitator-guide-template.md).
8. Embed the complete approved item list in a `source-contract` marker and record every confirmed disposition with the markers defined in the workshop-design guide, regardless of source type.
9. Run the alignment checklist, perform a reverse coverage review, and run the bundled validator against the self-contained guide.

## Completion

The task is complete only when every approved source item has exactly one confirmed disposition; every participant-facing and facilitator-only item is faithfully conveyed in its mapped destination; every optional or excluded item has an approved reason; the user approved the takeaways and workshop contract; every approved takeaway moves from a relatable experience through teaching, practise, and debrief to a call to action; the bundled validator exits with code `0` and reports zero errors; another facilitator can run the guide without reconstructing intent; participants actively apply the idea; learning is observable; approved source meaning is preserved; and participants leave with a reusable output or next action.

