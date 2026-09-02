# Domain MOC design

## Decide whether a domain should exist

A domain deserves its own MOC when it gives a stable answer to:

> Would a reader expect to look here for this atomic idea?

Create a separate domain when the scope, audience, or navigation purpose is meaningfully distinct. Do not create one merely because a source uses a new label.

Before creating a MOC:

1. Inspect existing MOC titles and scopes.
2. Identify overlap and likely ambiguity.
3. Prefer one clear home over duplicate navigation.
4. State why the proposed domain is useful.

## Define boundaries

A useful scope says both what belongs and what does not.

Weak:

> Notes about AI.

Stronger:

> Reusable ideas about how AI changes software engineering work and operating models. Product announcements and tool-specific setup instructions belong elsewhere.

Keep the scope stable enough to guide future notes without trying to predict every subtopic.

## Write navigation entries

Each entry combines an internal link with a short reason to open it. Use portable relative Markdown by default:

```markdown
- [Golden paths reduce cognitive load](ai-engineering-golden-paths-reduce-cognitive-load.md) — Why paved roads matter as AI increases change volume.
```

Do not use bare links, duplicate the atomic note, or link to a file that does not exist. If the domain has no notes, use `No atomic notes yet.` until the first note is created.

## Connect adjacent domains

Link another MOC only when the relationship improves navigation, and explain it:

```markdown
This domain intersects [Platform engineering](platform-engineering-moc.md) where AI-enabled delivery increases the need for paved roads and guardrails.
```

## Apply tags

Every MOC uses:

- one or more domain tags;
- `#moc`;
- exactly one workflow tag: `#draft`, `#review`, or `#publish`;
- exactly one visibility tag: `#private` or `#public`.

These conventions are plain Markdown text. If the selected PKM tool prefers wiki-style internal links, that syntax is also valid; do not otherwise introduce tool-specific metadata or query features.

## Review

Confirm:

- the domain does not duplicate an existing MOC;
- the scope guides inclusion and exclusion;
- every linked note exists and clearly belongs;
- every link has a navigation explanation;
- the tags support filtering and publishing workflow;
- the MOC remains navigation rather than becoming a long-form note.
