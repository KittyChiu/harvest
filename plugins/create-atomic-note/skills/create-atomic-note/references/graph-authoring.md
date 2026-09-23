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

## Obfuscate identities and record safe provenance

Use the source as read-only grounding, not as body content to reproduce or cite. Before proposing candidates or drafting the note:

1. Replace customer, organization, account, and team names with stable neutral roles such as `a customer`, `a product team`, or `an enablement group`.
2. Remove project codenames, locations, dates, organizational details, and combinations of facts that could identify the source when those details are not essential to the pattern.
3. Generalize examples enough to be reusable while preserving the situation, mechanism, uncertainty, and constraint that make the learning valid.
4. Remove source names, filenames, meeting and transcript references, citations, attribution prose, and external source URLs from the body and MOC entry.
5. Record provenance in frontmatter `sources`. Use a non-identifying scope descriptor by default; use a path or URL only when the user explicitly approves exposing it.

Each source requires a lowercase kebab-case `id` and a `resource` accepted by OKF: an approved absolute URL, a bundle-relative path, or a scope descriptor. An optional `title` must be de-identified. Do not use reversible pseudonyms or labels such as `Customer A` when a neutral role works. Keep the same neutral role throughout the note when several statements refer to the same actor. The MOC entry describes the decision the pattern supports; it does not identify or cite the source.

## Apply OKF metadata

Use OKF v0.2 YAML frontmatter:

- `type`: always `Reusable Pattern`;
- `title`: exactly the H1 title;
- `description`: one sentence describing the supported decision;
- `tags`: domain, workflow, and visibility values without `#`;
- `status`: `draft`, `stable`, or `deprecated`;
- `sources`: de-identified provenance;
- `generated`: the producer actor and meaningful-change timestamp.

Use `status: draft` with the `draft` or `review` workflow tag. Use `status: stable` with `publish`. Reserve `deprecated` for a retained, formerly published pattern and keep the `publish` workflow tag.

`generated` describes production, not confirmation. Add `verified` only for a real verification event. Its absence explicitly means unverified. Add `stale_after` only when a source or approved policy establishes an expiry; absence means that no expiry is scheduled, not that the pattern is permanently true.

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

Use the note's exact H1 title for the MOC entry and its Pattern map node. When adding, revising, or renaming a note, update the MOC Pattern map and any populated Domain workflow in the same change. Preserve an honest `No supported domain workflow yet.` state rather than inventing a sequence.

## Create meaningful relationships

Choose a relationship type by the role the linked note plays:

- **Prerequisite** — must be understood or present first.
- **Extension** — develops this pattern further.
- **Contrast** — exposes a meaningful alternative or boundary.
- **Example** — demonstrates this pattern in a concrete case.

Explain the connection in the same list item. Do not add a link because two notes share a topic. Prefer an explicit no-relationship state over planned, dangling, or decorative links.

Use standard relative Markdown links. OKF relationships are directed links whose type and meaning come from the surrounding prose. Do not use wiki-style links or transclusions. Every target must already exist in the approved knowledge directory.

## Apply graph tags

Use frontmatter `tags` YAML list values for three independent filtering dimensions:

- domain: one or more lowercase kebab-case subject tags;
- workflow: exactly one of `draft`, `review`, or `publish`;
- visibility: exactly one of `private` or `public`.

Tags do not replace MOC membership or relationship prose. Do not add tool-specific properties, queries, transclusions, or plugins.

## Review

Before completion, confirm:

- the note contains one reusable pattern rather than a topic;
- source learning and synthesized recommendations remain distinguishable;
- customer and team identities are obfuscated with neutral roles;
- provenance is recorded in frontmatter without exposing unapproved identities or locations;
- lifecycle, production, verification, and expiry metadata are truthful;
- the causal chain works in both directions;
- the MOC is the correct navigation home;
- every relationship has the right type and a supported explanation;
- uncertainty and constraints are preserved;
- no learning, evidence, example, or causal claim was invented.
