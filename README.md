# Harvest Dialogue

A GitHub Copilot CLI plugin marketplace for turning source material into reusable knowledge and learning experiences.

## Available plugins

| Plugin | Capability |
| --- | --- |
| `create-knowledge-note` | Create or revise a concise second-brain knowledge note. |
| `create-learning-module` | Create paired participant and coach guides for a self-paced module. |
| `create-obsidian-marp` | Create a narrative Marp deck for the Obsidian Marp Slides plugin. |

The skills include Python validators, so Python 3 is required when generating or validating an artifact.

## Add the marketplace

```bash
copilot plugin marketplace add KittyChiu/harvest-dialogue
copilot plugin marketplace browse harvest-dialogue
```

## Install a plugin

Install only the capabilities you need:

```bash
copilot plugin install create-knowledge-note@harvest-dialogue
copilot plugin install create-learning-module@harvest-dialogue
copilot plugin install create-obsidian-marp@harvest-dialogue
```

Restart an active Copilot CLI session after installation, then use `/skills list` to verify that the installed skill is available.

## Update

```bash
copilot plugin marketplace update harvest-dialogue
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
