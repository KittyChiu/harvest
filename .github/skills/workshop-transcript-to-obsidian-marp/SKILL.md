---
name: workshop-transcript-to-obsidian-marp
description: Turn a thought-leadership whitepaper, existing IP, or workshop transcript into a narrative Marp deck with speaker notes that works in the Obsidian Marp Slides plugin. Use for presentations, workshop decks, reusable slides, or Marp Markdown. When a whitepaper is supplied, treat it as the source of truth and focus the deck on why the idea matters, what it is, and an example or demonstration of how to apply it.
compatibility: >
  Produces Markdown for the Obsidian Marp Slides plugin and standard Marp CLI.
  Uses Python 3 only for the optional bundled validator.
---

# Workshop Transcript to Obsidian Marp

Turn source material into an evidence-grounded, reusable presentation rather than a document summary.

## Required input

The caller must provide:

1. **IP source**: a canonical whitepaper, another existing thought-leadership artifact, a transcript, pasted text, or readable file paths.
2. **Deck brief**: the content and outcome the slides must deliver.

The deck brief should state as many of these as are known:

- audience;
- presentation objective;
- required messages or sections;
- desired duration or slide count;
- tone;
- workshop exercises or calls to action;
- output path.

Treat the deck brief as authoritative for presentation scope.

Use this source precedence:

1. canonical whitepaper;
2. other explicitly approved IP;
3. raw transcript or workshop notes;
4. new synthesis, clearly identified as such.

When a whitepaper is supplied, preserve its canonical terminology, claims, framework, boundaries, and provenance. Use transcripts primarily for stories, examples, analogies, demonstrations, and speaker-note texture. Do not silently change the underlying IP.

If the IP source or deck brief is missing, ask one focused question before authoring. Do not invent the requested slide content.

## Output

Create one self-contained `.md` Marp deck unless the caller requests additional artifacts.

The deck must:

- open with valid Marp YAML front matter;
- use a built-in theme by default;
- contain a clear narrative arc;
- include speaker notes on every substantive slide;
- remain grounded in the supplied source of truth;
- distinguish direct quotes from paraphrases and new synthesis;
- pass the compatibility checks in [references/obsidian-marp-compatibility.md](references/obsidian-marp-compatibility.md).

## Workflow

### 1. Read the whole source before designing slides

Read the source material in sections when necessary, but build the deck only after reviewing the complete source.

If the source is a whitepaper, first extract its downstream map:

- central thesis and audience problem;
- canonical framework and terminology;
- key principles and practices;
- strongest example or demonstration;
- boundaries, risks, and anti-patterns;
- claims and evidence;
- recommended action.

Create a private evidence inventory:

| Evidence type | Harvest |
|---|---|
| Problems | Friction, failed approaches, misconceptions, tensions |
| Insights | Principles, lessons, decisions, surprising conclusions |
| Stories | Incidents with a setup, turning point, and consequence |
| Analogies | Memorable comparisons already used by participants |
| Language | Distinctive phrases and quotable wording |
| Practices | Repeatable steps, checklists, methods, experiments |
| Proof | Results, observations, examples, demonstrations |
| Open questions | Ambiguity that should not be presented as settled fact |

Do not flatten disagreement or uncertainty. Do not fabricate quotes, outcomes, metrics, or consensus.

### 2. Convert the brief into a presentation promise

Write a one-sentence internal promise:

> By the end, this audience will understand or be able to **[observable outcome]**.

Discard source material that does not support that promise. A source document is not the slide order.

### 3. Build a narrative, not meeting minutes

Prefer this arc unless the brief calls for another:

1. **Hook** — a vivid analogy, incident, question, or contradiction.
2. **Tension** — why the familiar approach fails or carries risk.
3. **Discovery** — what the workshop revealed.
4. **Model** — the framework, principles, or mental model.
5. **Practice** — examples, workflow, exercise, or decision guide.
6. **Transfer** — what the audience should reuse or change afterward.

Use the strongest source analogy or incident as a recurring thread when it genuinely supports the argument.

For thought-leadership presentations, emphasize:

- **why** the audience should care;
- **what** the idea, framework, or practice is;
- one credible **example or demonstration** of how to apply it.

Leave comprehensive implementation instruction to the facilitator guide and detailed IP exposition to the whitepaper.

### 4. Design the slide architecture

Before writing prose, assign each slide one job.

For each planned slide define:

- **purpose** — why this slide exists;
- **headline** — the point, not merely the topic;
- **evidence** — source material supporting it;
- **visual form** — short list, comparison table, quote, process, code, or image;
- **transition** — why the next slide follows.

Typical pacing is one slide per 1–3 minutes. Prefer fewer strong slides over dense coverage.

### 5. Write slides for projection

- Express one primary idea per slide.
- Use short, assertion-led headlines.
- Keep body copy scannable from a distance.
- Prefer 3–5 bullets or a small table.
- Split a dense slide rather than shrinking everything.
- Put explanation, caveats, provenance, and transitions in speaker notes.
- Use direct quotes only when the source supports the exact wording.
- Label newly created frameworks or synthesis honestly.

Avoid agenda-heavy openings, walls of prose, decorative jargon, and generic closing slides.

### 6. Write narrative speaker notes

Every substantive slide needs notes that help a presenter tell the story rather than read the slide.

Notes should contain the useful subset of:

- the spoken setup;
- the source story or analogy;
- the point the audience should infer;
- a concrete example;
- a question or interaction prompt;
- a transition to the next slide;
- a caveat or provenance reminder.

Use Marp speaker-note comments:

```markdown
<!--
Tell the story in natural spoken language.

Ask: "What would happen in your environment?"

Transition: "That leads to the boundary we need to define."
-->
```

Do not use `<div>`, `<span>`, `<p>`, or other HTML layout elements. HTML comments are allowed only for Marp directives and speaker notes.

### 7. Apply the Obsidian-safe Marp format

Start from [assets/deck-template.md](assets/deck-template.md). Use simple front matter:

```yaml
---
marp: true
theme: gaia
class: invert
paginate: true
size: 16:9
---
```

Use:

- `---` on its own line as the slide separator;
- standard Markdown headings, lists, tables, links, images, blockquotes, and fenced code;
- built-in `default`, `gaia`, or `uncover` themes unless a tested local theme is requested;
- `<!-- _class: lead invert -->` for local slide directives when useful.

Do not depend on arbitrary HTML layout, remote web fonts, JavaScript, or uninstalled Markdown-it plugins.

### 8. Validate before finishing

Run:

```bash
python3 .github/skills/workshop-transcript-to-obsidian-marp/scripts/validate_marp.py "<deck.md>"
```

Then inspect the output for:

- slide count;
- notes on every substantive slide;
- accidental raw HTML;
- malformed front matter;
- content density and likely overflow;
- unsupported dependencies;
- ungrounded quotes or claims;
- drift from canonical whitepaper terminology or boundaries.

If a Marp preview command already exists in the environment, use it. Do not install new tooling solely to preview the deck unless the caller requests it.

## Quality bar

The result is complete only when:

- the deck fulfills the caller's brief;
- the narrative can be followed without reading the transcript;
- the speaker notes preserve useful human texture from the source;
- source evidence and new synthesis are not confused;
- the file is valid, portable Marp Markdown for the Obsidian plugin;
- a presenter can deliver it without reconstructing missing context.

## Invocation examples

> Use the workshop-transcript-to-obsidian-marp skill. Source of truth: `context-whitepaper.md`. Create a 20-minute deck for engineering leaders explaining why context quality matters, what the framework is, and one demonstration of how to apply it. Save it as `context-workshop-marp.md`.

> Turn `discovery-session.txt` into 12 Obsidian Marp slides. Audience: product managers. Required content: customer pain, three insights, the decision framework, and a closing exercise. Keep the tone practical and include narrative speaker notes.
