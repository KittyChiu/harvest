# Contributing to Harvest

Thank you for helping improve Harvest.

## Before you start

- Search existing issues before opening a new one.
- Open an issue before making a substantial behavior or contract change.
- Keep each plugin independently installable and each skill focused on one capability.
- Do not commit source transcripts, generated project outputs, credentials, or personal data.

## Development

Requirements:

- Python 3.10 or later
- GitHub Copilot CLI for plugin integration checks

Clone the repository and run the contract tests:

```bash
python3 -m unittest discover -s .github/plugin/scripts -p 'test_*.py'
```

Run all skill validator tests:

```bash
for skill in create-domain-moc create-atomic-note create-coaching-note create-obsidian-marp-slides; do
  python3 -m unittest discover -s "plugins/$skill/skills/$skill/scripts" -p 'test_*.py'
done
```

Load an affected plugin directly:

```bash
copilot --plugin-dir ./plugins/create-atomic-note plugin list
```

When changing a plugin version or metadata, update both its `plugin.json` and
the matching entry in `.github/plugin/marketplace.json`.

## Pull requests

- Keep changes scoped and explain the user-facing outcome.
- Add or update tests for contract or validator changes.
- Update documentation and templates when behavior changes.
- Confirm all checks pass before requesting review.

By contributing, you agree that your contributions are licensed under the
[MIT License](LICENSE).
