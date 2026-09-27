# NorthStar Retail — BOPIS Inventory Discrepancy Workflow

## Purpose

This document maps the current-state and target-state workflow for the initial BOPIS inventory discrepancy use case.

## Current-State Workflow

### 1. Customer places a BOPIS order

The OMS accepts a customer order for store pickup. Fulfillment depends on inventory information indicating that the requested product and quantity are available at the selected store.

### 2. Store receives the fulfillment task

A store associate receives the order and attempts to pick the requested product.

### 3. Associate searches for the product

The associate may search:

- the expected sales-floor location;
- back stock;
- returns or recently processed merchandise; and
- other store locations or operational sources as appropriate.

### 4. Physical quantity does not match system availability

The associate cannot physically locate enough units even though the inventory system reports sufficient available quantity.

This is the key operational discrepancy addressed by the first NorthStar use case.

### 5. Associate or manager investigates

The employee may review information from systems such as:

- OMS
- inventory
- POS
- returns
- product information
- warehouse or fulfillment systems

The employee may also need assistance from a store manager.

### 6. Resolution is determined

Depending on the evidence and applicable policy, employees may locate the product, wait for additional information, escalate the issue, source the item through another permitted workflow, or cancel/reorder when authorized.

### 7. Customer is updated

The customer may receive an email, text message, phone call, or other status update depending on the outcome.

### 8. Operational systems are updated

Authorized employees update relevant systems and records according to policy.

## Current-State Pain Points

The current process can be slow because evidence is fragmented across systems and physical store activity. Important problems include:

- inventory data may not reflect current physical reality;
- employees must manually reconstruct the case;
- managers may not be immediately available;
- source timestamps and system lineage may be difficult to compare;
- investigation steps may vary by employee or store;
- the reason for a decision may not be captured consistently.

## Target-State NorthStar Workflow

The target workflow introduces a deterministic exception layer before any AI assistance.

```text
BOPIS order + inventory evidence + store observation
                         |
                         v
              Canonical evidence model
                         |
                         v
           Deterministic exception engine
                         |
                         v
              INVENTORY_NOT_FOUND
                         |
                         v
             Operational exception record
                         |
                         v
              Investigation workflow
                         |
              +----------+----------+
              |                     |
              v                     v
       Human investigation     AI assistance later
              |                     |
              +----------+----------+
                         |
                         v
              Authorized human action
                         |
                         v
                 Audit / outcome
```

## Detection Boundary

NorthStar creates the initial `INVENTORY_NOT_FOUND` exception only when the documented deterministic rule is satisfied.

Physical observation is required. Stale inventory does not prevent detection; instead, freshness is retained as evidence for investigation.

## Human Decision Boundary

Detection is not the same as resolution.

Creating an exception does not authorize NorthStar to:

- modify inventory;
- cancel an order;
- change a reservation;
- issue a refund; or
- declare a root cause.

Those actions remain governed by operational policy and authorized human workflows.

## Future AI Role

A later Investigation Copilot may help:

- gather permitted evidence;
- summarize the exception;
- highlight conflicting or stale information;
- identify plausible explanations supported by evidence; and
- suggest permitted next steps.

The AI layer will operate after deterministic detection and will not replace the authoritative enterprise systems or human approval requirements.
