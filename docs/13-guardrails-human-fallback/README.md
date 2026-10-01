# Phase 13 — Guardrails + Human Fallback

## Purpose

Phase 13 converts the concrete findings from Phase 12 into enforceable controls. The copilot remains advisory: it may organize evidence, retrieve approved policy, and recommend investigation steps, but it cannot execute consequential operational actions.

## Remediations

### Evidence identity validation

Store-observation `store_id` and `product_id` must match the order/inventory evidence before detection or investigation proceeds. Mismatched evidence is rejected instead of silently combined.

### Quantity validation

Required, available, and observed quantities must be integer values greater than or equal to zero. Impossible negative quantities fail validation and enter the safe fallback path.

### Approved-policy enforcement

Policy metadata now carries `status`. Retrieval filters the corpus to `APPROVED` sections only. Draft, unapproved, or unspecified policy content cannot become authoritative policy evidence.

## Human-control boundary

The guardrail layer classifies consequential actions such as inventory adjustment, order cancellation, reservation changes, refunds, and policy overrides as `human_approval_required`. The software does not execute them.

Normal investigation assistance is `human_review`. Invalid evidence or a workflow with no operational exception produces `safe_fallback`.

```text
Evidence / exception
       |
       v
Validation + approved-policy retrieval
       |
       v
Investigation assistance
       |
       v
Guardrail decision
   /        |         \
review   approval    fallback
   |         |          |
   +---------+----------+
             v
      Authorized human
```

## Safe fallback

Fallback is explicit rather than an AI guess. Invalid/mismatched evidence returns a reason explaining which validation failed. If no exception exists, the workflow returns to the governed operational path rather than manufacturing an investigation.

## Phase boundary

This phase implements application-level controls for the current offline prototype. Authentication/RBAC infrastructure, durable approval workflows, production policy stores, model-provider controls, and distributed enforcement belong to later production phases.
