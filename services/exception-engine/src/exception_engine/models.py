from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class DetectionInput:
    order_id: str
    store_id: str
    product_id: str
    fulfillment_type: str
    required_quantity: int
    available_quantity: int
    observed_quantity: int | None
    inventory_source_updated_at: datetime
    inventory_ingested_at: datetime
    observation_event_id: str
    observation_timestamp: datetime

@dataclass(frozen=True)
class OperationalException:
    exception_type: str
    order_id: str
    store_id: str
    product_id: str
    required_quantity: int
    available_quantity: int
    observed_quantity: int | None
    inventory_source_updated_at: datetime
    inventory_ingested_at: datetime
    observation_event_id: str
    observation_timestamp: datetime
    detected_at: datetime
    inventory_is_stale: bool
