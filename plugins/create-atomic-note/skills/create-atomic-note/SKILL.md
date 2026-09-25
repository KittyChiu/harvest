---
name: create-atomic-note
description: Create or revise one OKF-compatible reusable knowledge pattern in a file-based PKM graph. Use when source material contains a repeatable rule that should be grounded in learning, connected to one domain MOC, and expressed with practical signals, actions, constraints, provenance, lifecycle, trust, freshness, and relationships.
license: MIT
compatibility: Produces Open Knowledge Format v0.2 Markdown for file-based PKM tools. Python 3.10 or later is required for validation.
---

# Create Atomic Note

Create or revise one self-contained, reusable pattern as an Open Knowledge Format (OKF) v0.2 concept and make it navigable from exactly one domain Map of Content (MOC).

## Artifact contract

Write the note and update its MOC directly in the approved existing knowledge directory:

- source MOC: `<domain>-moc.md`
- atomic note: `<domain>-<pattern-slug>.md`

Use lowercase kebab-case filenames. The MOC must already exist and remain the note's only parent. Do not create folders, MOCs, coaching notes, presentations, indexes, registries, or graph databases.

Use [assets/atomic-note-template.md](assets/atomic-note-template.md) as the artifact schema. Read [references/graph-authoring.md](references/graph-authoring.md) for selection, grounding, graph, and relationship decisions.
Use the [OKF v0.2 specification](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md) as the source of truth for frontmatter semantics.

## Source and write gate

Before analysis, confirm:

- the authoritative source and every read-only input;
- create or revise mode;
- the approved existing knowledge directory;
- the domain and approved existing MOC;
- the exact atomic-note and MOC filenames;
- the workflow and visibility tags, lifecycle status, provenance resource, producer actor, and any evidence-backed verification or expiry;
- the atomic note and MOC as the only files permitted to change.

If no existing MOC fits, offer an available domain-MOC specialist with the proposed domain and continuation context, or stop. Invoke another skill only with explicit consent. Never create a MOC inside this skill or leave an atomic note orphaned.

## Workflow

1. Read the approved source and MOC. In revise mode, read the existing atomic note. Inspect nearby note titles only to detect duplication and supported relationships.
2. Extract no more than three candidate patterns. Before presenting them, replace customer, organization, and team names with neutral role descriptions and de-identify provenance. Each candidate must include:
   - one reusable “When X, do Y, because Z” rule;
   - the learning from the source that supports it;
   - the smallest practical action;
   - observable situations that signal when it applies;
   - known constraints.
3. Ask the user to select or reframe one candidate. Handle other patterns in separate runs.
4. Propose the title, description, exact filenames, parent MOC, OKF frontmatter values, template-aligned content outline, and supported typed relationships.
5. Obtain explicit approval for the content contract and permitted files.
6. Create or revise the atomic note, then update its descriptive MOC entry and synchronize the MOC Pattern map and Domain workflow. Add or rename the pattern node, update supported edges, and use the supported workflow empty state when no defensible workflow exists.

Do not ask for information already supplied. Combine confirmations when the user can approve them safely in one decision.

## Authoring rules

- Express one reusable pattern, not a topic, source summary, broad principle collection, or implementation plan.
- Preserve distinctive non-identifying terminology, uncertainty, and boundaries from the source.
- Obfuscate customer, organization, and team names with stable neutral roles such as `a customer`, `a product team`, or `an enablement group`. Remove identifying combinations of project names, locations, dates, and organizational details when they could reveal the source.
- Start the atomic note with YAML frontmatter. Require `type: Reusable Pattern`, `title`, `description`, `tags`, `status`, `sources`, and `generated`.
- Make `title` match the H1 exactly. Write `description` as one sentence that states the decision the pattern supports.
- Put tags in the frontmatter `tags` YAML list without `#`. Include at least one lowercase kebab-case domain tag, exactly one workflow tag (`draft`, `review`, or `publish`), and exactly one visibility tag (`private` or `public`).
- Set `status` to `draft` for the `draft` or `review` workflow, and `stable` for `publish`. Use `deprecated` only when revising a formerly published pattern that is intentionally retained for history.
- Record at least one `sources` entry with a stable lowercase kebab-case `id` and `resource`. Prefer a non-identifying scope descriptor for sensitive input. Use a bundle-relative path or external URL only when the user explicitly approves exposing that source. An optional source `title` must also be de-identified.
- Use source material only for grounding. Keep source names, filenames, meeting or transcript references, customer identities, citations, attribution prose, and external source URLs out of the body and MOC entry. Put approved provenance only in frontmatter `sources`.
- Require `generated.by` and `generated.at`. Use `create-atomic-note/1.1.1` as the producer actor and an ISO 8601 generation timestamp with an explicit UTC offset. Update `generated.at` after every meaningful revision.
- Add `verified` only after an actual human or deterministic process confirms the content. Use `human:<stable-id>` or `process:<stable-id>` and an ISO 8601 timestamp. Omit `verified` rather than implying confirmation; remove stale verification after a meaningful change unless it remains truthful.
- Add `stale_after` only when the source or an approved policy supplies a defensible expiry. Use an ISO 8601 timestamp with an explicit UTC offset. Omit it rather than inventing freshness.
- Separate what was learned from what the pattern recommends.
- Explain why the pattern works through cause and effect, not unsupported benefits.
- Keep the practice observable and signals recognizable before or during application.
- Use `Parent: [<domain name>](<domain>-moc.md)`.
- Use the template's sections once each and in their defined order. Replace every instructional prompt and placeholder.
- Use standard relative Markdown links. Do not use wiki-style links or transclusions in the OKF atomic note.
- In `Relationships`, use only supported prerequisite, extension, contrast, or example links and explain each connection. If none exist, state that explicitly.
- Add the MOC entry as `- [<atomic-note-title>](<atomic-note>.md) — <navigation description>`.
- Keep the MOC Pattern map complete after adding, revising, or renaming the note. Use the atomic note's exact H1 title as its Mermaid node label and preserve only supported typed relationships.
- Keep a populated MOC Domain workflow synchronized when the note participates in it. Do not force the note into a sequence; `No supported domain workflow yet.` remains valid when no defensible workflow exists.
- Do not invent learning, evidence, causality, examples, outcomes, or relationships.

## Validate

Run:

```bash
python3 "<skill-directory>/scripts/validate_atomic_note.py" "<atomic-note.md>" "<domain-moc.md>"
```

Resolve `<skill-directory>` from this `SKILL.md`. Fix every error. Then confirm qualitatively that the source supports the learning, frontmatter provenance reveals only approved information, customer and team identities are obfuscated, lifecycle and trust claims are truthful, freshness is evidence-backed or omitted, the learning supports the pattern, the mechanism explains the recommendation, the signals indicate when to use it, the constraints prevent overgeneralization, and the MOC entry, Pattern map, and Domain workflow remain consistent.

## Companion assets

After validation, report:

- whether `<atomic-stem>.coach.md` exists;
- whether `<domain>.marp.md` exists;
- when the presentation exists, whether it has a `Source:` link for this note.

Offer available coaching or presentation specialists only with explicit consent. Pass the approved atomic note, MOC, knowledge directory, and exact target filename. Do not create companion assets inside this skill.

## Completion

Complete only when the approved atomic note and MOC are the only changed files; the note follows the template with no prompts or placeholders left; its required OKF metadata, tags, provenance, lifecycle, and generated trust signal are valid; optional verification and freshness metadata are truthful; it has one parent MOC and a descriptive MOC entry; it appears under its exact title in the complete MOC Pattern map and any populated Domain workflow; it contains one source-grounded reusable pattern without sensitive attribution in the body; it obfuscates customer and team identities; it uses only meaningful, resolvable standard Markdown relationships; and the validator reports zero errors.
