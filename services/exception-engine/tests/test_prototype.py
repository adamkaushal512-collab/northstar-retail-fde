import json
from pathlib import Path

import pytest

from exception_engine.idempotency import InMemoryEventRegistry
from exception_engine.processor import ProcessingResult
from exception_engine.prototype import (
    PrototypeInputError,
    detection_input_from_payload,
    process_file,
    process_payload,
)


EXAMPLE = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "examples"
    / "bopis-inventory-discrepancy.json"
)


def _load_example():
    return json.loads(EXAMPLE.read_text(encoding="utf-8"))


def test_example_payload_maps_to_detection_input():
    evidence = detection_input_from_payload(_load_example())

    assert evidence.order_id == "order-100045"
    assert evidence.store_id == "store-042"
    assert evidence.product_id == "product-98765"
    assert evidence.required_quantity == 1
    assert evidence.available_quantity == 2
    assert evidence.observed_quantity == 0
    assert evidence.inventory_source_system == "INVENTORY"
    assert evidence.observation_event_id == "observation-001"


def test_example_file_runs_end_to_end_and_creates_exception():
    result = process_file(EXAMPLE)

    assert result["result"] == "exception_detected"
    assert result["exception"]["exception_type"] == "INVENTORY_NOT_FOUND"
    assert result["exception"]["order_id"] == "order-100045"
    assert result["exception"]["inventory_source_system"] == "INVENTORY"
    assert result["exception"]["inventory_is_stale"] is True


def test_prototype_returns_no_exception_for_sufficient_observation():
    payload = _load_example()
    payload["store_observation"]["observed_quantity"] = 1

    outcome = process_payload(payload)

    assert outcome.result is ProcessingResult.NO_EXCEPTION
    assert outcome.exception is None


def test_shared_registry_suppresses_duplicate_observation_event():
    payload = _load_example()
    registry = InMemoryEventRegistry()

    first = process_payload(payload, event_registry=registry)
    second = process_payload(payload, event_registry=registry)

    assert first.result is ProcessingResult.EXCEPTION_DETECTED
    assert second.result is ProcessingResult.DUPLICATE_EVENT
    assert second.exception is None


def test_mismatched_product_identity_is_rejected():
    payload = _load_example()
    payload["inventory_position"]["product_id"] = "different-product"

    with pytest.raises(PrototypeInputError, match="product_id values must match"):
        detection_input_from_payload(payload)


def test_timestamp_without_timezone_is_rejected():
    payload = _load_example()
    payload["store_observation"]["observed_at"] = "2026-09-22T13:45:00"

    with pytest.raises(PrototypeInputError, match="timezone offset"):
        detection_input_from_payload(payload)
