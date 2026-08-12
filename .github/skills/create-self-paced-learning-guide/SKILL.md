---
name: create-self-paced-learning-guide
description: Interactively create a concise self-paced learning guide from a canonical knowledge note, existing thought-leadership IP, raw notes, or a transcript. Recommend creating a knowledge note when none exists while allowing direct use of approved raw sources. Confirm source coverage and key learning points, then design intuitive explanations, examples, practice, self-checks, and optional coaching notes.
compatibility: Produces self-contained Markdown with a .guide.md extension. Python 3 is used only by the bundled validator.
---

# Create Self-Paced Learning Guide

Create an intuitive guide a learner can complete independently. Optional coaching notes reinforce key learning points but must never carry instructions or content required to complete the guide.

## Input and source rules

Require an IP source. Before analysis, confirm the source files and their authority, files that remain read-only, create or revise mode, the exact `.guide.md` output path, and the exact files permitted to change. Develop learner profile, available time, format, and constraints through the learning-point conversation when absent.

Check whether the user supplied or identified an approved knowledge note. Use user-provided paths and project conventions discovered from local documentation; do not assume a storage directory. Confirm authority before using a discovered file; a matching filename alone does not make it authoritative. If no approved note is available, ask which path to use:

- **Create a knowledge note first (recommended)** — discover an available specialist skill whose description matches creating a concise knowledge note, invoke it with the approved raw sources and continuation context, preserve its approval gates, and resume this workflow only after the note is approved and complete.
- **Continue from raw sources** — keep the skill atomic and do not create a knowledge note. Extract and confirm a task-local content contract from the approved IP, notes, or transcript before learning-guide design.
- **Choose an existing knowledge note** — let the user identify another note.

Do not invoke another skill automatically. The recommendation is a user choice, not a prerequisite. If no matching specialist is available, offer raw-source mode rather than implementing knowledge-note creation inside this skill.

Use source precedence: approved knowledge note, approved IP, transcript/notes, then clearly separated learning design. Discover the source's actual structure without assuming section names, order, or heading level. Extract only candidate claims, principles, practices, examples, and boundaries that may belong in the guide; do not classify every source paragraph as required content. Assign stable descriptive IDs and confirm the task-local content contract with the user. Preserve approved terminology and claims. Treat learner framing, learning objectives, activities, and self-checks as learning design unless the source states them explicitly.

Begin with every item in the approved source contract unclassified. Propose one disposition for each: learner-facing, coach-only, optional, or excluded. The guide purpose, learner, time, and user-approved coverage contract determine the disposition; never infer it from a heading name. Allow the user to classify a whole source group or override individual items.

Do not expect the knowledge note to contain separate objectives, rationale, glossary, metadata, provenance, or an extraction map. Do not reopen its original sources merely to reconstruct omitted detail unless the user approves those sources for this task.

Read [references/self-paced-learning-design.md](references/self-paced-learning-design.md) for coverage markers, learning-point formatting, concise learning design, coaching notes, self-checks, and alignment checks.

## Learning contract gate

**Do not design or modify the guide immediately after reading the source.**

1. Resolve the source path: use the supplied knowledge note, delegate note creation only with user approval, or confirm atomic raw-source mode. Inventory every item in the resulting source contract.
2. Propose a coverage contract with a disposition and reason for each item. Let the user change dispositions at section or item level, then confirm it.
3. Extract the teachable core from learner-facing content and the boundaries coaching notes must reinforce.
4. Propose up to three memorable key learning points. Together they must organize, not replace or narrow, all learner-facing content.
5. Explain each point's message, importance, practice change, application, and source coverage.
6. Ask what to keep, change, replace, or combine. Offer **No opinion — recommend**, **Keep all**, and **None — reanalyse**.
7. Confirm the learner, desired change, available time, format, tools, exclusions, intended depth, coverage contract, and write authority. Surface time/scope trade-offs and obtain approval.

## Design and authoring

After approval:

1. Derive observable learning outcomes and evidence from the approved learning points.
2. Create a source-to-guide map for every learner-facing and coach-only item. Learner-facing content belongs in explanation, example, practice, reflection, or self-check. Coach-only content belongs in optional section coaching notes or the coach appendix.
3. Build a short journey for each learning point: relatable situation → concise explanation → example → practice → self-check.
4. Write so a learner can follow every instruction and complete every activity without a coach, cohort, breakout room, presentation, or live demonstration.
5. Add brief section coaching notes only where they help a coach reinforce a key point, ask a useful question, or notice a misconception. Removing all coach notes must leave a complete guide.
6. Default to one explanation, one example, one practice, and one self-check per learning point. Remove repeated summaries, alignment tables, scripts, logistics, and duplicated instructions.
7. Write from [assets/self-paced-learning-guide-template.md](assets/self-paced-learning-guide-template.md).
8. Put the visible source coverage table, when useful, and the complete `source-contract` marker in the coach appendix. Keep disposition markers as invisible HTML comments beside their mapped content.
9. Run the alignment checklist, perform a reverse coverage review, and run the bundled validator against the self-contained `.guide.md` file.

## Completion

The task is complete only when every approved source item has exactly one confirmed disposition; every learner-facing and coach-only item is faithfully conveyed in its mapped destination; every optional or excluded item has an approved reason; the user approved the key learning points and learning contract; the learner can complete the guide without assistance; coaching notes are optional and concise; source metadata is confined to the coach appendix; the filename ends in `.guide.md`; the bundled validator exits with code `0` and reports zero errors; learning is observable; approved source meaning is preserved; and the learner leaves with a reusable output or next action.

