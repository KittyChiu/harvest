---
name: review-primitive
description: "Evaluate Copilot prompts, instructions, agents, skills, plugins, tools, retrieval, memory, or orchestration using layered, outcome-based reliability evidence."
argument-hint: "Identify the primitive and the decision this evaluation must support"
agent: agent
---
# Primitive Review

Evaluate the Copilot primitive identified by the user or current context. If the target or evaluation decision is unclear and would materially change the review, ask one focused clarifying question before proceeding.

## Scope and Boundary

This review assesses behavioral reliability and the evidence available to support a development, regression, release, monitoring, or incident decision. It does not replace:

- [Context Authoring](../instructions/context-authoring.instructions.md) for reviewing the clarity and structure of instructional content.
- [Skill and Plugin Design](../instructions/skill-plugin-design.instructions.md) for reviewing skill and plugin boundaries, implementation, ownership, packaging, and deterministic artifact validation.

## Evaluation Frame

Use the context sandwich to define the evaluation before selecting metrics or graders.

### 1. Goal or Decision

- State the decision the evaluation supports: development comparison, regression review, launch readiness, production monitoring, or incident analysis.
- Define observable success through the requested outcome, expected environment state, required and prohibited actions, and relevant operating budgets.
- Select measures that can change the stated decision. Do not begin with a generic scorecard.

### 2. Relevant System Context

- Identify the primitive under evaluation, its dependencies, configuration and version, authoritative data sources, risk level, and current baseline.
- Evaluate the primitive independently and in realistic composition with routing, retrieval, tools, memory, handoffs, and recovery behavior.
- Include real tasks, confirmed historical failures, edge cases, and adversarial or prompt-injection cases that represent material risks.

### 3. Constraints and Reliability Requirements

- Prefer deterministic assertions and environment-state checks where possible, rubric-based judgment where necessary, and human calibration where consequences are material.
- Treat verified outcomes as primary release evidence. Use traces to diagnose routing, instruction, tool, handoff, and recovery failures.
- Do not require one exact trajectory unless the path is itself a control requirement. Hard-check required confirmations, authorization, prohibited actions, and other mandatory controls.
- Treat safety, security, privacy, authorization, and policy controls as non-compensatory gates. A good aggregate score must not offset a critical violation.
- Do not prescribe universal thresholds or collapse distinct failure modes into one agent-quality score. Set thresholds from risk, baseline performance, and failure consequences.

### 4. Evaluation Protocol and Report

- Build or propose a versioned scenario set with expected outcomes, required or prohibited behavior, evaluator choice, and failure classification.
- Run repeated trials in a controlled or simulated environment when execution is available and behavior is nondeterministic.
- Capture inputs, relevant configuration, retrieval, tool calls, state transitions, outputs, errors, latency, and usage needed to reproduce and diagnose results.
- Grade with the smallest reliable combination of deterministic checks, rubric judges, adversarial tests, and human review.
- Compare results with the versioned baseline and report regressions, uncertainty, evidence gaps, and decision impact.
- Add confirmed, representative production failure modes to regression coverage.

## Evaluation Surface

Evaluate only the surfaces relevant to the primitive and decision:

| Primitive | Independent evaluation | Composed evaluation |
|---|---|---|
| Prompt | Intent coverage, ambiguity, input and phrasing variation, expected assertions | Correct capability activation for realistic requests |
| Instructions | Adherence, precedence, scope boundaries, clarification, refusal, format and policy | Robustness under long context, tool output, memory, and adversarial content |
| Agent or skill | Task contract, prerequisites, required steps, tool composition, output contract, failure behavior | Correct selection, handoffs, recovery, and contribution to the outcome |
| Plugin or tool | Schema, arguments, authorization, correctness, side effects, idempotency, timeout and error behavior | Selection, sequencing, retry, confirmation, and least-privilege use |
| Retrieval or memory | Relevance, recall, freshness, provenance, citation, retention and isolation | Useful decision support without overriding authoritative instructions |
| Planning or orchestration | Completeness, termination, delegation boundaries, loop and budget limits | Goal achievement, recovery, handoffs, and absence of prohibited actions |
| End to end | Not applicable | Verified final state, task success, consistency, safety, latency, and cost |

## Reliability and Evaluation Quality

- Assess outcome reliability, behavioral reliability, safety and control, and operability separately.
- For reliability-sensitive behavior, report per-trial success and the probability that all repeated trials succeed (`pass^k`), not only whether any trial succeeds (`pass@k`).
- Validate the evaluation system before using it as a gate: check scenario and failure-mode coverage, grader-human agreement, reproducibility, uncertainty, saturation, and drift.
- Reevaluate when a model, prompt, instruction, orchestrator, tool, retrieval source, or other material dependency changes.
- If execution or reliable grading is unavailable, report the review as static analysis and identify the missing evidence. Do not claim behavioral reliability from inspection alone.

## Required Review Output

Report:

1. The primitive, evaluation decision, scope, baseline, and success criteria.
2. Evidence gathered and evaluation methods used.
3. Findings separated into outcome, behavior, safety and control, and operability.
4. Independent-component and composed-system results where relevant.
5. Mandatory-control failures separately from scored quality findings.
6. Repeated-trial results, uncertainty, grader agreement, and evidence gaps where relevant.
7. The decision supported by the evidence and the smallest next actions needed to close gaps.

Do not claim behavioral reliability unless execution evidence supports it. Label inspection-only conclusions as static analysis.
