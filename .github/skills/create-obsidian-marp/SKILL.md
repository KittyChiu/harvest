---
name: create-obsidian-marp
description: Turn a canonical knowledge note, existing thought-leadership IP, or transcript into a narrative Marp deck with speaker notes for the Obsidian Marp Slides plugin. Interactively select an explained storytelling approach and confirm Marp configuration. Build one coherent narrative spine rather than fragmented anecdotes.
compatibility: Produces Obsidian-compatible Marp Markdown. Python 3 is used only by the bundled validator.
---

# Create Obsidian Marp

Present **why**, **what**, and one example or demonstration of **how**. Leave comprehensive instruction to the facilitator guide and detailed IP to the knowledge note.

## Input and source rules

Require an IP source and deck brief. The brief defines audience, objective, required messages, duration/slide count, tone, optional story/demo, and output path.

Use source precedence: canonical knowledge note, approved IP, transcript/notes, then clearly identified synthesis. Preserve canonical terminology, claims, framework, boundaries, and provenance.

Read these references when their phase begins:

- [references/storytelling-guide.md](references/storytelling-guide.md) — approach options, explanations, spine, and coherence.
- [references/configuration-guide.md](references/configuration-guide.md) — defaults, available values, discovery, and trade-offs.
- [references/authoring-checklist.md](references/authoring-checklist.md) — extraction, slides, notes, and validation.
- [references/obsidian-marp-compatibility.md](references/obsidian-marp-compatibility.md) — supported syntax and portability.

## Workflow

1. Read all source material and extract the presentation evidence.
2. Define one presentation promise; exclude material that does not support it.
3. Present two to four viable storytelling approaches. For each explain its plain-language meaning, proposed throughline, audience experience, source use, strengths, trade-offs, and 4–6 beat flow.
4. Recommend one and ask the user to select, blend with one primary approach, delegate, or request different options.
5. **Do not design slides until the storytelling decision is made.**
6. Inspect the target vault when available. Present Marp defaults, available built-ins, detected local themes/plugins, meanings, and portability trade-offs.
7. Ask whether to use defaults or customize. Defaults are `theme: default`, standard theme styling, `16:9`, pagination on, no header/footer, local or approved images, and no optional plugins.
8. **Do not design slides until configuration is confirmed or delegated.**
9. Build slide architecture around one narrative spine, then author visible content and connected speaker notes from [assets/deck-template.md](assets/deck-template.md).
10. Apply the compatibility reference and run the bundled validator.

## Non-negotiables

- One primary idea and story beat per slide.
- Every substantive slide has speaker notes.
- Supporting examples reinforce the same throughline.
- No arbitrary HTML layout, remote fonts, JavaScript, or unconfirmed plugins.
- No custom CSS by default.
- Direct quotes require exact support.
- The close resolves the opening tension.

## Completion

The task is complete only when the brief, selected storytelling approach, and confirmed Marp configuration are honored; the narrative is coherent; source and synthesis are distinct; the deck is portable; and a presenter can deliver it without reconstructing missing context.

