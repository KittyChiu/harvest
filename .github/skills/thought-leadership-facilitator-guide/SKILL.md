---
name: thought-leadership-facilitator-guide
description: Create a practical workshop facilitator guide from a canonical whitepaper, existing thought-leadership IP, or workshop transcript. Use to coach others on what an idea or framework is and how to apply it through teaching, exercises, demonstrations, debriefs, and assessment. When a whitepaper is supplied, treat it as the source of truth. This skill works independently or alongside the whitepaper and Obsidian Marp skills.
compatibility: >
  Produces a self-contained Markdown facilitator guide. No external tools are required.
---

# Thought Leadership Facilitator Guide

Turn canonical IP into a workshop another facilitator can run reliably. Focus on **what participants need to understand** and **how they will practise applying it**.

## Role in the three-asset system

| Asset | Primary job | Content emphasis |
|---|---|---|
| Whitepaper | Capture and govern the IP | Detailed why, what, how, evidence, boundaries, lineage |
| Marp deck | Present the thought leadership | Why, what, one example or demonstration |
| Facilitator guide | Teach people to apply it | What and how, exercises, reflection, assessment |

This skill can run independently from an existing IP artifact or raw transcript. When a canonical whitepaper exists, it outranks all downstream artifacts.

## Required input

The caller must provide:

1. **IP source**: canonical whitepaper, existing framework/article, transcript, pasted content, or readable file paths.
2. **Workshop brief**: audience, intended capability, duration, delivery format, and output path.

Useful optional inputs:

- participant prerequisites;
- group size;
- available tools and environment;
- required exercise or demonstration;
- accessibility or remote-delivery constraints;
- expected take-home artifact;
- relationship to an existing Marp deck.

If the IP source or intended participant capability is missing, ask one focused question.

## Source precedence

Use:

1. canonical whitepaper;
2. other explicitly approved IP;
3. raw transcript or workshop notes;
4. new facilitation design, clearly separated from canonical claims.

When a whitepaper is supplied:

- preserve its central thesis, framework, terminology, practices, and boundaries;
- use its `Downstream extraction map` as the first-pass handoff;
- use transcript material only to enrich examples, analogies, prompts, and facilitator notes;
- do not redefine or expand the IP without identifying the proposed change.

## Workflow

### 1. Extract the teachable core

Identify:

- participant problem and motivation;
- concepts they must understand;
- decisions or actions they must be able to perform;
- framework steps or principles;
- common mistakes and boundaries;
- example or demonstration;
- practice task;
- observable evidence of learning;
- durable artifact participants should take away.

Exclude whitepaper detail that does not support learning or application.

### 2. Define outcome-based learning objectives

Use observable verbs. Prefer:

- distinguish;
- diagnose;
- choose;
- construct;
- apply;
- compare;
- critique;
- validate;
- transfer.

Avoid objectives such as "know," "learn," or "be aware of" unless paired with observable evidence.

For each objective define how the facilitator will know it was achieved.

### 3. Design the learning journey

Prefer this sequence:

1. **Experience** — surface the problem through a story, prompt, or baseline attempt.
2. **Explain** — teach the minimum model required.
3. **Demonstrate** — show the framework applied to a realistic case.
4. **Practise** — participants apply it to their own or supplied work.
5. **Critique** — compare results, expose risks, and resolve ambiguity.
6. **Transfer** — create a durable artifact, commitment, or next action.

Use short teaching segments followed by active practice. Do not turn the guide into a lecture transcript.

### 4. Build a realistic agenda

Account for:

- opening and psychological setup;
- instruction;
- transitions;
- forming groups or opening tools;
- exercise work;
- report-back;
- debrief;
- breaks for sessions longer than 90 minutes;
- close and transfer.

Each agenda row must state time, activity, participant action, and outcome.

### 5. Specify every activity

For each activity include:

- purpose;
- duration;
- setup and materials;
- facilitator instructions;
- participant instructions;
- expected output;
- debrief questions;
- watch-outs;
- fallback if time, tools, or participation fail.

Instructions must be precise enough for a facilitator who did not attend the original workshop.

### 6. Add facilitator narrative

Include concise talk tracks for:

- opening framing;
- key concept explanations;
- transitions;
- demonstration setup;
- debrief synthesis;
- closing call to action.

Use stories and analogies from the source when grounded. Keep canonical exposition aligned with the whitepaper and avoid copying slide speaker notes wholesale.

### 7. Design application and assessment

Prefer authentic work over trivia. Participants should create or improve something that demonstrates the thought leadership in action.

Define:

- baseline or starting condition;
- constraints;
- steps;
- observable measures;
- comparison or critique method;
- acceptance criteria;
- take-home artifact and owner.

Use the same measures when comparing two approaches.

### 8. Write the guide

Start from [assets/facilitator-guide-template.md](assets/facilitator-guide-template.md).

The guide should include:

- purpose and workshop promise;
- audience, duration, format, prerequisites, and materials;
- learning outcomes and evidence;
- source-of-truth statement;
- agenda;
- facilitator preparation;
- teaching content;
- demonstration;
- activity instructions;
- debrief;
- watch-outs and recovery paths;
- success criteria;
- adaptations;
- follow-up and transfer.

### 9. Check alignment

Before finishing, verify:

- every learning objective appears in the agenda;
- every objective has practice or evidence;
- timings add up;
- activities have outputs and debriefs;
- terminology matches the source of truth;
- risks and boundaries are taught where participants could misuse the idea;
- the guide can stand alone without the slide deck;
- references to optional slides are helpful but not required.

## Quality bar

The guide is complete only when:

- another facilitator can run it without reconstructing intent;
- participants spend meaningful time applying the idea;
- the workshop teaches canonical what and practical how;
- activities produce observable evidence of learning;
- the whitepaper's IP is preserved without unnecessary duplication;
- participants leave with a reusable output, commitment, or next action.

## Invocation examples

> Use the thought-leadership-facilitator-guide skill. Source of truth: `Managing AI Context.md`. Create a 90-minute guide for engineers and product roles. Participants must build a RESET brief, compare overloaded and curated context, critique the result, and create one Transfer artifact. Save it as `RESET Workshop Guide.md`.

> Turn `framework-article.md` into a 60-minute remote workshop for managers. Focus on what the framework is and how to apply it to one live scenario. Include facilitator scripts, breakout instructions, debrief questions, timing, and success criteria.

