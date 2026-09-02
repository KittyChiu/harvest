# Domain slide design

## Build one domain presentation

The MOC defines the source boundary. Its scope supplies orientation; every atomic note in its `Notes` section supplies one reusable idea. The result is one evolving domain presentation, not one deck per note and not a concatenation of mini-decks.

Choose one throughline that answers:

> What should this audience understand about the domain, and how should the sequence change their view or action?

A useful domain movement is:

1. **Orient** — define the domain and why it matters.
2. **Create tension** — identify the shared problem or decision.
3. **Develop** — sequence atomic ideas so each creates the need for the next.
4. **Apply** — combine the ideas in one example, contrast, or demonstration.
5. **Close** — resolve the opening and invite one domain-level next action.

## Map sources to slides

Before authoring, map every MOC note to a visible destination. Put a `Source:` line on the slide where its idea is conveyed. One note may support several slides, but it needs only one source declaration. Multiple related notes may share a slide only when the slide still has one primary idea.

Use available `.coach.md` companions to shape speaker notes. Put a `Coach source:` line and a non-empty speaker-note comment on the relevant slide. When an atomic note has no coaching companion, speaker notes are optional.

## Update without fragmenting

When the MOC changes:

1. Compare its atomic-note set with the existing presentation's source lines.
2. Add newly linked notes.
3. Revise changed ideas without duplicating them.
4. Remove sources and slides for notes no longer in the MOC.
5. Reorder and rewrite transitions so the presentation remains one story.
6. Preserve confirmed Marp configuration and useful unaffected slides.

Do not append every new idea to the end by default.

## Write for projection

- Use assertion-led headlines.
- Keep one primary claim per slide.
- Prefer 3-5 short bullets or one small table.
- Keep critical constraints visible.
- Split content the audience would need to read rather than hear.
- Use one connected example rather than unrelated anecdotes.

## Write coaching speaker notes

When a coaching companion exists, its relevant slide has a non-empty HTML comment beginning with:

```markdown
<!--
Coach cue: Ask what the audience notices before explaining the model.
-->
```

A cue may ask an open question, identify what to listen for, surface a constraint, suggest a non-coercive nudge, or provide a transition. Do not invent a coaching cue merely to populate every slide.

## Review

Confirm:

- there is exactly one presentation file for the domain;
- every MOC atomic note has a visible destination;
- no source remains after its note leaves the MOC;
- every available coaching companion informs at least one sourced speaker note;
- the sequence is one coherent domain story;
- the close resolves the opening.
