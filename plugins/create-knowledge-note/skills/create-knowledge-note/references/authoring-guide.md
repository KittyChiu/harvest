# Knowledge-note authoring guide

## Candidate selection

Read the approved sources and extract only ideas that can earn space in a 300-word note. Group duplicates and preserve meaningful tensions rather than smoothing them away.

Present candidates in a compact table:

| Candidate idea | Why it matters | Suggested action |
|---|---|---|
| Short label | One-sentence meaning or value | Keep, merge, park, or drop |

Include the central idea, possible guiding principles, useful practices, strongest examples, real constraints, and related ideas. Do not catalogue every topic in the source.

Let the user keep, drop, merge, park, or reframe any candidate. Then propose two to five guiding principles that are:

- short enough to remember;
- directional rather than descriptive;
- distinct from one another;
- supported by the selected source material.

## Approval summary

Before writing, confirm in one compact message:

- title;
- selected ideas;
- guiding principles;
- create or revise mode;
- approved existing destination directory, exact output filename, and files allowed to change.

Explicit approval is required before writing. If the user changes several fields, accept them together and reconfirm only what changed.

## Structure

Use 5–8 sections. Default to these six:

1. Core Idea
2. Guiding Principles
3. Practices
4. Examples
5. Constraints
6. Related Ideas

Omit a section when the source cannot support it. Add no more than two sections when they improve retrieval or preserve an essential idea. Useful additions include Questions, Terms, and Implications.

Headings must describe the content. Do not use empty sections, filler, repeated conclusions, or document-production language.

## Word limit

The complete visible Markdown note must be 300 words or fewer. Count the title, headings, prose, list items, link labels, and table text. Do not count Markdown punctuation or hidden metadata, although metadata should be omitted by default.

If the draft is too long, tighten in this order:

1. Remove repetition and process narrative.
2. Keep one strong example rather than several weak ones.
3. Merge overlapping practices or related ideas.
4. Shorten context before cutting critical constraints.
5. Preserve the Core Idea and approved guiding principles.

## Writing style

- Write like a thoughtful practitioner sharing lived understanding.
- Use plain language, short paragraphs, and compact lists.
- Minimize jargon; define any specialist term that must remain.
- Use markdown headings over bold titles.
- Use concrete examples and state practical implications directly.
- Preserve source terminology when it carries meaning.
- Briefly label interpretation, recommendation, or uncertainty when confusion is possible.
- Link sources and related notes only when supplied or verifiable.
- Do not write a transcript summary, meeting recap, marketing brochure, or slide deck in prose.
- Do not narrate the harvesting or writing process.
- Do not overstate novelty, causality, validation, or generality.

## Final checks

Before completion, resolve `scripts/validate_note.py` relative to the skill's `SKILL.md`, then run `python3 "<resolved-validator-path>" <output-path>`. Add `--allow-front-matter` only when the user explicitly requested front matter. The validator checks the 300-word limit, 5–8 non-empty level-two sections, and the default prohibition on front matter.

Then verify:

- the file was written only to the approved output path;
- the file is directly inside the approved destination directory and no directory or subfolder was created;
- no read-only source or unapproved asset changed;
- the note has 5–8 non-empty sections;
- all visible words, including title and headings, total 300 or fewer;
- the Core Idea and approved guiding principles are intact;
- practices follow from the principles;
- examples are concrete and constraints are meaningful;
- related ideas are relevant rather than decorative;
- unsupported claims, contradictions, and uncertainty are removed or marked;
- the note stands alone without the source or process history.
