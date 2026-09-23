# INVENTORY_NOT_FOUND — Exception Detection Specification

## Purpose

This specification defines when NorthStar Retail should create an `INVENTORY_NOT_FOUND` operational exception for the Phase 1 BOPIS inventory discrepancy use case.

The exception represents a situation where the inventory system reports sufficient product availability to fulfill a BOPIS order, but store staff physically observe insufficient quantity to fulfill the order.

The purpose of the exception is to initiate investigation and resolution without automatically changing inventory, cancelling the customer order, or assuming which source of information is incorrect.

## Detection Rule

Create an `INVENTORY_NOT_FOUND` exception when all of the following conditions are true:

1. The order uses `BOPIS` fulfillment.
2. The order requires a specific quantity of the product.
3. The inventory system reports `available_quantity >= required_quantity`.
4. A physical store observation is available.
5. The store reports `observed_quantity < required_quantity`.

### Rule Expression

IF
    fulfillment_type = "BOPIS"
AND available_quantity >= required_quantity
AND observed_quantity IS PRESENT
AND observed_quantity < required_quantity
THEN
    create INVENTORY_NOT_FOUND

## Duplicate Event Handling

The exception engine must be idempotent. If the same triggering observation event is delivered multiple times because of retries or duplicate messages, NorthStar must create only one `INVENTORY_NOT_FOUND` exception.

Each observation event should include a unique event identifier that can be used to determine whether the event has already been processed.

Duplicate events may be recorded for operational troubleshooting, but they must not create duplicate operational exceptions.

## Stale Inventory Evidence

Stale inventory data must not prevent creation of an `INVENTORY_NOT_FOUND` exception when the detection conditions are otherwise satisfied.

The exception should preserve the inventory source timestamp and ingestion timestamp so investigators can determine the age of the inventory evidence.

If the inventory record exceeds the configured freshness threshold, the evidence should be marked as stale.

Staleness must not automatically be treated as the root cause of the discrepancy. It is supporting evidence that may assist investigation.

## Non-Actions

Creation of an `INVENTORY_NOT_FOUND` exception must not automatically:

- Cancel the customer order.
- Change the inventory quantity.
- Release or modify the inventory reservation.
- Issue a refund.
- Assume the inventory system is incorrect.
- Assume the store employee observation is incorrect.
- Treat stale inventory data as the confirmed root cause.

These actions require separate business workflows, policies, or authorized human decisions.

## Evidence Captured

When an `INVENTORY_NOT_FOUND` exception is created, the exception record should preserve or reference the following evidence:

- Canonical order identifier.
- Canonical store identifier.
- Canonical product identifier.
- Required order quantity.
- Inventory-reported available quantity.
- Store-observed quantity.
- Inventory source system.
- Inventory source update timestamp.
- Inventory ingestion timestamp.
- Observation event identifier.
- Observation timestamp.
- Exception detection timestamp.
- Inventory freshness or stale-data indicator.

This evidence provides the context required for investigation, reconciliation, auditability, and future root-cause analysis.
