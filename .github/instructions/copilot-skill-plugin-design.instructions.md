---
name: Copilot Skill and Plugin Design
description: "Use when creating, reviewing, or refactoring Copilot skills, plugins, SKILL.md files, validators, references, scripts, or bundled assets. Enforces atomic capabilities, loose coupling, deterministic components, reuse, and concise maintenance."
applyTo: ".github/skills/**, .github/plugins/**, .agents/skills/**, .claude/skills/**"
---
# Copilot Skill and Plugin Design

- Keep each skill or plugin atomic and independently usable.
- Collaborate through explicit capability and data contracts. Do not depend on another customization's name, caller identity, directory, or internal schema.
- Make delegation optional. Preserve a standalone path when the capability can operate directly.
- Keep deterministic behavior in scripts with focused tests: parsing, validation, transformations, naming, and repeatable checks.
- Keep stable domain guidance in references and reusable scaffolding in assets. Keep `SKILL.md` focused on decisions, interaction gates, and workflow orchestration.
- When changing a contract or taxonomy, update `SKILL.md`, references, assets, scripts, and tests together. Search for stale terms, casing, and removed fields.
- Reference an existing source of truth instead of copying it. Introduce a shared dependency only when its contract and availability are intentional.
- Prefer small structured contracts over inferred conventions or prose-based coupling.
- Before writing, confirm source authority, read-only inputs, exact output path and filename, and permitted files. Do not infer artifact locations.
- Preserve backward compatibility only when it is cheap and explicit; mark legacy aliases clearly.
- Validate representative generated output against the approved source and intent. Structural checks passing is not sufficient.
- Optimize for maintainability: concise instructions, minimal duplication, narrow edits, and executable validation.