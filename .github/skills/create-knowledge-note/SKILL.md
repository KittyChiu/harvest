---
name: create-knowledge-note
description: Interactively harvest transcripts, notes, research, examples, and existing IP into a canonical knowledge note for a second brain. First analyze candidate concepts, let the user select what belongs, and refine the Guiding Principles before writing. The approved note becomes the source of truth for downstream Marp decks and facilitator guides.
compatibility: Produces self-contained Markdown. No external tools are required.
---

# Create Knowledge Note

Capture detailed thought-leadership IP: why, what, how, constraints, influences, examples, practices, and glossary terms.

## Input and source rules

Require source material. A brief may be supplied or developed interactively.

Treat sources in this order: existing canonical note, approved IP, transcript/notes, then clearly identified synthesis. Source precedence determines which ideas carry authority; it never grants permission to modify a source. Only the approved artifact manifest grants write authority.

Preserve exact terminology; separate evidence, opinion, interpretation, recommendation, and hypothesis; acknowledge influences; never fabricate quotes or certainty.

Read [references/authoring-guide.md](references/authoring-guide.md) for the deterministic analysis, option matrices, contract fields, writing rules, extraction map, and metadata format.

## Artifact-routing gate

**Before analysis, present and confirm an artifact manifest.** Include:

- source files and their authority;
- files that remain read-only;
- create or revise mode;
- canonical note output path;
- exact files permitted to change.

Never infer that an existing source is the output target. Do not treat source precedence as write permission.

## Mandatory interaction gate

**Do not draft or modify the note immediately after reading the source.**

1. Read all sources and build the IP inventory.
2. Present the candidate concept map.
3. Dynamically list every candidate concept for selection. Allow any combination, plus free-form instructions to keep, drop, park, merge, or reanalyse concepts.
4. Refine one focused question at a time.
5. Present the knowledge-note contract.
6. Obtain explicit approval. Approval of concepts alone is not approval to write.

Let the user correct multiple contract fields in one response. After a correction, show only the changed fields and ask once for final write authorization; do not repeat approvals for unchanged decisions.

## Authoring

After approval:

1. Establish the canonical objectives, Guiding Principles, Rationale, practices, examples, constraints, influences, and Glossary.
2. Run the integrity checks in the authoring guide.
3. Write from [assets/knowledge-note-template.md](assets/knowledge-note-template.md).
4. Write ideas directly for a private knowledge base—never as a workshop report or document-production narrative. Use a human, experiential, light, concise voice with plain language, short paragraphs, and concrete examples.
5. Add the downstream extraction map and invisible metadata footer.
6. Run the post-write contract audit in the authoring guide before presenting the note as complete.

When revising, update rather than duplicate the note, increment its version, preserve stable terminology, and identify stale downstream assets.

## Optional downstream assets

After the canonical note passes its post-write audit, ask whether the user wants a facilitator guide, a Marp deck, both, or neither.

Delegate only after explicit consent:

- use `create-facilitator-guide` for a facilitator guide;
- use `create-obsidian-marp` for a Marp deck;
- preserve each specialist skill's interaction and approval gates.

Do not create or update downstream assets silently or automatically.

## Completion

The task is complete only when the user has approved the concepts and Guiding Principles, the note is understandable without the source material, observation and synthesis are distinguishable, the Glossary is consistent, constraints are explicit, the post-write contract audit passes, and downstream assets can reuse the IP without redefining it.

