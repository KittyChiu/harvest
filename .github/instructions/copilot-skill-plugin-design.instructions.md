---
name: Copilot Skill and Plugin Design
description: "Use when creating, reviewing, or refactoring Copilot skills, plugins, SKILL.md files, validators, references, scripts, or bundled assets. Enforces atomic capabilities, loose coupling, deterministic components, reuse, and concise maintenance."
applyTo: ".github/skills/**, .github/plugin/**, plugins/**, .agents/skills/**, .claude/skills/**"
---
# Copilot Skill and Plugin Design

## General

- Treat a skill as one user-facing capability and a plugin as the installable package for one or more skills. Do not use the terms interchangeably.
- Collaborate through explicit capability and data contracts. Do not depend on another skill or plugin's name, caller identity, directory, or internal schema.
- Reference an existing source of truth instead of copying it. Introduce a shared dependency only when its contract and availability are intentional.
- Prefer small structured contracts over inferred conventions or prose-based coupling.
- Keep compatibility aliases only with a documented owner and removal condition or deadline. Otherwise migrate the capability, remove superseded skills or plugins and empty directories, and update package and marketplace entries, documentation, paths, tests, and references.
- Optimize for maintainability: concise instructions, minimal duplication, narrow edits, and executable validation.

## Plugin

- Package skills as separate plugins when users may install, discover, version, update, or retire them independently.
- Bundle multiple skills in one plugin only when they form one cohesive product with the same lifecycle and dependencies.
- Keep plugin manifests and marketplace metadata aligned with the packaged skills. Use plugin-relative paths so installed components do not depend on the source repository layout.
- Keep artifact and domain validation in the owning skill directory. Use the plugin directory only for validation spanning multiple packaged skills, and the marketplace layer only for cross-plugin catalog validation.
- At the plugin layer, unit-test plugin-owned executable behavior such as hooks, MCP or LSP servers, and plugin-level scripts. Test skill-owned scripts in the owning skill's suite.
- For metadata-only plugins, use static contract tests covering compliant artifacts and representative violations: parse manifests, validate schema conformance and required fields, verify declared component paths and `SKILL.md` files exist, and confirm marketplace names, versions, and sources match plugin manifests.
- Run packaging integration tests with temporary, isolated `COPILOT_HOME` and `COPILOT_CACHE_HOME`, and remove them afterward. For plugin-only changes, load and install each affected plugin. For plugin manifests or marketplace changes, also register and browse the marketplace, install every catalog entry, and verify each installed component is listed.

## Skill

- Split functionality into separate skills when it delivers independently useful outcomes, has distinct approval or interaction flows, uses different inputs or outputs, or can operate without the other capability.
- Keep each skill atomic and independently usable.
- Give each skill a unique lowercase hyphenated `name` that normally matches its directory, and a `description` that states both what the skill does and when to use it.
- Grant only the minimum `allowed-tools`. Do not pre-approve `shell` or `bash` unless the skill and every referenced script are trusted and require non-interactive execution.
- Make delegation optional. Preserve a standalone path when the capability can operate directly.
- When delegating, pass the continuation context while preserving the delegated skill's approval gates.
- Keep stable domain guidance in references and reusable scaffolding in assets. Keep `SKILL.md` focused on decisions, interaction gates, and workflow orchestration.
- When changing a contract or taxonomy, update `SKILL.md`, references, assets, scripts, and tests together. Search for stale terms, casing, and removed fields.
- For artifact-writing skills, confirm source authority, read-only inputs, create-or-revise mode, exact output filenames, and permitted files before writing.
- Test or validate deterministic skill behavior, including contracts, permissions, assets, parsing, transformations, naming, and artifacts. Cover compliant and violating cases; exclude prompt-driven behavior from deterministic tests.
- Validate representative generated output against the approved source and intent. Structural checks passing is not sufficient.
- Run the skill's declared or bundled test suite from its source directory. Run post-install integration or smoke tests against the installed skill path.
