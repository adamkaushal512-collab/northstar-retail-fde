# NorthStar Retail — Use-Case Prioritization

## Purpose

This document records why BOPIS inventory discrepancy is the first prioritized NorthStar Retail FDE use case.

## Candidate Operational Problem Areas

Customer discovery identified a broader enterprise operations problem involving fragmented information, legacy systems, operational tickets, security constraints, and slow exception resolution.

Potential areas include order exceptions, inventory discrepancies, fulfillment problems, returns, and related store operational workflows.

NorthStar will not attempt to solve every operational problem in the first implementation.

## Prioritized Use Case

The first use case is:

**BOPIS Inventory Discrepancy — `INVENTORY_NOT_FOUND`**

A BOPIS order requires a quantity of a product, the inventory system reports sufficient available inventory, but a physical store observation reports less than the required quantity.

## Why This Use Case Was Selected

### Clear customer impact

A discrepancy can delay pickup, cause cancellation, require repeated customer communication, and contribute to customer dissatisfaction.

### Cross-system enterprise problem

Investigation requires evidence from multiple operational sources rather than a single isolated application.

### Deterministic starting point

The initial condition can be expressed as an auditable deterministic rule before introducing AI.

### Strong FDE relevance

The use case requires customer discovery, workflow analysis, enterprise integration, canonical modeling, source lineage, exception processing, security boundaries, testing, and later AI assistance.

### Expandable architecture

The same exception framework can later support additional operational exception types without redesigning the entire platform.

## Prioritization Decision

NorthStar will build and validate the deterministic BOPIS inventory discrepancy workflow first.

The first detection rule is:

```text
IF fulfillment_type == BOPIS
AND available_quantity >= required_quantity
AND observed_quantity is present
AND observed_quantity < required_quantity
THEN create INVENTORY_NOT_FOUND
```

## Required Evidence

The exception should preserve enough evidence to reconstruct the detection, including:

- canonical order identifier;
- canonical store identifier;
- canonical product identifier;
- required quantity;
- inventory-reported available quantity;
- store-observed quantity;
- inventory source system;
- inventory source update timestamp;
- inventory ingestion timestamp;
- observation event identifier;
- observation timestamp;
- exception detection timestamp; and
- inventory freshness/stale-data indicator.

## Explicit Non-Actions

Detection must not automatically:

- change inventory;
- cancel the BOPIS order;
- change reservations;
- issue a refund; or
- claim a root cause that the evidence does not establish.

## Expansion Criteria

Additional use cases should be added only after the first workflow establishes reusable patterns for canonical evidence, exception detection, idempotency, auditability, security, and operational resolution.
