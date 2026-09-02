---
name: create-domain-moc
description: Create or revise one domain Map of Content (MOC) for a file-based PKM knowledge graph. Use when defining a new knowledge domain, clarifying its boundaries, or organizing existing atomic notes with descriptive navigation links.
license: MIT
compatibility: Produces portable Markdown for file-based PKM tools. Python 3 is required for validation.
---

# Create Domain MOC

Create one domain Map of Content (MOC). A MOC defines a coherent knowledge domain and helps readers navigate its atomic notes; it does not contain the knowledge itself.

## Domain contract

Write one file directly in the approved existing knowledge directory:

- `<domain>-moc.md`

Use a lowercase kebab-case domain stem. Do not create folders, atomic notes, coaching notes, decks, registries, or graph databases.

A MOC contains:

- a clear domain name;
- domain, `#moc`, workflow, and visibility tags;
- a scope that explains what belongs and what does not;
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
2. Propose:
   - a short domain name and lowercase kebab-case filename;
   - one-sentence purpose;
   - explicit inclusion and exclusion boundaries;
   - domain, workflow, and visibility tags;
   - descriptive entries for existing notes that clearly belong;
   - meaningful links to adjacent MOCs only when the relationship can be stated.
3. If no atomic notes exist yet, use `No atomic notes yet.` rather than adding planned or decorative links.
4. Obtain explicit approval for the domain contract, exact output path, and permitted files.
5. Write or revise only the MOC.

## Navigation rules

- Keep broad orientation in the MOC and reusable knowledge in atomic notes.
- Use `- [<atomic-note-title>](<atomic-stem>.md) — <why a reader would open it>` for note entries.
- Use portable relative Markdown links by default. Wiki-style links are allowed when the selected PKM tool uses them.
- Link only to files that exist in the knowledge directory.
- Explain every internal link in prose; never produce a bare related-links list.
- Preserve stable domain naming when revising.
- Do not invent domain consensus, evidence, atomic notes, or relationships.

## Validate

Run:

```bash
python3 "<skill-directory>/scripts/validate_moc.py" "<domain-moc.md>"
```

Resolve `<skill-directory>` from this `SKILL.md`. Fix every error, then confirm qualitatively that the domain is coherent, distinct from neighboring MOCs, and narrow enough to guide whether an atomic note belongs.

## Completion

Complete only when one MOC is written in the approved knowledge directory, uses the required filename, defines useful boundaries, carries all tag categories, contains only descriptive and resolvable internal links, changes only the approved file, and the validator reports zero errors.
