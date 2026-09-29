# BOPIS Inventory Investigation Policy

policy_id: BOPIS-INV-001
version: 1.0
effective_date: 2026-09-01
status: APPROVED

## Inventory discrepancy investigation

When a BOPIS item cannot be located even though system inventory indicates sufficient available quantity, preserve the store observation and inventory timestamps before resolution. Review recent inventory movements and confirm that the order, product, and store identifiers refer to the same fulfillment attempt.

## Stale inventory

Inventory older than the configured freshness threshold should be identified as stale evidence. Staleness may justify retrieving a newer inventory record, but it does not by itself establish the cause of the discrepancy.

## Human action

The investigation assistant may summarize evidence and recommend checks. Inventory adjustments, order cancellation, reservation changes, refunds, and policy overrides require the applicable authorized human workflow.
