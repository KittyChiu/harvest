---
name: create-obsidian-marp
description: Turn a canonical knowledge note, existing thought-leadership IP, raw notes, or a transcript into a narrative Marp deck with speaker notes for the Obsidian Marp Slides plugin. Recommend creating a knowledge note when none exists, while allowing direct use of approved raw sources. Interactively select a storytelling approach and confirm Marp configuration.
license: MIT
compatibility: Produces Obsidian-compatible Marp Markdown. Python 3 is used only by the bundled validator.
---

# Create Obsidian Marp

Present **why**, **what**, and one example or demonstration of **how**. Leave hands-on practice and reflection to a learning module, but preserve every approved source message classified as visible in the confirmed coverage contract.

## Input and source rules

Require an IP source and deck brief. Before analysis, confirm the source files and their authority, files that remain read-only, create or revise mode, the approved existing destination directory, the exact output filename ending in `.marp.md`, and the exact files permitted to change. If the proposed filename uses another extension, propose the corrected `.marp.md` filename and confirm it before writing. The brief defines audience, objective, required messages, duration/slide count, tone, and optional story/demo.

Reuse the destination directory supplied in the invocation or continuation context. If none is supplied, ask the user to identify an existing directory. Write the deck directly into that directory. Do not infer the directory name, create a directory or subfolder, or group the output by artifact type. When delegating knowledge-note creation, pass the same destination directory in the continuation context.

Check whether the user supplied or identified an approved knowledge note. Use user-provided paths and project conventions discovered from local documentation; do not assume a storage directory. Confirm authority before using a discovered file; a matching filename alone does not make it authoritative. If no approved note is available, ask which path to use:

- **Create a knowledge note first (recommended)** — discover an available specialist skill whose description matches creating a concise knowledge note, invoke it with the approved raw sources and continuation context, preserve its approval gates, and resume this workflow only after the note is approved and complete.
- **Continue from raw sources** — keep the skill atomic and do not create a knowledge note. Extract and confirm a task-local content contract from the approved IP, notes, or transcript before presentation design.
- **Choose an existing knowledge note** — let the user identify another note.

Do not invoke another skill automatically. The recommendation is a user choice, not a prerequisite. If no matching specialist is available, offer raw-source mode rather than implementing knowledge-note creation inside this skill.

Use source precedence: approved knowledge note, approved IP, transcript/notes, then clearly identified synthesis. Discover the source's actual structure without assuming section names, order, or heading level. Extract only candidate claims, principles, practices, examples, and boundaries that may belong in the deck; do not classify every source paragraph as required content. Assign stable descriptive IDs and confirm the task-local content contract with the user. Preserve approved terminology, claims, and constraints. Treat audience framing, the narrative spine, and any inferred model as presentation design unless the source states them explicitly.

Begin with every item in the approved source contract **unclassified**. Propose one disposition for each: visible, notes-only, optional, or excluded. The brief and user-approved coverage contract determine the disposition; never infer it from a heading name. Allow the user to classify a whole source group or override individual items. Speaker notes may deepen visible content but never substitute for it.

Do not expect the knowledge note to contain separate objectives, rationale, glossary, metadata, provenance, or an extraction map. Do not reopen its original sources merely to reconstruct omitted detail unless the user approves those sources for this task.

Read these references when their phase begins:

- [references/storytelling-guide.md](references/storytelling-guide.md) — approach options, explanations, spine, and coherence.
- [references/configuration-guide.md](references/configuration-guide.md) — defaults, available values, discovery, and trade-offs.
- [references/authoring-checklist.md](references/authoring-checklist.md) — extraction, slides, notes, and validation.
- [references/obsidian-marp-compatibility.md](references/obsidian-marp-compatibility.md) — supported syntax and portability.

## Workflow

1. Resolve the source path: use the supplied knowledge note, delegate note creation only with user approval, or confirm atomic raw-source mode. Read the approved source material and extract the presentation evidence.
2. Build a source coverage contract listing every discovered section and item, the proposed disposition, and the reason. Let the user change dispositions at section or item level, then confirm the contract before storytelling selection.
3. Define one presentation objective. Use the confirmed visible content as the required message set; retain notes-only content in notes and omit content confirmed as optional or excluded.
4. Present two to four viable storytelling approaches. For each explain its plain-language meaning, proposed throughline, audience experience, source use, strengths, trade-offs, 4–6 beat flow, and how every item classified as visible remains visible.
5. Recommend one and ask the user to select, blend with one primary approach, delegate, or request different options.
6. **Do not design slides until the coverage contract and storytelling decision are confirmed.**
7. Inspect the target vault when available. Present Marp defaults, available built-ins, detected local themes/plugins, meanings, and portability trade-offs.
8. Ask whether to use defaults or customize. Defaults are `theme: default`, standard theme styling, `16:9`, pagination on, no header/footer, local or approved images, and no optional plugins.
9. **Do not design slides until configuration is confirmed or delegated.**
10. Build slide architecture around one narrative spine. Create a source-to-slide map showing the destination for every visible and notes-only item, then author visible content and connected speaker notes from [assets/deck-template.md](assets/deck-template.md). The narrative connects the confirmed visible content; it does not replace or suppress it.
11. Embed the complete approved item list in a `source-contract` marker and record every confirmed disposition with the markers defined in [references/authoring-checklist.md](references/authoring-checklist.md), regardless of source type.
12. Apply the compatibility reference, perform a reverse coverage review against the approved source contract, and run the bundled validator against the self-contained deck.

## Non-negotiables

- One primary idea and story beat per slide.
- The output filename ends in `.marp.md`.
- The deck is directly inside the approved destination directory; no directory or subfolder is created.
- Every approved source item has exactly one confirmed disposition.
- Every item classified as visible appears in visible slide content.
- Every slide includes an HTML-comment speaker-note block; the block may be empty.
- Speaker-note comments are an explicit exception to the prohibition on arbitrary HTML.
- Supporting examples reinforce the same throughline.
- No arbitrary HTML layout, remote fonts, JavaScript, or unconfirmed plugins.
- No custom CSS by default.
- Direct quotes require exact support.
- The close resolves the opening tension.

## Completion

The task is complete only when the deck is written directly in the approved destination directory without creating a directory or subfolder; the source-to-slide map has been checked against the final deck; every approved source item has exactly one confirmed disposition; every visible and notes-only item is faithfully conveyed in its destination; every optional or excluded item has an approved reason; the bundled validator exits with code `0` and reports zero errors; the brief, selected storytelling approach, and confirmed Marp configuration are honored; the narrative is coherent; source and synthesis are distinct; the deck is portable; and a presenter can deliver it without reconstructing missing context.
