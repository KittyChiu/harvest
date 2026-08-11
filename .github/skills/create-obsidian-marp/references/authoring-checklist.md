# Marp authoring checklist

## Source extraction

When the source is a concise knowledge note, extract its available Core Idea, Guiding Principles, Practices, Examples, Constraints, and Related Ideas. Treat these as the canonical content boundary; Related Ideas are optional connections, not automatic deck scope.

Derive the presentation objective, audience tension, narrative spine, and call to action for the approved brief. Use a framework, evidence claim, or provenance detail only when the source explicitly provides it. Label new framing, transitions, analogies, and inferred models as presentation synthesis.

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
python3 .github/skills/create-obsidian-marp/scripts/validate_marp.py "<deck.md>"
```

Inspect slide count, notes, raw HTML, front matter, density, dependencies, claims, canonical terminology, confirmed configuration, and narrative coherence.

