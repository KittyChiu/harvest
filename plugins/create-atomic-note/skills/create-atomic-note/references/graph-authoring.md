# Atomic-pattern authoring

## Select a reusable pattern

A pattern connects a recurring situation to a practical response and explains why that response should work. It must be reusable beyond the source event without becoming so broad that it loses its trigger or boundary.

Prefer titles that state the pattern, such as:

- `golden-paths-reduce-cognitive-load`
- `small-batches-shorten-feedback-loops`

Reject topic containers such as `everything-about-platform-engineering`, event summaries, isolated facts, personal reminders, and collections of loosely related advice.

When reading a source:

1. Remove chronology, repetition, and delivery commentary.
2. Group observations that support the same response and mechanism.
3. Preserve contradictions, uncertainty, failures, and boundary conditions.
4. Distinguish learning present in the source from recommendations synthesized for the note.
5. Propose no more than three patterns and write only the selected one.

## Test the causal chain

Check the proposed note in both directions:

- Forward: does the learning support the pattern, and does the mechanism explain why the practice should affect the named situation?
- Reverse: do the signals actually indicate the pattern is relevant, and do the constraints identify when the mechanism would fail?

Do not use outcomes, popularity, or confidence as substitutes for a mechanism. If the source supports an observation but not a causal explanation, preserve that uncertainty rather than inventing one.

## Choose the parent MOC

Use one approved existing MOC whose scope contains the pattern. If none fits, offer a domain-MOC specialist or stop.

The MOC entry is navigation, not a second summary. Describe the decision a reader can make by opening the note:

```markdown
- [Golden paths reduce cognitive load](platform-golden-paths-reduce-cognitive-load.md) — Decide when a maintained default can remove repeated delivery choices.
```

## Create meaningful relationships

Choose a relationship type by the role the linked note plays:

- **Prerequisite** — must be understood or present first.
- **Extension** — develops this pattern further.
- **Contrast** — exposes a meaningful alternative or boundary.
- **Example** — demonstrates this pattern in a concrete case.

Explain the connection in the same list item. Do not add a link because two notes share a topic. Prefer an explicit no-relationship state over planned, dangling, or decorative links.

Use portable relative Markdown links by default. Wiki-style links are acceptable when the selected PKM tool prefers them. Every target must already exist in the approved knowledge directory.

## Apply graph tags

Use inline tags for three independent filtering dimensions:

- domain: one or more subject tags;
- workflow: exactly one of `#draft`, `#review`, or `#publish`;
- visibility: exactly one of `#private` or `#public`.

Tags do not replace MOC membership or relationship prose. Do not add tool-specific front matter, properties, queries, transclusions, or plugins unless explicitly requested.

## Review

Before completion, confirm:

- the note contains one reusable pattern rather than a topic;
- source learning and synthesized recommendations remain distinguishable;
- the causal chain works in both directions;
- the MOC is the correct navigation home;
- every relationship has the right type and a supported explanation;
- uncertainty and constraints are preserved;
- no learning, evidence, example, or causal claim was invented.
