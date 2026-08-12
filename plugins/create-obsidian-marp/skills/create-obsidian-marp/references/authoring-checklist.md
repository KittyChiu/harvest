# Marp authoring checklist

## Output routing

Reuse the approved existing destination directory from the invocation or continuation context. If absent, ask the user to identify one. Write the `.marp.md` file directly inside it. Do not infer a directory name or create a directory or artifact-specific subfolder.

## Source extraction

Discover the approved source's actual structure without assuming section names, order, or heading level. Extract a concise set of candidate content items. Group repetition and omit meeting logistics or production chatter. Assign stable descriptive IDs, present the extracted items for approval, and treat that approved list as the task-local source contract.

Derive the presentation objective, audience tension, narrative spine, and call to action for the approved brief. Use a framework, evidence claim, or provenance detail only when the source explicitly provides it. Label new framing, transitions, analogies, and inferred models as presentation synthesis.

Do not flatten uncertainty or fabricate quotes, outcomes, metrics, or consensus.

## Coverage contract

Before storytelling selection, inventory the approved source in this form:

| Source ID | Source item | Proposed disposition | Approved disposition | Reason |
|---|---|---|---|---|
| `why-this-matters-1` | First item under `Why This Matters` | Visible | Visible | Supports the objective |
| `further-reading-*` | Entire `Further Reading` section | Excluded | Excluded | Outside this deck's scope |

Create stable source IDs from the source's own labels where useful, or from concise descriptive item labels. Use `<group-slug>-*` to classify a whole approved group as optional or excluded. Every extracted item begins unclassified. Propose dispositions from the brief and presentation objective, explain the choices, and obtain explicit user confirmation.

After selecting the story, replace the planned beat with exact slide numbers to create the source-to-slide map. Record each approved disposition in the deck:

```markdown
<!-- source: ways-of-working-1 -->
<!-- source-notes: caveats-1 -->
<!-- source-optional: related-topics-1 | reason: Not needed for this audience -->
<!-- source-excluded: further-reading-* | reason: Outside this deck's objective -->
```

`source` means visible and may also be written as `source-visible`. The legacy `canonical` forms are accepted. Multiple comma-separated IDs may share one marker. Add visible or notes-only markers only where the item is conveyed. Optional and excluded markers require a reason confirmed by the user. Whole-group `-*` selectors are allowed only for optional and excluded dispositions.

Embed the complete approved task-local item list once in every deck:

```markdown
<!-- source-contract: outcome-focus, persist-learning, checkpoint-choice -->
```

This declares the approved source boundary for validation, independently of the source's file type or structure.

## Slide architecture

For each slide define story beat, purpose, assertion-led headline, evidence, visual form, and causal/emotional transition. Remove slides that do not advance the narrative.

The narrative spine is connective presentation design, not a content filter. Every item classified as visible in the confirmed coverage contract must remain visible. Split or reshape slides when necessary rather than hiding visible content in notes.

## Projection rules

- One primary idea per slide.
- Short headlines.
- Scannable body.
- Prefer 3–5 bullets or a small table.
- Split dense slides.
- Put explanation and caveats in notes.
- Keep the complete meaning of every item classified as visible on the slide; use notes only to deepen it.
- Label synthesis honestly.
- Avoid agenda-heavy openings, walls of prose, decorative jargon, and generic closes.

## Speaker notes

Every slide includes an HTML-comment speaker-note block. Empty blocks are valid. When notes are useful, include spoken setup, relevant story or analogy, inference, concrete example, optional audience prompt, transition, and caveat.

Use:

```markdown
<!--
Presenter narrative.

Transition: "That leads to..."
-->
```

Speaker-note comments are allowed Marp syntax and are exempt from the raw HTML restriction.

## Validation

Run:

```bash
python3 "<skill-directory>/scripts/validate_marp.py" "<deck.marp.md>"
```

Resolve `<skill-directory>` from the skill's `SKILL.md`; do not assume the plugin is installed in the current project.

The validator checks that every approved source item has exactly one disposition, optional and excluded dispositions have reasons, and whole-group selectors resolve to source items. It cannot judge approval or semantic fidelity. Perform a reverse coverage review against the confirmed contract: inspect each visible item without speaker notes and each notes-only item in its notes, then confirm that the destination preserves the complete meaning and approved terminology.

Also inspect slide count, notes, raw HTML, front matter, density, dependencies, claims, confirmed configuration, and narrative coherence. Report any approved notes-only or excluded items at completion.

Confirm that the deck is directly inside the approved destination directory and no directory or subfolder was created.
