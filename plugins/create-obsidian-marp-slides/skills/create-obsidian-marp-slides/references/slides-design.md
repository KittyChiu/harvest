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

Give each atomic source a contiguous identifier (`P1` through `PN`), a short name, and a cluster. In update mode, preserve an existing pattern's ID unless the user approves a renumbering. Remove gaps after sources leave the MOC and update every map, comparison, scenario, and table consistently.

One pattern slide contains:

- its `Pn of N` position and cluster;
- an assertion-led short name;
- the atomic note's one-sentence Pattern;
- observable Signals;
- one to three concrete Practices;
- one source link;
- an optional supported relationship;
- when a companion exists, one coach link and one question in a speaker-note comment.

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

On a pattern slide, use `**Related:** P<n> · <name> through **<relationship>**`. Keep the `P<n>` target outside Markdown-link brackets so the relationship remains unambiguous and machine-checkable.

Use Mermaid only when the user confirms that the target Marp setup renders it. Otherwise use a fenced `text` map with the same IDs and labels. The map is communication, not a new graph database.

## Apply without overstating

Choose one realistic situation whose signals make several patterns relevant. Sequence practices using supported relationships and keep at least one critical constraint visible.

The before/after synthesis describes an expected direction, not a measured result. Label presentation synthesis clearly when the source notes do not state it directly. The closing experiment should pair:

- one observable signal;
- one pattern;
- one small practice;
- one way to review what happened.

## Use coaching companions

Use a companion's Conversation section to select one open question for its pattern slide. Put the companion in `Coach:` and the question in an HTML comment:

```markdown
Coach: [Golden-path coaching](platform-golden-paths.coach.md)

<!--
Coach cue: Where does repeated setup work consume the most attention?
-->
```

Do not turn Progress signals into targets or copy the companion into visible slide content.

## Update without fragmentation

When the MOC changes:

1. compare atomic sources with pattern slides;
2. preserve IDs for retained patterns;
3. add or remove pattern slides;
4. make IDs contiguous and update every cross-reference;
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
