---
name: Context Authoring
description: "Use when creating, reviewing, or revising SKILL.md, custom agent, prompt, or custom instruction files. Uses the context sandwich to make instructions focused, actionable, and verifiable."
applyTo: "**/SKILL.md, **/*.agent.md, **/*.prompt.md, **/*.instructions.md, **/copilot-instructions.md"
---
# Context Authoring

This instruction governs how instructional content communicates behavior. It does not define primitive architecture or prove behavioral reliability.

## Core Frame: Context Sandwich

Structure each instruction artifact around four layers. Apply the frame to the document as a whole and, when useful, to a major workflow or decision section. Do not repeat layers mechanically when the information is already clear.

### 1. Goal or Outcome

- State the behavior or capability the artifact must produce.
- Define when the instruction applies and the observable successful result.
- Lead with the outcome, not background, implementation detail, or motivational prose.

### 2. Relevant Context

- Include only the domain facts, inputs, terminology, source hierarchy, and references needed to act correctly.
- Explain why context matters when its relevance is not self-evident.
- Reference an authoritative source instead of copying it. Do not embed broad repository context that the agent can inspect when needed.
- Keep examples representative and focused; examples illustrate rules but do not replace them.

### 3. Constraints and Requirements

- State must, must-not, boundary, approval, assumption, edge-case, and compatibility rules explicitly.
- Separate unconditional rules from conditional behavior.
- Define completion and validation criteria that can be observed or executed.
- Resolve contradictions within the artifact and state precedence when two local rules could apply at the same time.

### 4. Action and Response Contract

- Specify the workflow or decisions the agent must carry out.
- Define the required output, evidence, validation, or handoff.
- Request concise rationale, assumptions, and supporting evidence when useful. Do not request private step-by-step reasoning.
- Make failure and uncertainty behavior explicit when proceeding would be unsafe or materially change scope.

## Authoring Standard

- Write direct, imperative, testable instructions.
- Prefer precise conditions and concrete outcomes over broad advice such as "be careful" or "use best practices."
- Keep the artifact concise. Remove duplicated rules, redundant examples, and context that does not affect a decision.
- Keep each rule in the narrowest owning instruction domain. Do not restate rules owned by a more general or more specialized instruction.
- Use stable terminology consistently. Define terms that could be interpreted more than one way.
- Follow the platform's format, discovery, naming, and frontmatter requirements for the artifact type being authored.

## Review Checklist

Before completing an instruction artifact, verify:

1. The intended behavior, trigger, and successful outcome are clear.
2. Every included context item helps the agent make a decision.
3. Constraints are explicit, internally consistent, and paired with completion criteria.
4. The required workflow and output are actionable and verifiable.
5. Sources of truth are referenced rather than copied.
6. Rules are not duplicated across general and specialized instruction domains.
