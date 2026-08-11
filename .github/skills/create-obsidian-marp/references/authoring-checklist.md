# Marp authoring checklist

## Source extraction

Extract thesis, audience problem, framework, terminology, principles, practices, example/demo, boundaries, evidence, and action. Inventory problems, insights, stories, analogies, language, practices, proof, and open questions.

Do not flatten uncertainty or fabricate quotes, outcomes, metrics, or consensus.

## Slide architecture

For each slide define story beat, purpose, assertion-led headline, evidence, visual form, and causal/emotional transition. Remove slides that do not advance the narrative.

## Projection rules

- One primary idea per slide.
- Short headlines.
- Scannable body.
- Prefer 3–5 bullets or a small table.
- Split dense slides.
- Put explanation and caveats in notes.
- Label synthesis honestly.
- Avoid agenda-heavy openings, walls of prose, decorative jargon, and generic closes.

## Speaker notes

Each substantive slide includes spoken setup, relevant story/analogy, inference, concrete example, optional audience prompt, transition, and caveat where useful.

Use:

```markdown
<!--
Presenter narrative.

Transition: "That leads to..."
-->
```

## Validation

Run:

```bash
python3 .github/skills/create-obsidian-marp/scripts/validate_marp.py "<deck.md>"
```

Inspect slide count, notes, raw HTML, front matter, density, dependencies, claims, canonical terminology, confirmed configuration, and narrative coherence.

