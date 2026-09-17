# NorthStar Retail — Canonical Data Model

## Phase 1 Use Case

Inventory / BOPIS discrepancy

## 1. Store

The canonical Store entity represents a physical NorthStar retail location.

### Attributes

| Field | Description |
|---|---|
| store_id | Internal canonical identifier |
| store_number | Human-facing store number |
| name | Store name |
| region_id | Regional organization identifier |
| timezone | Store-local timezone |
| address | Physical store address |
| status | Store operational status |

### External Identifiers

A store may have different identifiers across enterprise systems.

| System | Example Identifier |
|---|---|
| OMS | 042 |
| Inventory | STORE-042 |
| POS | 42 |

The canonical `store_id` will provide a stable internal identity while preserving external system identifiers for integration and reconciliation.
