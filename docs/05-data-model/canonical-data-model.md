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

## 4. Inventory Position

The canonical Inventory Position entity represents the inventory state of a product at a specific NorthStar store.

### Attributes

| Field | Description |
|---|---|
| inventory_position_id | Internal canonical inventory position identifier |
| store_id | Canonical store identifier |
| product_id | Canonical product identifier |
| on_hand_quantity | Quantity the inventory system reports physically on hand |
| reserved_quantity | Quantity reserved for customer orders |
| allocated_quantity | Quantity allocated for fulfillment |
| available_quantity | Quantity currently reported as available |
| damaged_quantity | Quantity unavailable because it is damaged or held |
| source_system | System that supplied the inventory state |
| source_updated_at | Timestamp when the source system last updated the inventory record |
| ingested_at | Timestamp when NorthStar integration received the record |

### Phase 1 Relevance

Inventory Position connects a product to a store and captures what the inventory system currently believes is available.

For the Phase 1 BOPIS discrepancy, this allows the system to identify situations where inventory reports available quantity but the store cannot locate the product.

The source and ingestion timestamps are preserved so the investigation workflow can determine whether stale or delayed inventory data may have contributed to the discrepancy.
