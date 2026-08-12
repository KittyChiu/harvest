---
name: create-learning-module
description: Interactively create a modular self-paced learning experience from a knowledge note, existing thought-leadership IP, raw notes, or a transcript. Produces separate participant and coach guides. Recommend creating a knowledge note when none exists while allowing direct use of approved raw sources. Confirm source coverage and key learning points, then design a concise experiential journey.
compatibility: Produces paired Markdown files ending in .participant.guide.md and .coach.guide.md. Python 3 is used only by the bundled validator.
---

# Create Learning Module

Create one self-contained self-paced module with two complementary guides. The participant guide stands alone. The coach guide helps a coach surface key learning points without repeating participant content.

## Source and module contract

Before analysis, confirm source authority, read-only inputs, create or revise mode, the approved existing destination directory, the exact two output filenames, and permitted files. Both filenames use the same module stem:

- `<module>.participant.guide.md`
- `<module>.coach.guide.md`

Reuse the destination directory supplied in the invocation or continuation context. If none is supplied, ask the user to identify an existing directory. Write both guides directly into that directory. Do not infer the directory name, create a directory or subfolder, or group the guides by artifact type. When delegating knowledge-note creation, pass the same destination directory in the continuation context.

Use an approved knowledge note when supplied. If none is available, offer three explicit choices: create one first through an available specialist (recommended), continue directly from approved raw sources, or choose an existing note. Never invoke another skill automatically or treat a knowledge note as a prerequisite.

Discover source content without assuming headings or structure. Extract a concise task-local source contract with stable descriptive IDs. Begin with every item unclassified; propose learner-facing, coach-only, optional, or excluded dispositions and obtain user approval. Scope follows the module purpose, not source headings.

Keep the module composable: teach one coherent capability, produce one reusable learner output, state prerequisites explicitly, and avoid dependencies on module numbering, sequence, or another module's internal content.

Read [references/learning-design.md](references/learning-design.md) for experiential design, source markers, audience separation, modularity, and validation.

## Approval gate

Before writing:

1. Confirm the approved source contract and dispositions.
2. Propose up to three key learning points, one realistic opening scenario, a short exercise that reveals the core ideas, and an open question connecting them to the learner's own work.
3. Confirm learner, desired change, prerequisites, available time, depth, tools, exclusions, reusable output, destination directory, paired filenames, and write authority.
4. Surface time or scope trade-offs and obtain approval.

## Authoring

After approval:

1. Write the participant guide from [assets/participant-guide-template.md](assets/participant-guide-template.md) as one journey: **Scenario → Exercise → Reflection → Takeaways and next step**. Keep the last two stages reflective and participant-led.
2. Make every participant instruction and self-check independently usable. Allow brief `Tip` callouts that help the learner proceed; do not include coach-directed notes, a coach appendix, delivery logistics, or the source contract.
3. Write the coach guide from [assets/coach-guide-template.md](assets/coach-guide-template.md). Use level-3 numbered stage headings with ordered, unordered, or checklist items as appropriate. Point to participant stages; do not copy explanations, exercises, instructions, or answers.
4. Put learner-facing source markers beside participant content. Put coach-only markers and the complete invisible `source-contract` in the coach guide; keep optional and excluded reasons there too.
5. Remove repeated outcomes, recaps, planning tables, scripts, and sections that do not advance the experiential journey.
6. Validate the pair:

```bash
python3 .github/skills/create-learning-module/scripts/validate_module.py "<module>.participant.guide.md" "<module>.coach.guide.md"
```

## Completion

Complete only when both guides share a module stem and are written directly in the approved destination directory; no directory or subfolder was created; every source item has exactly one disposition; participant and coach content are separated; the participant can complete the module alone; the coach guide reinforces rather than duplicates; the module has one reusable output and no hidden dependency on another module; approved meaning is preserved; and the validator reports zero errors.

