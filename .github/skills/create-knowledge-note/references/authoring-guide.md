# Knowledge-note authoring guide

## IP inventory

| Category | Capture |
|---|---|
| Problem | Important problem, affected audience, stakes, failed defaults |
| Thesis | Central position or insight |
| Principles | Durable beliefs that guide judgment |
| Framework | Named stages, components, relationships, definitions |
| Practices | Repeatable actions and decision rules |
| Examples | Incidents, analogies, demonstrations, counterexamples |
| Evidence | Observations, results, citations, limits of support |
| Boundaries | Non-goals, risks, exceptions, misuse |
| Lineage | Related disciplines, prior art, influences |
| Language | Canonical terms, memorable phrases, deprecated alternatives |
| Transfer | Assets, habits, or capabilities the idea should create |

## Candidate concept map

Present:

| Candidate concept | What it says | Why it may matter | Relationship or lineage | Suggested disposition |
|---|---|---|---|---|

Include primary concepts, reusable secondary insights, examples, possible frameworks, tensions, unrelated substantial topics, and ideas that may synthesize established practices.

Offer:

- **No opinion — recommend a selection:** choose the strongest coherent set.
- **All of them:** retain all, then determine whether they form one or several notes.
- **None — reanalyse:** use a materially different lens, not different wording.

## Point-of-view options

Propose two to four options using:

| Dimension | Question |
|---|---|
| Central claim | What do we believe is true? |
| Tension | What common assumption does it challenge? |
| Audience | Who needs this idea? |
| Stakes | Why does it matter? |
| Distinctive contribution | What does this framing add or combine? |
| Lineage | Which disciplines does it draw from? |
| Boundaries | What does it not claim? |
| Desired change | What should the reader think or do differently? |

Multiple points of view may share a note only when they support the same thesis. Otherwise recommend separate notes.

User reframing is canonical input, not commentary to mention in the note. Capture new synthesis, terminology, lineage, and boundaries.

## Knowledge-note contract

Confirm:

- working title;
- selected concepts;
- central claim;
- audience;
- framework and terminology;
- lineage;
- examples;
- boundaries and anti-claims;
- desired change;
- excluded or parked topics;
- output path.

## Integrity checks

- Is the thesis specific?
- Does the framework solve the stated problem?
- Are recommendations supported?
- Is synthesis distinguished from established practice?
- Are lineage, limits, trade-offs, and failure conditions explicit?
- Can a downstream author reproduce the idea without the source transcript?
- Are contradictions resolved or marked?

Do not overstate novelty, causality, validation, or generality.

## Writing rules

- Use assertion-led headings and direct point-of-view prose.
- Follow abstractions with concrete examples.
- Define canonical terms.
- Tie practices to principles.
- Cite sources where available.
- Do not write a transcript summary, meeting recap, marketing brochure, or slide deck in prose.
- Do not narrate the workshop or harvesting process.
- Avoid “this paper,” “this whitepaper,” and “the workshop showed.”
- Keep metadata and provenance out of the visible argument.

## Downstream extraction map

End with:

| Field | Canonical content |
|---|---|
| Central thesis | One sentence |
| Audience problem | Who, what, and why it matters |
| Framework | Components with one-line definitions |
| Key principles | Smallest durable set |
| Practices | Actions derived from the framework |
| Example/demo | Best demonstration candidate |
| Boundaries | Risks, anti-patterns, non-goals |
| Terminology | Terms downstream assets must preserve |
| Evidence/lineage | Support and related disciplines |
| Desired transfer | What should change or become reusable |

## Invisible metadata

Use an HTML comment footer:

```markdown
<!--
Second-brain metadata

Status: Draft
Version: 0.1
Last updated: YYYY-MM-DD
Canonical: Yes
Primary source: source-file.md

Provenance notes:
- Distinguish source-derived ideas from later synthesis here.
-->
```

Use visible front matter only when explicitly requested. When revising, update the existing note, increment its version, preserve stable terminology, and identify stale downstream assets.

