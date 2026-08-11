---
name: thought-leadership-whitepaper
description: Harvest transcripts, notes, research, examples, and existing IP into a detailed canonical thought-leadership whitepaper for a second brain. Use to capture insights, best practices, frameworks, terminology, evidence, examples, boundaries, and reusable intellectual property. The whitepaper is the source of truth for downstream Marp presentations and facilitator guides, but this skill also works independently.
compatibility: >
  Produces a self-contained Markdown whitepaper. No external tools are required.
---

# Thought Leadership Whitepaper

Create the canonical, detailed expression of the user's intellectual property. Preserve what was learned, show how the ideas fit together, and make later presentations or workshops traceable to one source of truth.

## Role in the three-asset system

| Asset | Primary job | Content emphasis |
|---|---|---|
| Whitepaper | Capture and govern the IP | Detailed why, what, how, evidence, boundaries, lineage |
| Marp deck | Present the thought leadership | Why, what, one example or demonstration |
| Facilitator guide | Teach people to apply it | What and how, exercises, reflection, assessment |

This skill can run alone. When used with the other skills, create or update the whitepaper first.

## Required input

The caller must provide:

1. **Source material**: transcript, notes, research, existing documents, pasted content, or readable file paths.
2. **Whitepaper brief**: topic, intended audience, purpose, and desired output path.

Useful optional inputs:

- working thesis;
- named framework or terminology;
- required examples;
- known influences or related disciplines;
- claims that require caution or evidence;
- desired length and tone;
- publication status: private second-brain note, internal paper, or external article.

If the topic or source material is missing, ask one focused question. Do not invent the user's IP.

## Source-of-truth rules

- Treat this document as canonical only after resolving contradictions in the supplied material.
- Preserve exact framework names and definitions.
- Separate observed evidence, participant opinion, interpretation, recommendation, and hypothesis.
- Do not claim originality merely because a phrase emerged in a workshop.
- Identify intellectual lineage and adjacent practices when known.
- Use exact quotations only when the source supports the wording.
- Mark unresolved questions instead of creating false certainty.
- Prefer a complete treatment over presentation-friendly brevity.

## Workflow

### 1. Harvest the source material

Read all supplied sources before drafting. Build a private IP inventory:

| Category | Capture |
|---|---|
| Problem | The important problem, affected audience, stakes, failed defaults |
| Thesis | The central position or insight |
| Principles | Durable beliefs that guide judgment |
| Framework | Named stages, components, relationships, and definitions |
| Practices | Repeatable actions and decision rules |
| Examples | Incidents, analogies, demonstrations, scenarios, counterexamples |
| Evidence | Observations, results, citations, and limits of support |
| Boundaries | Non-goals, risks, exceptions, and misuse |
| Lineage | Related disciplines, prior art, and influences |
| Language | Canonical terms, memorable phrases, and deprecated alternatives |
| Transfer | Assets, habits, or capabilities the idea should create |

Consolidate duplicates without losing meaningful nuance.

### 2. Establish the canonical model

Before prose, define:

- one-sentence thesis;
- audience and problem;
- canonical vocabulary;
- framework components and relationships;
- practices derived from the framework;
- strongest supporting examples;
- boundaries and anti-patterns;
- what is established, inferred, recommended, or still uncertain.

When sources conflict, resolve the issue from explicit user decisions or ask for clarification if it materially changes the IP.

### 3. Test the intellectual integrity

Challenge the emerging paper:

- Is the thesis meaningfully specific?
- Does the framework solve the stated problem?
- Are recommendations supported by reasoning or evidence?
- Is new synthesis distinguished from established practice?
- Are related disciplines acknowledged?
- Are limits, trade-offs, and failure conditions explicit?
- Could a downstream author reproduce the idea without the transcript?

Do not overstate novelty, causality, validation, or generality.

### 4. Write the whitepaper

Start from [assets/whitepaper-template.md](assets/whitepaper-template.md) and adapt the structure to the material.

Prefer:

- assertion-led headings;
- concrete examples after abstract ideas;
- tables only when relationships become clearer;
- explicit definitions for canonical terms;
- practical guidance tied back to principles;
- sufficient detail for later reuse;
- links or citations where sources are available.

Do not write a transcript summary, meeting recap, marketing brochure, or slide deck in prose.

### 5. Add the downstream extraction map

End with a concise section named `Downstream extraction map`. It is the stable handoff to the Marp and facilitator-guide skills.

Include:

| Field | Canonical content |
|---|---|
| Central thesis | One sentence |
| Audience problem | Who, what, and why it matters |
| Framework | Components with one-line definitions |
| Key principles | The smallest durable set |
| Practices | Actions derived from the framework |
| Example/demo | Best demonstration candidate |
| Boundaries | Risks, anti-patterns, and non-goals |
| Terminology | Terms downstream assets must preserve |
| Evidence/lineage | Support and related disciplines |
| Desired transfer | What should change or become reusable |

This map summarizes; it does not replace the detailed paper.

### 6. Maintain canonical metadata

Use front matter:

```yaml
---
title: Whitepaper title
status: draft
version: 0.1
last_updated: YYYY-MM-DD
canonical: true
audience:
  - Primary audience
source_material:
  - source-file.md
---
```

When revising an existing whitepaper:

- update rather than duplicate it;
- increment the version meaningfully;
- preserve stable terminology unless the change is intentional;
- identify downstream assets that may now be stale.

## Suggested structure

1. Executive abstract
2. The problem and why it matters
3. Observations and context
4. Central thesis
5. Canonical framework or model
6. Principles
7. Practices and implementation
8. Examples or case studies
9. Risks, boundaries, and anti-patterns
10. Evidence, lineage, and open questions
11. Implications and recommended actions
12. Conclusion
13. Downstream extraction map

Use only the sections the material warrants, while retaining enough detail to govern downstream assets.

## Quality bar

The whitepaper is complete only when:

- it captures the valuable IP from all supplied sources;
- a reader can understand and apply the thesis without the original transcript;
- claims, evidence, interpretation, and recommendations are distinguishable;
- terminology and framework definitions are internally consistent;
- related practices and limitations are acknowledged;
- downstream creators can extract presentation and coaching material without redefining the IP.

## Invocation examples

> Use the thought-leadership-whitepaper skill. Sources: `workshop-transcript.md` and `research-notes.md`. Capture the complete IP about context-window optimization for engineering leaders. Treat RESET as a synthesis of established practices, preserve the workshop examples, and save the canonical paper as `Managing AI Context.md`.

> Turn these notes into a private second-brain whitepaper. Audience: me and future collaborators. Capture the thesis, framework, practices, lineage, unresolved questions, and downstream extraction map.

