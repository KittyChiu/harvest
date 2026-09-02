# Atomic-note graph authoring

## Choose one idea

An atomic note makes one claim that can be reused in more than one context.

Good titles state the claim:

- `platform-engineering-is-a-product-discipline`
- `golden-paths-reduce-cognitive-load`

Avoid topic containers such as `everything-about-platform-engineering`. Broad navigation belongs in the domain MOC.

When reading a source:

1. Remove meeting narrative, repeated wording, and delivery commentary.
2. Group duplicate claims.
3. Preserve meaningful tensions and constraints.
4. Propose no more than three candidate claims.
5. Write only the selected claim.

## Choose the parent MOC

Every atomic note has one primary domain MOC. Use an approved existing MOC whose scope clearly contains the idea. If none fits, offer an available domain-MOC specialist with the approved continuation context or stop; do not create the MOC inside the atomic-note workflow.

The atomic note uses:

```markdown
Parent: [AI engineering](ai-engineering-moc.md)
```

The MOC uses a descriptive navigation entry:

```markdown
- [Golden paths reduce cognitive load](ai-engineering-golden-paths-reduce-cognitive-load.md) — Why paved roads matter more as AI increases change volume.
```

The description helps a reader decide whether to open the note.

## Create meaningful relationships

A relationship must explain the connection in a sentence:

```markdown
Platform teams need stronger paved roads when [AI-assisted development changes the unit of work](ai-assisted-development-changes-the-unit-of-work.md) because the volume and speed of change increase.
```

Do not write a bare list:

```markdown
- [Platform engineering](platform-engineering.md)
- [AI](ai.md)
```

Use portable relative Markdown links by default. Wiki-style internal links are also acceptable when the selected PKM tool prefers them. Link only to notes that already exist in the approved knowledge directory. Prefer no related link over a planned, dangling, or decorative one.

## Apply tags

Use inline tags as plain Markdown text for three filtering dimensions:

- domain: one or more subject tags such as `#ai`, `#platform`, or `#leadership`;
- workflow: exactly one of `#draft`, `#review`, or `#publish`;
- visibility: exactly one of `#private` or `#public`.

Additional useful tags are allowed, but tags do not replace MOCs or relationship sentences.

Apply the same workflow and visibility categories to a MOC, alongside its domain tag and `#moc`, so navigation notes can be filtered and published deliberately.

Do not add tool-specific front matter, database properties, queries, transclusions, or plugins unless the user explicitly requests them.

## Review

Before completion, confirm:

- the title is one reusable claim;
- the content can stand alone without the source;
- the MOC is the right navigation home;
- the MOC entry describes the note;
- each relationship states why the linked idea matters;
- the tags support filtering rather than duplicating prose;
- no unsupported certainty, quote, example, or relationship was added.
