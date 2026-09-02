# Domain presentation design

## Build one system narrative

The MOC defines the boundary. Its scope orients the audience; each Notes entry supplies one reusable pattern. The presentation should reveal how those patterns form a useful system rather than concatenate mini-decks.

Move through:

1. **Orient** — promise a domain-level outcome.
2. **Frame** — name recurring challenges and opportunities.
3. **Map** — cluster the patterns and show only supported connections.
4. **Teach** — give each pattern one memorable slide.
5. **Choose** — compare patterns only when they are alternatives.
6. **Apply** — combine patterns in one realistic scenario.
7. **Synthesize** — show directional change and remaining constraints.
8. **Revisit** — use the map to explain the system.
9. **Try** — invite one small practice against one visible signal.

## Assign stable pattern identities

Give each atomic source a contiguous internal identifier (`P1` through `PN`), a short name, and a cluster. In update mode, preserve an existing pattern's ID unless removing a source creates a gap; then minimally renumber the following patterns to restore contiguity. Use identifiers only in H6 position metadata and source matching; use short names in titles, Mermaid nodes, comparisons, scenarios, tables, and prose.

One pattern slide contains:

- its `p<n> of <N>` H6 position and cluster;
- an assertion-led H1 short name;
- one to three visible `Use when` signals;
- one to three visible `Do` practices;
- a speaker-note Pattern description;
- one speaker-note Coach cue question;
- an optional supported speaker-note relationship;
- one atomic source link and, when available, its companion link under speaker-note `Source:`.

Do not merge multiple atomic sources onto one pattern slide.

## Map relationships faithfully

Atomic-note relationships are typed and directed. For a relationship declared by source note `S` that links target note `T`, use only these translations:

| Atomic type | Permitted deck claim |
| --- | --- |
| `Prerequisite` | `S depends on T` or `T precedes S` |
| `Extension` | `S enables T`, `S informs T`, or `S complements T` |
| `Contrast` | `S contrasts with T` |
| `Example` | No pattern-to-pattern edge; use the example in the scenario |

Do not reverse `Extension` or `Contrast` claims unless the other note declares its own relationship. Omit unsupported edges instead of completing a visually balanced graph.

On a pattern slide, put `Related:` in the speaker notes followed by `<target short name> (<relationship>)`. On system slides, use `<source short name> <relationship> <target short name>`. These names map through pattern-slide sources to the typed atomic relationships.

Omit `Related:` when no source-supported relationship exists. Do not use an empty field or a prose placeholder.

Use fenced Mermaid for pattern maps and scenario flows. Mermaid nodes show exact pattern short names, never internal identifiers. If the target setup cannot render Mermaid, stop rather than substituting a text map.

## Apply without overstating

Choose one realistic situation whose signals make several patterns relevant. Sequence practices using supported relationships and keep at least one critical constraint visible.

The before/after synthesis describes an expected direction, not a measured result. Label presentation synthesis clearly when the source notes do not state it directly. The closing experiment should pair:

- one observable signal;
- one pattern;
- one small practice;
- one way to review what happened.

## Use coaching companions

Every pattern slide has one open `Coach cue:` question in its speaker notes. When a companion exists, use its Conversation section to select the question and link the companion under `Source:`:

```markdown
<!--
Pattern description:
When teams repeat setup decisions, provide a maintained path, because it removes avoidable choices.

Coach cue: Where does repeated setup work consume the most attention?

Source:
[Golden paths](platform-golden-paths.md)
[Golden-path coaching](platform-golden-paths.coach.md)
-->
```

Do not turn Progress signals into targets or copy the companion into visible slide content.

## Update without fragmentation

When the MOC changes:

1. compare atomic sources with pattern-slide `Source:` fields;
2. preserve IDs for retained patterns;
3. add or remove pattern slides;
4. make internal IDs contiguous without adding them to visible titles or diagrams;
5. revise clusters, maps, scenario, synthesis, and close;
6. remove coach links for missing companions and add newly available ones;
7. preserve confirmed configuration and useful unaffected content.

## Review

Confirm:

- the domain promise and closing experiment resolve the same need;
- challenges, opportunities, and domain question frame the pattern system;
- each MOC note has exactly one pattern slide;
- IDs, names, clusters, maps, comparisons, and scenarios agree;
- patterns and practices remain distinct;
- every relationship and directional change is supported or identified as synthesis;
- coaching cues are open questions;
- no source or coach remains after leaving the MOC.
