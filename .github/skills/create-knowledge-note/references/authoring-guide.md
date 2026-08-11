# Knowledge-note authoring guide

## IP inventory

| Category | Capture |
|---|---|
| Problem | Important problem, affected audience, stakes, and pain points |
| Guiding Principles | Memorable directional statements that anchor the note |
| Rationale | Why the Guiding Principles matter and what follows from them |
| Practices | Best practices and emerging industry applications of the Guiding Principles |
| Examples | Incidents, analogies, demonstrations, counterexamples |
| Constraints | Limits, risks, exceptions, failure conditions, and misuse |
| Influences | Related ideas, disciplines, and prior work |
| Glossary | Canonical terms, memorable phrases, and deprecated alternatives |

## Artifact manifest

Present and confirm this before analysis:

| Field | Confirm |
|---|---|
| Sources | Files or materials to read and their authority |
| Read-only files | Existing sources and assets that must not change |
| Mode | Create or revise |
| Canonical output | Exact output path for the knowledge note |
| Write authority | Exact files permitted to change |

Source precedence controls idea authority, not write authority. Never infer an output path from the location or authority of a source.

## Candidate concept map

Present:

| Candidate concept | What it says | Why it may matter | Relationship or influences | Suggested disposition |
|---|---|---|---|---|

Include primary concepts, reusable secondary insights, examples, possible frameworks, tensions, unrelated substantial topics, and ideas that may synthesize established practices.

Dynamically list every candidate concept as a selectable option. Let the user select any combination and provide free-form instructions to keep, drop, park, merge, or reanalyse concepts. Do not use a fixed option list.

## Knowledge-note contract

Confirm:

- artifact manifest;
- working title;
- objectives;
- selected concepts;
- Guiding Principles;
- Rationale;
- audience;
- Glossary;
- influences;
- examples;
- constraints;
- excluded or parked topics.

### Approval consolidation

Let the user correct several contract fields at once. After a correction, re-present only changed fields, then ask once for final write authorization. Approval of concepts or a title alone is not permission to write.

## Integrity checks

- Are the Guiding Principles memorable and directional?
- Does the Rationale explain why they matter and what follows from them?
- Are recommendations supported?
- Is synthesis distinguished from established practice?
- Are influences, constraints, trade-offs, and failure conditions explicit?
- Can a downstream author reproduce the idea without the source material?
- Are contradictions resolved or marked?

Do not overstate novelty, causality, validation, or generality.

## Writing rules

- Write like a thoughtful practitioner sharing lived understanding.
- Keep the tone human, experiential, light, and easy to understand.
- Use plain language, short paragraphs, and concrete examples.
- Minimize jargon; define any specialist term that must remain.
- Avoid cold, detached, academic, overly objective, or dense prose.
- Keep rigor by distinguishing observation, interpretation, recommendation, and uncertainty.
- Use direct headings and a clear perspective.
- Follow abstractions with concrete examples.
- Define canonical terms in the Glossary.
- Tie practices to the Guiding Principles and Rationale.
- Cite sources where available.
- Do not write a transcript summary, meeting recap, marketing brochure, or slide deck in prose.
- Do not narrate the workshop or harvesting process.
- Avoid “this paper,” “this whitepaper,” and “the workshop showed.”
- Keep metadata and provenance out of the visible argument.

## Downstream extraction map

End with:

| Field | Canonical content |
|---|---|
| Objectives | What the note should help the reader understand, decide, or do |
| Guiding Principles | Memorable directional statements |
| Rationale | Why they matter and what follows from them |
| Audience problem | Who, what, and why it matters |
| Practices | Best practices and emerging industry applications |
| Example/demo | Best demonstration candidate |
| Constraints | Risks, exceptions, trade-offs, and failure conditions |
| Glossary | Terms and phrases downstream assets must preserve |
| Influences | Related ideas, disciplines, and prior work |

## Post-write contract audit

Before completion, verify:

- the file was written only to the approved output path;
- no read-only source or unapproved asset changed;
- objectives, Guiding Principles, Rationale, and practices match the approved contract;
- observation, interpretation, recommendation, and synthesis remain distinguishable;
- constraints are explicit;
- the Glossary is stable and defined;
- the voice is human, experiential, concise, conversational, and low-jargon;
- abstractions are grounded in concrete examples;
- the extraction map is complete and consistent with the note;
- the metadata records the current version, sources, and provenance;
- stale downstream assets are identified;
- contradictions, uncertainty, and unsupported claims of certainty are resolved or marked.

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

