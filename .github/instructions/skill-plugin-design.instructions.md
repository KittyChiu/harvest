---
name: Skill and Plugin Design
description: "Use when creating, reviewing, or refactoring Copilot skills, plugins, SKILL.md files, validators, evals, references, scripts, or bundled assets. Enforces Agent Skills conformance, atomic capabilities, loose coupling, deterministic components, and evidence-based evaluation."
applyTo: ".github/skills/**, .github/plugin/**, plugins/**, .agents/skills/**, .claude/skills/**"
---
# Skill and Plugin Design

## Outcome and Sources of Truth

Create skills that are portable, correctly packaged, independently useful, concise, and validated against current upstream standards and repository contracts.

- Treat the current [Agent Skills specification](https://agentskills.io/specification) as normative for portable skill directory structure and `SKILL.md` format. Consult it during skill work instead of relying on remembered or locally copied constraints.
- The specification shows validation examples or demonstrations (e.g. `skills-ref`). Do not install, bundle, or require these examples or demonstrations in CI, release, or runtime paths.
- Follow the current [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills) workflow for behavioral skill evals.
- Apply [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices) as authoring guidance when it does not conflict with a normative requirement.
- Treat applicable Copilot and repository schemas as normative for plugin packaging and platform-specific extensions. Apply each schema only to the surface it governs. If two normative sources conflict on the same field or behavior, report the conflict instead of guessing.
- Do not mirror upstream requirements or recommendations in this instruction. Add an overlapping local rule only when it is an intentional repository-specific extension or stricter requirement, and identify that distinction.

## Core Model

- A **skill** is one atomic, independently usable, user-facing capability. A **plugin** is the installable package that contains one or more skills. Keep these concepts and terms distinct.
- Connect capabilities through small, explicit, structured capability and data contracts rather than inferred conventions or prose-based coupling. Never couple a skill or plugin to another component's name, caller identity, directory layout, or internal schema.
- Add a shared dependency only when its contract and availability are deliberate and guaranteed.

## Skill Boundaries

- Split functionality into separate skills when any of the following is true:
  - Each part produces an independently useful outcome.
  - The parts require distinct approval or interaction flows.
  - The parts accept different inputs or produce different outputs.
  - One part can operate without the other.
- Keep delegation optional whenever a capability can run directly; preserve a complete standalone path.
- When delegation is appropriate, pass the context needed to continue the workflow without bypassing or weakening the delegated skill's approval gates.

## Required Skill Deliverables

This repository requires every skill to include both:

- A `SKILL.md` that conforms to the current Agent Skills specification.
- An `evals/evals.json` behavioral eval suite that conforms to the current Evaluating skill output quality guidance.

## Skill Authoring and Safety

- Prefer deterministic components whenever behavior can be expressed reliably as executable logic, a schema, a validator, or a static asset. Reserve prompt instructions for judgment, decisions, interaction gates, and workflow orchestration.
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
- When changing a contract or taxonomy, update its `SKILL.md`, evals, references, assets, scripts, and tests together. Search for stale terms, casing, and removed fields.
- Retain a compatibility alias only when it has a documented owner and either a removal condition or a removal deadline. Otherwise:
  - Migrate the capability.
  - Remove superseded skills or plugins and any empty directories.
  - Update package and marketplace entries, documentation, paths, tests, and references.

## Validation Requirements

### Skills

- Validate against the current Agent Skills specification with repository-owned contract tests plus applicable platform checks.
- Test or validate every deterministic behavior, including contracts, permissions, assets, parsing, transformations, naming, and artifacts.
- Cover both compliant cases and representative violations. Do not include prompt-driven behavior in deterministic tests.
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
