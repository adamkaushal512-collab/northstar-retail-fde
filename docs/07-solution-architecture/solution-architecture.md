# NorthStar Retail — Solution Architecture

## Purpose

This document defines the target architecture for the NorthStar Retail BOPIS inventory discrepancy platform.

The architecture separates authoritative enterprise systems, canonical evidence, deterministic exception detection, operational workflow, and later AI assistance.

## Architecture Principles

1. Enterprise source systems remain authoritative for their respective domains.
2. NorthStar normalizes evidence into canonical models rather than tightly coupling business logic to source-specific identifiers.
3. Deterministic rules detect the initial operational exception.
4. Source lineage and timestamps are preserved for auditability.
5. AI is an investigation aid, not the authoritative detector or transaction system.
6. Irreversible operational actions require explicit authorization and appropriate human control.
7. Components should be reusable for future exception types.

## Logical Architecture

```text
+-------------------------------------------------------------+
|                  Enterprise Source Systems                  |
|                                                             |
|   OMS      Inventory      POS      Product/Store      Other |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                 Integration / Ingestion Layer               |
|  adapters | validation | identity mapping | timestamps      |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                    Canonical Data Layer                     |
|  Order | Store | Product | Inventory | Observation | etc.  |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|              Deterministic Exception Engine                 |
|  detection rules | freshness | idempotency | evidence       |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                  Operational Exception                      |
| INVENTORY_NOT_FOUND + evidence + lineage + timestamps       |
+------------------------------+------------------------------+
                               |
                               v
+-------------------------------------------------------------+
|                 Investigation / Workflow Layer              |
| case state | permitted actions | escalation | audit         |
+----------------------+----------------------+---------------+
                       |                      |
                       v                      v
              Human investigation     AI Investigation Copilot
                       |                      |
                       +----------+-----------+
                                  |
                                  v
+-------------------------------------------------------------+
|             Authorized Operational Resolution               |
| human/policy-controlled action + outcome + audit trail       |
+-------------------------------------------------------------+
```

## Source Systems

Initial system discovery includes enterprise systems such as:

- OMS
- inventory system
- POS
- product catalog
- store/master data
- returns
- warehouse or fulfillment systems

Not every source must be integrated into the first prototype. Integrations should be added according to the evidence required by the prioritized workflow.

## Canonical Data Layer

The canonical model provides stable NorthStar identities while preserving external identifiers needed for reconciliation.

The model is documented in:

`docs/05-data-model/canonical-data-model.md`

This layer prevents detection logic from depending directly on inconsistent source-system identifier formats.

## Exception Engine

The exception engine is deterministic.

For the first use case it is responsible for:

- accepting canonical detection evidence;
- enforcing the `INVENTORY_NOT_FOUND` rule;
- requiring physical observation;
- suppressing duplicate observation events;
- evaluating inventory freshness;
- preserving evidence and source lineage; and
- creating an `OperationalException`.

The detailed rule is documented in:

`docs/06-exception-detection/inventory-not-found.md`

## Persistence

The current prototype uses an in-memory event registry for idempotency. This is intentionally not considered production-grade.

A production implementation should use durable persistence and enforce appropriate uniqueness/idempotency guarantees so that behavior remains correct across restarts and multiple service instances.

## API / Event Boundary

The architecture should support evidence arriving through an explicit service or event boundary rather than allowing source-specific business logic to spread through the exception engine.

Detailed API/event contracts will be defined during continued prototype and production-engineering work.

## AI Investigation Copilot

AI is introduced only after deterministic exception creation.

Permitted future responsibilities include:

- retrieving approved evidence;
- summarizing the case;
- identifying conflicts or missing information;
- explaining plausible causes when supported by evidence;
- citing the evidence used; and
- suggesting permitted next steps.

The AI component must not be treated as an authoritative inventory source.

## Human-Control Boundary

The initial architecture does not permit AI or the detector to autonomously:

- modify inventory;
- cancel an order;
- change a reservation;
- issue a refund; or
- make another irreversible customer-impacting transaction.

These actions require policy enforcement, authorization, and appropriate human approval.

## Observability

Production evolution should include:

- structured logs;
- correlation identifiers;
- exception-processing metrics;
- latency and failure metrics;
- audit events; and
- distributed tracing where appropriate.

## Evolution Path

The architecture is intentionally staged:

1. deterministic exception foundation;
2. durable persistence and service/event interfaces;
3. investigation workflow;
4. controlled AI assistance;
5. evaluation and guardrails;
6. production engineering and observability;
7. pilot and business measurement.

This sequencing allows AI to build on an auditable enterprise foundation instead of replacing it.
