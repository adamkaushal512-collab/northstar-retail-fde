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

## 2. Product

The canonical Product entity represents a NorthStar product and provides a stable identity across enterprise systems.

### Attributes

| Field | Description |
|---|---|
| product_id | Internal canonical product identifier |
| sku | NorthStar SKU |
| upc | Universal Product Code when available |
| name | Product name |
| status | Product lifecycle status |

### External Identifiers

A product may have different identifiers across enterprise systems.

| System | Example Identifier |
|---|---|
| OMS | 98765 |
| Inventory | SKU-98765 |
| POS | 008123456789 |
| Product Catalog | PROD-5542 |

The canonical `product_id` provides a stable internal identity while preserving source-system identifiers for integration and reconciliation.

## 3. Order

The canonical Order entity represents a customer order and its fulfillment state across NorthStar enterprise systems.

### Attributes

| Field | Description |
|---|---|
| order_id | Internal canonical order identifier |
| external_order_id | Source-system order identifier |
| store_id | Canonical store fulfilling the order |
| order_status | Overall order status |
| fulfillment_type | Fulfillment method, such as BOPIS |
| promised_pickup_at | Expected customer pickup time |
| created_at | Order creation timestamp |
| updated_at | Last known order update timestamp |

### Order Items

Each order contains one or more products.

| Field | Description |
|---|---|
| product_id | Canonical product identifier |
| quantity | Quantity ordered |
| fulfillment_status | Current item fulfillment status |
| reserved_quantity | Quantity reserved for the order |

### External Identifiers

The same order may have different identifiers or representations across enterprise systems.

| System | Example Identifier |
|---|---|
| OMS | ORD-100045 |
| Store Systems | 100045 |
| Customer Service | CASE-78421 |

The canonical `order_id` provides a stable internal identity while preserving source-system identifiers for integration and reconciliation.

### Phase 1 Relevance

The Order entity allows the exception workflow to connect:

- The customer order
- The fulfillment store
- The requested product
- The quantity required
- The promised pickup time
- The current fulfillment state

This information will later be correlated with inventory and transaction data to determine why a BOPIS order cannot be fulfilled.
