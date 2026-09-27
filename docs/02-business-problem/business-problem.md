# NorthStar Retail — BOPIS Inventory Discrepancy Business Problem

## Purpose

NorthStar Retail needs a reliable operational workflow for BOPIS (Buy Online, Pick Up In Store) orders when enterprise inventory data indicates that sufficient inventory is available but store personnel cannot physically locate enough units to fulfill the order.

This document defines the business problem addressed by the initial NorthStar Retail FDE use case.

## Current-State Problem

A customer can place a BOPIS order because the order and inventory systems indicate that the selected store has sufficient inventory. During fulfillment, however, an associate may be unable to locate the required quantity on the sales floor, in back stock, in returns, or in other expected store locations.

The resulting discrepancy is operationally expensive because employees must investigate information across multiple systems and physical store processes before deciding what to do next.

Relevant systems may include:

- Order Management System (OMS)
- Inventory system
- Point of Sale (POS)
- Product catalog
- Returns processes
- Warehouse or fulfillment systems
- Store-level operational observations

The inventory record alone is not sufficient evidence that the product is physically available. Conversely, a failed physical search does not by itself prove the root cause of the discrepancy.

## Affected Users

The problem affects several groups:

- Store associates attempting to fulfill BOPIS orders
- Store managers responsible for exception resolution
- Regional or operations managers monitoring store performance
- Customers waiting for pickup confirmation or resolution

## Current Operational Impact

When an item cannot be located, employees may need to:

1. Search the sales floor and back stock.
2. Review inventory and order information.
3. Check returns, recent orders, or other operational evidence.
4. Contact or escalate to a manager.
5. Determine whether the order can still be fulfilled.
6. Update operational systems as permitted.
7. Communicate a delay, alternative, or cancellation to the customer.

Resolution can be immediate or can take hours depending on the discrepancy and the availability of employees and system information. The issue occurs a few times per week in the initial problem framing and can become more significant during peak sales and holiday periods.

## Business Consequences

The fragmented investigation process can lead to:

- Longer BOPIS fulfillment and exception-resolution times
- Customer delays and uncertainty
- Order cancellations
- Repeated manual investigation
- Inconsistent handling across stores
- Poor visibility into why discrepancies occur
- Weak auditability of operational decisions
- Customer dissatisfaction and potential customer loss

## Root-Cause Uncertainty

Potential contributing factors may include stale inventory data, misplaced merchandise, returns not yet reflected in inventory, reservation timing, transaction timing, process failures, or other system and store conditions.

NorthStar must not assume a root cause merely because an inventory discrepancy was detected. The platform must preserve the available evidence and distinguish observed facts from later investigation conclusions.

## Initial Business Objective

The initial objective is to reduce customer impact from BOPIS inventory discrepancies by detecting operational exceptions consistently, preserving the evidence required for investigation, and enabling faster and more auditable resolution.

The platform should help employees reconstruct what happened without automatically making unsupported operational decisions.

## Initial Use Case

The first prioritized exception is `INVENTORY_NOT_FOUND`.

The condition represents a BOPIS order where:

- the inventory system reports enough available quantity to satisfy the order;
- a physical store observation is available; and
- the observed quantity is lower than the quantity required by the order.

The detailed deterministic rule is maintained in:

`docs/06-exception-detection/inventory-not-found.md`

## Non-Goals for the Initial Use Case

The initial system does not autonomously:

- cancel customer orders;
- change inventory quantities;
- change reservations;
- issue refunds;
- assert an unsupported root cause; or
- allow an AI component to make irreversible operational decisions.

These actions require later workflow, authorization, governance, and human-control design.
