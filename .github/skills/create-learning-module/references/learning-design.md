# Learning module design reference

## Experiential journey

Design one module-level journey, not a repeated mini-lesson for every learning point:

1. **Scenario** — begin with a realistic situation, choice, or observation before explaining the ideas.
2. **Exercise** — use clear steps to help participants discover the core idea and concepts, introducing explanation when it becomes useful.
3. **Reflection** — use open prompts to connect the learning to a specific experience, choice, or pattern in the participant's work.
4. **Takeaways and next step** — let participants name what matters to them and consider one specific action.

The participant guide supplies everything required to complete this journey independently. Use examples only when needed to start or interpret the hands-on work.

## Audience separation

The participant guide contains the scenario, step-based exercise, connection to the participant's own work, and personal takeaway. Brief `> **Tip:**` callouts may clarify a step, suggest a shortcut, or help the learner recover. Keep each tip learner-facing and concise; do not hide required learning in it. The guide contains no coach-directed notes, coach appendix, source contract, delivery script, or facilitation logistics.

The coach guide uses the same four headings, numbered from `### 1. Scenario` through `### 4. Takeaways and next step`. Under each heading, use ordered steps, unordered prompts, or checklists as appropriate. Keep only useful questions, signals to notice, and possible nudges. Do not repeat participant explanations, instructions, exercises, or answers.

## Modular design

- Teach one coherent capability and produce one reusable output.
- State prerequisites as capabilities or inputs, not as required module names.
- Avoid numbering that fixes the module in a sequence.
- Do not rely on another module's terminology or hidden context.
- Keep each module independently usable so modules can later be ordered or combined.

## Output routing

Use the approved existing destination directory from the invocation or continuation context. If absent, ask the user to identify one. Write both guide files directly inside it. Do not infer a directory name or create a directory or artifact-specific subfolder. The paired filenames, not a folder hierarchy, identify the module.

## Source coverage

Discover the source structure without assuming headings. Extract concise candidate items, group repetition, assign stable IDs, and confirm one disposition per item:

- **Learner-facing** — conveyed and applied in the participant guide.
- **Coach-only** — helps a coach surface a key point or misconception.
- **Optional** — included only under an approved condition; requires a reason.
- **Excluded** — outside the module; requires a reason.

Use invisible comments:

```markdown
<!-- source: outcome-focus -->
<!-- source-coach: reset-caveat -->
<!-- source-optional: advanced-patterns-* | reason: Advanced learners only -->
<!-- source-excluded: further-reading-* | reason: Outside this module's purpose -->
<!-- source-contract: outcome-focus, reset-caveat, advanced-patterns-1 -->
```

Put learner-facing markers beside participant content. Put coach-only, optional, excluded, and the complete `source-contract` in the coach guide. Legacy `canonical`, `source-participant`, and `source-facilitator` aliases remain accepted. Whole-group `-*` selectors are allowed only for optional and excluded dispositions.

## Conciseness

- Use the four journey sections as the default participant structure.
- Use four level-3 numbered stage headings as the default coach structure; do not use a stage table.
- State each instruction or concept once, where its audience needs it.
- Omit agendas, timing tables, repeated outcomes, recaps, scripts, logistics, and empty sections.
- Prefer direct prompts and completion criteria over narration.

## Review and validation

Confirm that the scenario gives participants something meaningful to notice, the exercise reveals the core ideas through action, the open question connects them to real work, and the final reflection leads to one specific action. Review both guides for semantic fidelity and duplication, then run:

```bash
python3 .github/skills/create-learning-module/scripts/validate_module.py "<module>.participant.guide.md" "<module>.coach.guide.md"
```

The validator checks paired filenames, matching module stems, a shared parent directory, audience separation, and source coverage. It cannot judge whether the directory was user-approved or newly created, nor can it judge learning quality, conciseness, modularity, or semantic fidelity.