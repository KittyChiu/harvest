---
name: create-domain-moc
description: Create or revise one domain Map of Content (MOC) for a file-based PKM knowledge graph. Use when defining a new knowledge domain, clarifying its boundaries, or organizing existing atomic notes with descriptive navigation links.
license: MIT
compatibility: Produces portable Markdown for file-based PKM tools. Python 3 is required for validation.
---

# Create Domain MOC

Create one domain Map of Content (MOC). A MOC defines a coherent knowledge domain, shows how its atomic patterns relate and work together, and helps readers navigate to the notes that contain the knowledge.

## Domain contract

Write one file directly in the approved existing knowledge directory:

- `<domain>-moc.md`

Use a lowercase kebab-case domain stem. Do not create folders, atomic notes, coaching notes, decks, registries, or graph databases.

A MOC contains:

- a clear domain name;
- domain, `#moc`, workflow, and visibility tags;
- a scope that explains what belongs and what does not;
- a complete pattern map of the domain's atomic notes and supported relationships;
- a domain workflow showing how the patterns can be applied together;
- descriptive links to approved existing atomic notes, or an honest empty state.

Read [references/domain-design.md](references/domain-design.md) and use [assets/domain-moc-template.md](assets/domain-moc-template.md).

## Source and write gate

Before analysis, confirm:

- the intended domain and why it needs separate navigation;
- authoritative source material, if any, and every read-only input;
- create or revise mode;
- the approved existing knowledge directory;
- the exact `<domain>-moc.md` output filename;
- every file permitted to change;
- workflow and visibility tags.

Inspect existing MOCs before proposing a new one. If the domain substantially overlaps an existing MOC, recommend reusing or revising that MOC instead of creating a duplicate.

## Interaction flow

1. Inspect approved existing MOCs and nearby atomic-note titles.
2. Read every atomic note that will appear in the MOC. Extract its title and supported `Prerequisite`, `Extension`, `Contrast`, and `Example` relationships.
3. Propose:
   - a short domain name and lowercase kebab-case filename;
   - one-sentence purpose;
   - explicit inclusion and exclusion boundaries;
   - domain, workflow, and visibility tags;
   - descriptive entries for existing notes that clearly belong;
   - one pattern map containing every domain pattern, useful clusters, and only source-supported relationships;
   - one domain workflow containing every domain pattern, including branches or alternatives when a single sequence would misrepresent the domain;
   - meaningful links to adjacent MOCs only when the relationship can be stated.
4. If no atomic notes exist yet, use the template's honest empty states rather than adding planned patterns, relationships, or workflow.
5. In revise mode, add the required map sections when upgrading a legacy MOC, preserving its established scope, tags, and note links.
6. Obtain explicit approval for the domain contract, exact output path, and permitted files.
7. Write or revise only the MOC.

## Navigation rules

- Keep broad orientation in the MOC and reusable knowledge in atomic notes.
- Treat the MOC's `Pattern map` and `Domain workflow` as the authoritative domain-level system view. A presentation may reproduce them but must not be their only home.
- Use `- [<atomic-note-title>](<atomic-stem>.md) — <why a reader would open it>` for note entries.
- Use portable relative Markdown links by default. Wiki-style links are allowed when the selected PKM tool uses them; in `Notes`, alias each wiki link with the exact atomic-note title used by the diagrams.
- Link only to files that exist in the knowledge directory.
- Explain every internal link in prose; never produce a bare related-links list.
- Introduce each Mermaid diagram with concise prose that explains what the reader should learn from it.
- Use one fenced Mermaid `flowchart` in each populated map section. The Pattern map must show every note listed under `Notes`; a populated Domain workflow must show every note using the same pattern title.
- In `Pattern map`, group patterns only when a cluster improves orientation. Show only relationships supported by the atomic notes and apply the translation rules in [references/domain-design.md](references/domain-design.md).
- In `Domain workflow`, show a practical order, branch, or choice only when supported by the patterns and their relationships. Label synthesis explicitly in prose and preserve uncertainty; do not force unrelated patterns into a false sequence.
- Use exact pattern titles rather than MOC-only IDs in Mermaid nodes. Keep node names and relationship directions consistent across both diagrams.
- Preserve stable domain naming when revising.
- Do not invent domain consensus, evidence, atomic notes, or relationships.
- Replace every instructional prompt and placeholder from the template.

## Validate

Run:

```bash
python3 "<skill-directory>/scripts/validate_moc.py" "<domain-moc.md>"
```

Resolve `<skill-directory>` from this `SKILL.md`. Fix every error, then confirm qualitatively that the domain is coherent, distinct from neighboring MOCs, narrow enough to guide whether an atomic note belongs, and represented consistently across the Notes, Pattern map, and Domain workflow.

## Completion

Complete only when one MOC is written in the approved knowledge directory, uses the required filename, defines useful boundaries, carries all tag categories, contains only descriptive and resolvable internal links, gives every atomic note one consistently named place in the Pattern map and in any populated Domain workflow, uses only supported relationships and defensible workflow synthesis, contains no template prompts or placeholders, changes only the approved file, and the validator reports zero errors.
