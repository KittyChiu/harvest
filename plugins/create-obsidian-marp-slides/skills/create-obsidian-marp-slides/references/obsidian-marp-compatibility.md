# Obsidian Marp Slides compatibility

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
theme: default
paginate: true
size: 16:9
---
```

- Use the built-in `default` theme unless the user confirms another installed or built-in theme.
- Use the selected theme's standard styling; do not add custom CSS by default.
- Use standard Markdown for all visible slide content.
- Mermaid rendering is not part of the documented conservative surface, but the
  domain-presentation template requires fenced Mermaid maps and flows. Confirm
  rendering before authoring. If the target setup does not render Mermaid, stop
  rather than substituting a text map.
- Treat URL autolinks such as `<https://example.com>` and email autolinks such as `<person@example.com>` as standard Markdown, not raw HTML.
- Use Markdown image syntax rather than HTML image tags.
- Keep images local when portability or offline presenting matters.
- Use Marp directives only in HTML comments.
- Use HTML comments for speaker notes because the plugin's export implementation delegates to Marp CLI, which recognizes this form. Speaker-note comments are an explicit exception to the raw HTML restriction.

## Do not use by default

- HTML layout containers such as `<div>`, `<section>`, `<span>`, or `<p>`;
- CSS that depends on those containers;
- remote fonts or remote runtime assets;
- JavaScript;
- Markdown-it containers or other plugins unless the caller confirms they are installed;
- complex nested tables;
- browser-specific layout tricks.

## Coaching speaker notes

The plugin's syntax page describes square-bracket notes, but a bare Markdown block such as `[note]` is not the standard Marp CLI speaker-note representation. The plugin uses Marp CLI for export, including its PDF-notes mode. When a coaching companion exists, use a Marp HTML-comment note block on the relevant slide with a non-empty `Coach cue:`:

```markdown
# Slide title

Visible slide content.

<!--
Coach cue: What changes when the audience applies this idea?
-->
```

This is not arbitrary slide-body HTML. The compatibility restriction targets rendered HTML layout elements such as `<div>`, not Marp's comment-based directives or notes.

Speaker notes carry narrative and source metadata even when no coaching companion exists. Every pattern slide has one non-empty `Coach cue:` question ending in `?`; when a matching companion exists, link it under the note block's `Source:`.

## Density guardrails

Treat these as warnings, not rigid limits:

- title: approximately 8–12 words;
- body: approximately 40–70 visible words;
- bullets: 3–5;
- table: no more than 5 columns or 6 body rows;
- code: approximately 12–15 visible lines;
- one primary pattern per slide.

Split content when the audience would need to read rather than listen.
