# NorthStar Retail — System Landscape

## Phase 1 Use Case

Inventory / BOPIS discrepancy

A customer places a BOPIS order for an item that the inventory system reports as available, but the store cannot physically locate the item.

## Systems in Scope

| System | Primary Responsibility | Relevant Data |
|---|---|---|
| OMS | Customer orders and fulfillment | Order ID, SKU, quantity, store, fulfillment status, pickup status |
| Inventory Management | Inventory position | SKU, store, on-hand, reserved, available, adjustments, transfers |
| POS | Store transactions | Sales, returns, voids, transaction timestamps |
| Store Master | Enterprise store identity | Store ID, location, region, timezone |
| Product Catalog | Product identity | SKU, UPC, product ID, product attributes |
| IT Service Management | Operational incidents | Incident ID, system, severity, status, resolution |
| Workforce Management | Store staffing context | Store, employee, schedule, staffing status |

## Current-State Characteristics

NorthStar has a heterogeneous enterprise environment.

Different systems may use different integration patterns, including:

- REST APIs
- Event-based integrations
- Scheduled file transfers
- Legacy database integrations

The systems may experience:

- Delayed updates
- Duplicate events
- Missing or failed messages
- Temporary system unavailability
- Different store identifiers
- Different SKU representations
- Timestamp and timezone differences

## Phase 1 Investigation Flow

1. OMS identifies the BOPIS order and fulfillment requirement.
2. Inventory Management reports the item as available.
3. Associate searches for the item and cannot locate it.
4. Store manager investigates inventory and order information.
5. POS history is reviewed for recent sales, returns, or voids.
6. Additional inventory movements may be investigated.
7. The manager determines the appropriate operational action.
8. The customer is notified if the order cannot be fulfilled.

## Key Discovery Finding

The primary problem is not simply that one system contains incorrect information.

The operational problem is that store teams must manually correlate information across multiple enterprise systems to determine whether an order can be fulfilled.

## Design Constraints

Any future solution must account for:

- Existing enterprise systems cannot all be modified.
- Store users require simple workflows.
- Access must follow existing organizational permissions.
- Operational actions require auditability.
- Temporary system failures must not make the solution unusable.
- Duplicate and delayed data must be handled safely.
- Production rollout should begin with a controlled pilot.
