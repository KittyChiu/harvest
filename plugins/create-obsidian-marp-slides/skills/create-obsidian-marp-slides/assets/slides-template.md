---
marp: true
theme: default
paginate: true
size: 16:9
title: Domain presentation
description: Present a domain as a connected system of reusable patterns and practices
---

<!-- markdownlint-disable MD001 MD024 MD025 -->

<!--
Use the domain MOC, atomic pattern notes, and coaching companions.

Rules:
- Assign each pattern a stable identifier: P1, P2, P3, and so on.
- Give each pattern a short, memorable name.
- Present one pattern per slide.
- State each pattern as: "When X, do Y, because Z."
- Separate the pattern from its practices.
- Only show relationships supported by the source notes.
- Label relationships: enables, precedes, informs, complements, contrasts with,
  or depends on.
- Put coaching questions in presenter comments.
- Replace the text maps with Mermaid only when rendering support is confirmed.
-->

# [Domain name]

## [One-line domain promise]

[Describe the outcome this domain helps people achieve.]

MOC: [Domain name](domain-moc.md)
Tags: #domain #slides #draft #private

---

# Challenges & opportunities

## Challenges

- [Recurring challenge]
- [Practical consequence]
- [Limitation of the current approach]

## Opportunities

- [Potential improvement]
- [Capability the domain can enable]
- [Value of connecting the patterns]

> **Domain question:** [What do the patterns collectively help answer?]

---

# Pattern map

```text
[Domain name]
├── [Cluster 1]
│   ├── P1 · [Pattern name]
│   └── P2 · [Pattern name]
├── [Cluster 2]
│   └── P3 · [Pattern name]
└── [Cluster 3]
    └── P4 · [Pattern name]

P1 · [Pattern name] --[relationship]--> P3 · [Pattern name]
P2 · [Pattern name] --[relationship]--> P3 · [Pattern name]
P3 · [Pattern name] --[relationship]--> P4 · [Pattern name]
```

---

<!-- Repeat one slide for each pattern. -->

###### PATTERN P1 OF [N] · [CLUSTER]

# P1 · [Short pattern name]

> **When [condition], [action], because [mechanism].**

## Use it when

- [Observable signal]
- [Recurring situation]

## Practices

1. [Concrete action]
2. [Concrete action]
3. [Optional concrete action]

**Related:** [P2 · Pattern name] through **[relationship]**

Source: [Atomic pattern](domain-atomic-note.md)
Coach: [Coaching companion](domain-atomic-note.coach.md)

<!--
Coach cue: [One question that helps the audience discover or apply the pattern.]
-->

---

###### PATTERN P2 OF [N] · [CLUSTER]

# P2 · [Short pattern name]

> **When [condition], [action], because [mechanism].**

## Use it when

- [Observable signal]
- [Recurring situation]

## Practices

1. [Concrete action]
2. [Concrete action]
3. [Optional concrete action]

**Related:** [P1 · Pattern name] through **[relationship]**

Source: [Atomic pattern](domain-atomic-note.md)
Coach: [Coaching companion](domain-atomic-note.coach.md)

<!--
Coach cue: [One question that helps the audience discover or apply the pattern.]
-->

---

<!-- Optional: use when two patterns are alternatives. -->

# Choosing between P1 and P2

| Situation   | Use                     |
| ----------- | ----------------------- |
| [Condition] | **P1 · [Pattern name]** |
| [Condition] | **P2 · [Pattern name]** |

> **Selection rule:** When [condition], prefer [pattern], because [reason].

---

# Apply the patterns together

## Scenario: [Realistic situation]

```text
[Observed signal]
       ↓
P1 · [Pattern name]
       ↓ [relationship]
P3 · [Pattern name]
       ↓ [relationship]
P4 · [Pattern name]
       ↓
[Expected outcome]
```

- **Start with:** [First practice]
- **Then:** [Next practice]
- **Watch for:** [Constraint or failure condition]

---

# What changes

| Before              | Pattern | After                |
| ------------------- | ------- | -------------------- |
| [Current behaviour] | **P1**  | [Improved behaviour] |
| [Current behaviour] | **P3**  | [Improved behaviour] |
| [Current behaviour] | **P4**  | [Improved behaviour] |

> **Remaining constraint:** [What these patterns do not solve.]

---

# Pattern map revisited

```text
[Domain name]
├── P1 · [Pattern name]
├── P2 · [Pattern name]
├── P3 · [Pattern name]
└── P4 · [Pattern name]

P1 · [Pattern name] --[relationship]--> P3 · [Pattern name]
P3 · [Pattern name] --[relationship]--> P4 · [Pattern name]
```

> **Domain takeaway:** [Explain how the patterns work as a system.]

---

# Choose one pattern to try

- **Signal:** [Something observable]
- **Pattern:** P[ ] · [Pattern name]
- **Practice:** [One small action]
- **Review:** [How the result will be discussed]

> Start with the pattern that addresses the clearest signal.
