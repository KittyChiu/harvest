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
