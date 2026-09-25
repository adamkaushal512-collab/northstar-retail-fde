from datetime import datetime, timezone

from exception_engine.models import OperationalException


def test_operational_exception_preserves_detection_evidence():
    inventory_source_updated_at = datetime(
        2026, 9, 25, 14, 0, tzinfo=timezone.utc
    )
    inventory_ingested_at = datetime(
        2026, 9, 25, 14, 2, tzinfo=timezone.utc
    )
    observation_timestamp = datetime(
        2026, 9, 25, 14, 45, tzinfo=timezone.utc
    )
    detected_at = datetime(
        2026, 9, 25, 14, 46, tzinfo=timezone.utc
    )

    exception = OperationalException(
        exception_type="INVENTORY_NOT_FOUND",
        order_id="order-100045",
        store_id="store-042",
        product_id="product-98765",
        required_quantity=1,
        available_quantity=2,
        observed_quantity=0,
        inventory_source_updated_at=inventory_source_updated_at,
        inventory_ingested_at=inventory_ingested_at,
        observation_event_id="observation-001",
        observation_timestamp=observation_timestamp,
        detected_at=detected_at,
        inventory_is_stale=True,
    )

    assert exception.exception_type == "INVENTORY_NOT_FOUND"
    assert exception.order_id == "order-100045"
    assert exception.store_id == "store-042"
    assert exception.product_id == "product-98765"
    assert exception.required_quantity == 1
    assert exception.available_quantity == 2
    assert exception.observed_quantity == 0
    assert exception.inventory_source_updated_at == inventory_source_updated_at
    assert exception.inventory_ingested_at == inventory_ingested_at
    assert exception.observation_event_id == "observation-001"
    assert exception.observation_timestamp == observation_timestamp
    assert exception.detected_at == detected_at
    assert exception.inventory_is_stale is True
