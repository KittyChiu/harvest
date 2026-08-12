---
name: create-knowledge-note
description: "Create or revise a concise second-brain knowledge note from transcripts, notes, research, or existing IP. Use when: harvesting ideas into a self-contained Markdown note of 300 words or fewer with 5–8 clear sections, including Core Idea, Guiding Principles, Practices, Examples, Constraints, and Related Ideas."
compatibility: Produces self-contained Markdown of 300 words or fewer. No external tools are required.
---

# Create Knowledge Note

Turn source material into a compact, reusable second-brain note. Preserve the idea's meaning while removing meeting narrative, repetition, and production commentary.

## Source and output gate

Before analysis, confirm:

- the source material and its authority;
- whether to create or revise;
- the exact output path;
- which files may change.

Treat source files as read-only unless the user explicitly approves one as the output. Prefer an existing canonical note over approved IP, then transcript or notes, then clearly identified synthesis. Preserve distinctive terminology and never invent quotes, evidence, or certainty.

Read [references/authoring-guide.md](references/authoring-guide.md) for selection, writing, and validation rules.

## Interaction flow

Do not write or modify the note immediately after reading the source.

1. Extract the strongest candidate ideas and group duplicates.
2. Present a concise candidate list with a one-line explanation for each idea.
3. Ask the user what to keep, drop, merge, or reframe. Accept a multi-part answer.
4. Propose two to five short, directional guiding principles.
5. Confirm the selected ideas, guiding principles, title, and output path in one approval request.
6. Write only after explicit approval.

Ask one focused question at a time only when ambiguity would materially change the note. Do not require repeated approval for unchanged decisions.

## Note contract

Use [assets/knowledge-note-template.md](assets/knowledge-note-template.md) as the default structure.

- The complete visible note, including title and headings, must contain **300 words or fewer**.
- Use **5–8 sections** with descriptive Markdown headings.
- Default to: **Core Idea, Guiding Principles, Practices, Examples, Constraints, Related Ideas**.
- Omit a default section only when the source has no useful content for it; never add filler.
- Add at most two sections only when they materially improve retrieval, such as **Questions**, **Terms**, or **Implications**.
- Keep each section focused: a short paragraph or a compact list.
- Make the note understandable without reopening the source.
- Distinguish source claims from synthesis with brief wording when the difference matters.
- Cite or link sources only when supplied or verifiable.

Do not add an extraction map, conclusion, objectives section, glossary, front matter, or metadata unless the user requests it and the result still fits the word limit.

## Write and validate

After approval:

1. Draft the note in a human, direct, low-jargon voice.
2. Count all visible words, including the title and headings.
3. Tighten the note until it is at most 300 words without losing the Core Idea, Principles, or critical Constraints.
4. Run the checks in the authoring guide.
5. Write only to the approved output path.

When revising, update the existing note rather than duplicating it. Preserve stable terminology and mention any downstream asset that may now be stale.

## Optional downstream assets

After the note passes validation, ask whether the user wants a facilitator guide, a Marp deck, both, or neither.

When the invocation context identifies this as a delegated upstream step and names a workflow to resume, return to that workflow after the note is approved and complete. Do not ask the downstream-assets question again; the requested continuation is already known. Otherwise, use the optional downstream-assets flow below.

Delegate only after explicit consent:

- discover the available specialist skill whose description matches each selected asset type;
- invoke that specialist with the approved knowledge note and the user's requested continuation;
- preserve the specialist's interaction and approval gates;
- if no matching specialist is available, report that limitation instead of generating the asset within this skill.

Do not create or update downstream assets silently or automatically.

## Completion

The task is complete when the approved note has 5–8 useful sections, contains no more than 300 visible words, stands on its own, preserves the selected ideas and guiding principles, states meaningful constraints, and changes only approved files.

