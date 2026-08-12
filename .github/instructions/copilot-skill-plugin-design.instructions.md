---
name: Copilot Skill and Plugin Design
description: "Use when creating, reviewing, or refactoring Copilot skills, plugins, SKILL.md files, validators, references, scripts, or bundled assets. Enforces atomic capabilities, loose coupling, deterministic components, reuse, and concise maintenance."
applyTo: ".github/skills/**, .github/plugin/**, plugins/**, .agents/skills/**, .claude/skills/**"
---
# Copilot Skill and Plugin Design

## General

- Treat a skill as one user-facing capability and a plugin as its installable package. Do not use the terms interchangeably.
- Collaborate through explicit capability and data contracts. Do not depend on another customization's name, caller identity, directory, or internal schema.
- Reference an existing source of truth instead of copying it. Introduce a shared dependency only when its contract and availability are intentional.
- Prefer small structured contracts over inferred conventions or prose-based coupling.
- Preserve backward compatibility only when it is cheap and explicit. Keep a replacement alias only when it has a documented owner and removal condition or deadline; otherwise remove the superseded customization.
- Optimize for maintainability: concise instructions, minimal duplication, narrow edits, and executable validation.

## Plugin

- Package skills as separate plugins when users may install, discover, version, update, or retire them independently.
- Bundle multiple skills in one plugin only when they form one cohesive product with the same lifecycle and dependencies.
- Do not preserve an obsolete plugin beside its replacement unless it is an intentional time-boxed compatibility alias. Remove the superseded package and empty directories, then update marketplace entries, documentation, paths, tests, and cross-references together.
- Keep plugin manifests and marketplace metadata aligned with the packaged skills. Use plugin-relative paths so installed components do not depend on the source repository layout.
- Keep artifact validators and domain validation logic in the owning skill directory, not the plugin root or manifest layer.
- Unit-test only executable behavior owned by the plugin, such as hooks, MCP or LSP servers, and plugin-level scripts.
- For metadata-only plugins, use static contract tests: parse manifests, check required fields, verify declared component paths and `SKILL.md` files exist, and confirm marketplace names, versions, and sources match plugin manifests.
- Run packaging integration tests with temporary, isolated `COPILOT_HOME` and `COPILOT_CACHE_HOME`, and remove them afterward. For plugin-only changes, load and install each affected plugin. For plugin manifests or marketplace changes, also register and browse the marketplace, install every catalog entry, and verify each installed component is listed.

## Skill

- Split a customization into separate skills when it delivers independently useful outcomes, has distinct approval or interaction flows, uses different inputs or outputs, or can operate without the other capability.
- Keep each skill atomic and independently usable.
- Do not preserve an obsolete skill beside its replacement unless it is an intentional time-boxed compatibility alias. Migrate the capability and remove the superseded skill, then update documentation, paths, tests, and cross-references together.
- Give each skill a unique lowercase hyphenated `name` that normally matches its directory, and a `description` that states both what the skill does and when to use it.
- Grant only the minimum `allowed-tools`. Do not pre-approve `shell` or `bash` unless the skill and every referenced script are trusted and require non-interactive execution.
- Make delegation optional. Preserve a standalone path when the capability can operate directly.
- When delegating, pass the continuation context while preserving the delegated customization's approval gates.
- Keep stable domain guidance in references and reusable scaffolding in assets. Keep `SKILL.md` focused on decisions, interaction gates, and workflow orchestration.
- When changing a contract or taxonomy, update `SKILL.md`, references, assets, scripts, and tests together. Search for stale terms, casing, and removed fields.
- For artifact-writing skills, confirm source authority, read-only inputs, create-or-revise mode, exact output filenames, and permitted files before writing.
- Keep deterministic behavior in scripts with focused tests: parsing, validation, transformations, naming, and repeatable checks. Cover both compliant artifacts and representative violations.
- Validate representative generated output against the approved source and intent. Structural checks passing is not sufficient.
- Run tests with the framework bundled by the skill. For Python `unittest` suites, run `python3 -m unittest discover -s <skill-directory>/scripts -p 'test_*.py'`. Resolve `<skill-directory>` from the installed skill rather than assuming a repository-relative path.
