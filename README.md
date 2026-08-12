# Harvest

[![CI](https://github.com/KittyChiu/harvest/actions/workflows/ci.yml/badge.svg)](https://github.com/KittyChiu/harvest/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A GitHub Copilot CLI plugin marketplace for turning source material into reusable knowledge and learning experiences.

## Available plugins

| Plugin | Capability |
| --- | --- |
| `create-knowledge-note` | Create or revise a concise second-brain knowledge note. |
| `create-learning-module` | Create paired participant and coach guides for a self-paced module. |
| `create-obsidian-marp` | Create a narrative Marp deck for the Obsidian Marp Slides plugin. |

The skills include Python validators, so Python 3.10 or later is required when generating or validating an artifact.

## Add the marketplace

```bash
copilot plugin marketplace add KittyChiu/harvest
copilot plugin marketplace browse harvest
```

## Install a plugin

Install only the capabilities you need:

```bash
copilot plugin install create-knowledge-note@harvest
copilot plugin install create-learning-module@harvest
copilot plugin install create-obsidian-marp@harvest
```

Restart an active Copilot CLI session after installation, then use `/skills list` to verify that the installed skill is available.

## Update

```bash
copilot plugin marketplace update harvest
copilot plugin update create-knowledge-note
```

Replace `create-knowledge-note` with the installed plugin you want to update.

## Local development

Load a plugin directly from the repository without installing it:

```bash
copilot --plugin-dir ./plugins/create-knowledge-note plugin list
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
