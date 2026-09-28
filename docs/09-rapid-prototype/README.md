# Phase 9 — Rapid Prototype / Core Build

## Status

**Complete for the portfolio prototype scope.**

Phase 9 establishes a runnable deterministic vertical slice for the initial NorthStar Retail BOPIS inventory discrepancy use case. Production hardening, durable infrastructure, observability, AI/RAG, evaluation, and deployment remain later lifecycle phases.

## Prototype Scope

```text
canonical JSON evidence
        |
        v
input mapping + boundary validation
        |
        v
DetectionInput
        |
        v
deterministic INVENTORY_NOT_FOUND rule
        |
        +--> no exception
        |
        v
freshness evaluation + idempotency
        |
        v
OperationalException
        |
        v
JSON-serializable processing outcome
```

## Implemented Capabilities

- Canonical `DetectionInput` and `OperationalException` models
- Deterministic `INVENTORY_NOT_FOUND` detection
- Physical-observation requirement
- Inventory freshness/staleness evaluation
- Observation-event idempotency for the prototype process
- Preservation of inventory source lineage and timestamps
- Creation of an operational exception record
- Canonical JSON-to-domain input mapping
- Boundary checks for cross-system store/product identity consistency
- Timezone-aware timestamp validation at the prototype boundary
- JSON serialization of processing outcomes
- Command-line runner for an end-to-end demonstration
- Automated unit and end-to-end prototype tests

## Run the Prototype

From `services/exception-engine`:

```bash
PYTHONPATH=src python -m exception_engine ../../data/examples/bopis-inventory-discrepancy.json
```

Expected result: `exception_detected` with an `INVENTORY_NOT_FOUND` exception containing preserved evidence and an inventory-staleness indicator.

## Run Tests

```bash
PYTHONPATH=src pytest -q
```

## Intentional Prototype Limits

The following are deferred to later lifecycle phases:

- durable database/event-store persistence;
- distributed/concurrency-safe idempotency;
- production API or message-broker integration;
- enterprise authentication/RBAC enforcement;
- production observability and CI/CD;
- AI/RAG/agent investigation;
- AI evaluations and red-team testing;
- automated order cancellation, refund, reservation, or inventory mutation.

## Phase 9 Completion Criteria

Phase 9 is complete when the repository demonstrates a tested vertical slice that can accept representative canonical evidence, deterministically decide the initial use case, preserve required evidence, reject invalid boundary conditions, and produce a usable exception outcome without relying on AI.

The current prototype satisfies that scope.
