# Harvest

[![CI](https://github.com/KittyChiu/harvest/actions/workflows/ci.yml/badge.svg)](https://github.com/KittyChiu/harvest/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A GitHub Copilot CLI plugin marketplace for building a portable personal knowledge management (PKM) graph from domain Maps of Content, atomic notes, meaningful internal links, and filtering tags.

## Available plugins

| Plugin | Capability |
| --- | --- |
| `create-domain-moc` | Define one domain and create its navigation MOC. |
| `create-atomic-note` | Create one reusable knowledge pattern and connect it to a domain MOC. |
| `create-coaching-note` | Turn one atomic pattern into a supportive coaching experience. |
| `create-obsidian-marp-slides` | Present the domain as one connected system of patterns, practices, and optional coaching companions. |

Together, the plugins use one flat directory in any file-based PKM tool:

```text
<knowledge-directory>/
├── <domain>-moc.md
├── <domain>-<pattern>.md
├── <domain>-<pattern>.coach.md
└── <domain>.marp.md
```

Portable relative Markdown links are the default. Wiki-style internal links are also accepted for PKM tools that use them. Each domain has at most one Marp presentation, which draws from the atomic notes linked by its MOC. Only `create-obsidian-marp-slides` is tool-specific because its output depends on the Obsidian Marp Slides plugin.

Each plugin remains independently installable. The skills include Python validators, so Python 3.10 or later is required when generating or validating an artifact.

## Add the marketplace

```bash
copilot plugin marketplace add KittyChiu/harvest
copilot plugin marketplace browse harvest
```

## Install a plugin

Install only the capabilities you need:

```bash
copilot plugin install create-domain-moc@harvest
copilot plugin install create-atomic-note@harvest
copilot plugin install create-coaching-note@harvest
copilot plugin install create-obsidian-marp-slides@harvest
```

Restart an active Copilot CLI session after installation, then use `/skills list` to verify that the installed skill is available.

## Use the installed skills

Invoke a skill by name in a normal Copilot prompt. For best results, provide:

- the existing knowledge directory where artifacts may be written;
- the source material or patterns to capture;
- the workflow and visibility tags;
- the audience and objective when requesting coaching notes or slides.

The skills pause for approval before writing files. `create-atomic-note` and
`create-coaching-note` each handle one pattern per invocation, while
`create-obsidian-marp-slides` creates one presentation for the complete domain.

For example:

```text
Use create-domain-moc to create the "delivery" domain in <knowledge-directory>
with #draft and #private tags.

After the MOC is created, use create-atomic-note once for each of
these engineering delivery patterns:

- Plan first, then code as stacked changes.
- Move from user story to implementation plan to code.

For each pattern, identify which GitHub Copilot features or specific
capabilities to apply at each step, explain how they support the pattern, and
include that guidance in the atomic note. Consider planning, custom
instructions, agent workflows, code review, and pull request capabilities
where they are relevant; do not force a feature where it does not fit.

For each approved atomic note, use create-coaching-note to create a companion
for software engineers learning the pattern.

Finally, use create-obsidian-marp-slides to create delivery.marp.md for a
30-minute engineering team workshop. Use the delivery MOC, its atomic notes,
and their coaching companions as read-only sources.
```

Replace `<knowledge-directory>` with an existing directory in your PKM tool or
Obsidian vault. Copilot will guide you through the required scope, filename,
source, and write approvals at each stage. Run the steps as separate prompts if
you want to review each artifact before continuing.

## Update

```bash
copilot plugin marketplace update harvest
copilot plugin update create-atomic-note
```

Replace `create-atomic-note` with the installed plugin you want to update.

## Local development

Load a plugin directly from the repository without installing it:

```bash
copilot --plugin-dir ./plugins/create-atomic-note plugin list
```

Each directory under `plugins/` is an independent plugin. The marketplace catalog is defined in `.github/plugin/marketplace.json`.

Run the marketplace contract tests after changing a plugin manifest, skill path, or catalog entry:

```bash
python3 -m unittest discover -s .github/plugin/scripts -p 'test_*.py'
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the complete development and pull
request workflow.

## Community and security

- Use [GitHub Issues](https://github.com/KittyChiu/harvest/issues) for bugs and feature requests.
- Read [SUPPORT.md](SUPPORT.md) before requesting help.
- Report vulnerabilities privately by following [SECURITY.md](SECURITY.md).
- Participation is governed by [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## License

Harvest is available under the [MIT License](LICENSE).
