# Obsidian Marp compatibility

Use the conservative subset of Marp supported by the Obsidian Marp Slides plugin.

## Confirmed surfaces

The plugin documentation describes:

- standard Markdown;
- `---` or `===` slide separators;
- fenced code blocks and syntax highlighting;
- built-in and custom themes;
- preview, export, and presentation features.

References:

- [Marp Syntax](https://samuele-cozzi.github.io/obsidian-marp-slides/13.MarpSyntax.html)
- [Features](https://samuele-cozzi.github.io/obsidian-marp-slides/20.Features.html)

## Safe defaults

```yaml
---
marp: true
theme: gaia
class: invert
paginate: true
size: 16:9
---
```

- Prefer built-in themes: `default`, `gaia`, or `uncover`.
- Use standard Markdown for all visible slide content.
- Use Markdown image syntax rather than HTML image tags.
- Keep images local when portability or offline presenting matters.
- Use Marp directives only in HTML comments.
- Use HTML comments for speaker notes because the plugin's export implementation delegates to Marp CLI, which recognizes this form.

## Do not use by default

- HTML layout containers such as `<div>`, `<section>`, `<span>`, or `<p>`;
- CSS that depends on those containers;
- remote fonts or remote runtime assets;
- JavaScript;
- Markdown-it containers or other plugins unless the caller confirms they are installed;
- complex nested tables;
- browser-specific layout tricks.

## Speaker-note clarification

The plugin's syntax page describes square-bracket notes, but a bare Markdown block such as `[note]` is not the standard Marp CLI speaker-note representation. The plugin uses Marp CLI for export, including its PDF-notes mode. Use Marp's HTML-comment note blocks for reliable rendering and export:

```markdown
# Slide title

Visible slide content.

<!--
Presenter-only narrative.
-->
```

This is not arbitrary slide-body HTML. The compatibility restriction targets rendered HTML layout elements such as `<div>`, not Marp's comment-based directives or notes.

## Density guardrails

Treat these as warnings, not rigid limits:

- title: approximately 8–12 words;
- body: approximately 40–70 visible words;
- bullets: 3–5;
- table: no more than 5 columns or 6 body rows;
- code: approximately 12–15 visible lines;
- one primary claim per slide.

Split content when the audience would need to read rather than listen.

