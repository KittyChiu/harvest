---
name: Copilot Skill and Plugin Design
description: "Use when creating, reviewing, or refactoring Copilot skills, plugins, SKILL.md files, validators, references, scripts, or bundled assets. Enforces atomic capabilities, loose coupling, deterministic components, reuse, and concise maintenance."
applyTo: ".github/skills/**, .github/plugin/**, plugins/**, .agents/skills/**, .claude/skills/**"
---
# Copilot Skill and Plugin Design

## Core Model

- A **skill** is one user-facing capability. A **plugin** is the installable package that contains one or more skills. Keep these concepts and terms distinct.
- Design each skill as an atomic, independently usable capability.
- Connect capabilities through small, explicit, structured capability and data contracts. Never couple a skill or plugin to another component's name, caller identity, directory layout, or internal schema.
- Add a shared dependency only when its contract and availability are deliberate and guaranteed.
- Prefer explicit structured contracts over inferred conventions or prose-based coupling.

## Skill Boundaries

- Split functionality into separate skills when any of the following is true:
  - Each part produces an independently useful outcome.
  - The parts require distinct approval or interaction flows.
  - The parts accept different inputs or produce different outputs.
  - One part can operate without the other.
- Keep delegation optional whenever a capability can run directly; preserve a complete standalone path.
- When delegation is appropriate, pass the context needed to continue the workflow without bypassing or weakening the delegated skill's approval gates.

## Skill Structure and Safety

- Give every skill a unique, lowercase, hyphenated `name` that normally matches its directory.
- Write a `description` that states both what the skill does and when it should be used.
- Prefer deterministic components whenever behavior can be expressed reliably as executable logic, a schema, a validator, or a static asset. Reserve prompt instructions for judgment, decisions, interaction gates, and workflow orchestration.
- Keep `SKILL.md` focused on decisions, interaction gates, and workflow orchestration. Put stable domain guidance in references, reusable static scaffolding in assets, and executable deterministic logic in scripts.
- Grant only the minimum required `allowed-tools`. Do not pre-approve `shell` or `bash` unless both the skill and every script it references are trusted and require non-interactive execution.
- Before an artifact-writing skill writes anything, confirm:
  - The authoritative source.
  - Which inputs are read-only.
  - Whether the operation creates or revises an artifact.
  - The exact output filenames.
  - The files the skill is permitted to modify.

## Plugin Boundaries and Packaging

- Package skills as separate plugins when users may install, discover, version, update, or retire them independently.
- Bundle multiple skills into one plugin only when they form a cohesive product and share the same lifecycle and dependencies.
- Keep plugin manifests and marketplace metadata synchronized with the skills actually packaged.
- Use plugin-relative paths so installed components never depend on the source repository layout.

## Ownership and Change Management

- Keep artifact-specific and domain-specific validation in the owning skill directory.
- Put validation in the plugin directory only when it spans multiple skills packaged by that plugin.
- Put validation at the marketplace layer only when it checks the catalog across plugins.
- Test skill-owned scripts in the owning skill's test suite. At the plugin layer, unit-test only plugin-owned executable behavior, including hooks, MCP or LSP servers, and plugin-level scripts.
- When changing a contract or taxonomy, update its `SKILL.md`, references, assets, scripts, and tests together. Search for stale terms, casing, and removed fields.
- Retain a compatibility alias only when it has a documented owner and either a removal condition or a removal deadline. Otherwise:
  - Migrate the capability.
  - Remove superseded skills or plugins and any empty directories.
  - Update package and marketplace entries, documentation, paths, tests, and references.

## Validation Requirements

### Skills

- Test or validate every deterministic behavior, including contracts, permissions, assets, parsing, transformations, naming, and artifacts.
- Cover both compliant cases and representative violations. Do not include prompt-driven behavior in deterministic tests.
- Validate representative generated output against the approved source and intended outcome; passing structural checks alone is not sufficient.
- Run the skill's declared or bundled test suite from its source directory.
- After installation, run integration or smoke tests against the installed skill path.

### Plugins and Marketplace

- For metadata-only plugins, add static contract tests that cover compliant artifacts and representative violations. These tests must:
  - Parse manifests.
  - Validate schema conformance and required fields.
  - Verify that declared component paths and `SKILL.md` files exist.
  - Confirm that marketplace names, versions, and sources match their plugin manifests.
- Run packaging integration tests with temporary, isolated `COPILOT_HOME` and `COPILOT_CACHE_HOME` directories, and remove those directories afterward.
- For plugin-only changes, load and install every affected plugin.
- For plugin manifest or marketplace changes, also register and browse the marketplace, install every catalog entry, and verify that every installed component is listed.
