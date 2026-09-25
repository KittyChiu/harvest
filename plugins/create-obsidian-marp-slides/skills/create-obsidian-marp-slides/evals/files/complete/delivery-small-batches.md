---
type: Reusable Pattern
title: Small batches shorten feedback loops
description: Decide when to divide delivery work so each result can inform the next step.
tags:
  - delivery
  - publish
  - private
status: stable
sources:
  - id: delivery-learning
    resource: internal delivery learning
generated:
  by: create-atomic-note/1.1.1
  at: 2026-09-25T12:00:00Z
---

# Small batches shorten feedback loops

Parent: [Delivery](delivery-moc.md)

## Pattern

> When uncertainty can change the plan, deliver a small reviewable batch, because each result improves the next decision.

## Practice

- Define the smallest result that tests the current assumption.
- Review it before dependent work begins.

## Why it works

Each result replaces an assumption with evidence before more work is committed.

## Signals

- The plan depends on an untested assumption.
- Later work would be expensive to revise.

## Learning

Smaller review points exposed mistaken assumptions before they affected later work.

## Constraints

- Coordination costs can outweigh the benefit when work cannot be separated safely.

## Relationships

- Extension: [Review feedback changes the next decision](delivery-review-feedback.md) explains when the result must affect later work.
