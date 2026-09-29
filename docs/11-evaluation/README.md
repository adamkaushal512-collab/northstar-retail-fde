# Phase 11 — Evaluation

## Purpose

Phase 11 establishes a reproducible evaluation baseline for the NorthStar Retail investigation workflow. The goal is to measure behavior, not merely confirm that code executes.

## Current System Under Evaluation

The current Phase 10 copilot is an offline deterministic investigation baseline with lexical policy retrieval. It does not yet call an external LLM. Therefore this phase does **not** claim to measure live-model hallucination, semantic reasoning quality, or model latency.

The baseline is valuable because a future LLM-backed copilot can be compared against known expected behavior without weakening deterministic detection, evidence grounding, policy use, or human-control boundaries.

## Evaluation Dimensions

The initial suite evaluates:

- deterministic exception outcome correctness;
- inventory-versus-observation conflict detection;
- missing inventory-movement evidence handling;
- correct stale-versus-fresh evidence treatment;
- presence of approved policy references;
- suppression of investigation when no exception exists; and
- a basic unsupported-claim safety check.

## Dataset

Evaluation cases live in:

`data/evals/investigation-eval-cases.json`

The initial scenarios cover:

1. stale inventory with recent movements;
2. stale inventory with missing movements;
3. fresh inventory with a physical discrepancy; and
4. a no-discrepancy control case.

The cases are derived from the canonical BOPIS example and change only the evidence needed to exercise a specific behavior.

## Evaluation Harness

`services/exception-engine/src/exception_engine/evaluation.py` applies scenario overrides, runs the same Phase 10 agent path used by the prototype, and compares structured output with explicit expectations.

The report includes total cases, passed cases, pass rate, and per-case checks.

## Baseline Result

For the current deterministic/lexical implementation, all four initial evaluation scenarios pass their expected checks. This is a development baseline, not evidence of production readiness or a claim of real-world model accuracy.

## Limitations

The current evaluation set is intentionally small and synthetic. It does not establish production performance across stores, products, policies, noisy enterprise data, adversarial inputs, or live LLM outputs.

When a live model is introduced, the evaluation suite should expand to measure:

- grounded-claim precision;
- citation/evidence correctness;
- policy retrieval relevance;
- unsupported-claim rate;
- recommendation quality;
- consistency across repeated runs;
- refusal/abstention behavior when evidence is insufficient;
- latency and token/cost characteristics; and
- human reviewer acceptance and correction rates.

Red-team and adversarial safety testing remain Phase 12 rather than being conflated with this baseline evaluation phase.

## Run the Evaluation

From `services/exception-engine`:

```bash
PYTHONPATH=src python -m exception_engine.evaluation_cli \
  --cases ../../data/evals/investigation-eval-cases.json \
  --payload ../../data/examples/bopis-inventory-discrepancy.json \
  --policy ../../data/policies/bopis-inventory-investigation.md
```

The command exits successfully only when all configured evaluation cases pass.
