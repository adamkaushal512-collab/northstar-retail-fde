import json
from dataclasses import asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from .idempotency import InMemoryEventRegistry
from .models import DetectionInput
from .processor import ExceptionProcessor, ProcessingOutcome


class PrototypeInputError(ValueError):
    """Raised when prototype input cannot be converted to detection evidence."""


def _required(mapping: dict[str, Any], key: str, context: str) -> Any:
    if key not in mapping:
        raise PrototypeInputError(f"missing required field: {context}.{key}")
    return mapping[key]


def _parse_timestamp(value: Any, field_name: str) -> datetime:
    if not isinstance(value, str):
        raise PrototypeInputError(f"{field_name} must be an ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise PrototypeInputError(
            f"{field_name} must be an ISO-8601 timestamp"
        ) from exc
    if parsed.tzinfo is None:
        raise PrototypeInputError(f"{field_name} must include a timezone offset")
    return parsed


def detection_input_from_payload(payload: dict[str, Any]) -> DetectionInput:
    """Convert the canonical prototype payload into deterministic evidence."""
    try:
        order = _required(payload, "order", "payload")
        inventory = _required(payload, "inventory_position", "payload")
        observation = _required(payload, "store_observation", "payload")
        items = _required(order, "items", "order")
    except TypeError as exc:
        raise PrototypeInputError("payload sections must be objects") from exc

    if not isinstance(order, dict) or not isinstance(inventory, dict):
        raise PrototypeInputError("order and inventory_position must be objects")
    if not isinstance(observation, dict):
        raise PrototypeInputError("store_observation must be an object")
    if not isinstance(items, list) or len(items) != 1 or not isinstance(items[0], dict):
        raise PrototypeInputError(
            "prototype requires exactly one order item"
        )

    item = items[0]
    order_store_id = _required(order, "store_id", "order")
    inventory_store_id = _required(inventory, "store_id", "inventory_position")
    inventory_product_id = _required(
        inventory, "product_id", "inventory_position"
    )
    item_product_id = _required(item, "product_id", "order.items[0]")

    if order_store_id != inventory_store_id:
        raise PrototypeInputError("order and inventory store_id values must match")
    if item_product_id != inventory_product_id:
        raise PrototypeInputError("order item and inventory product_id values must match")

    return DetectionInput(
        order_id=_required(order, "order_id", "order"),
        store_id=order_store_id,
        product_id=item_product_id,
        fulfillment_type=_required(order, "fulfillment_type", "order"),
        required_quantity=_required(item, "quantity", "order.items[0]"),
        available_quantity=_required(
            inventory, "available_quantity", "inventory_position"
        ),
        observed_quantity=_required(
            observation, "observed_quantity", "store_observation"
        ),
        inventory_source_system=_required(
            inventory, "source_system", "inventory_position"
        ),
        inventory_source_updated_at=_parse_timestamp(
            _required(inventory, "source_updated_at", "inventory_position"),
            "inventory_position.source_updated_at",
        ),
        inventory_ingested_at=_parse_timestamp(
            _required(inventory, "ingested_at", "inventory_position"),
            "inventory_position.ingested_at",
        ),
        observation_event_id=_required(
            observation, "observation_event_id", "store_observation"
        ),
        observation_timestamp=_parse_timestamp(
            _required(observation, "observed_at", "store_observation"),
            "store_observation.observed_at",
        ),
    )


def serialize_outcome(outcome: ProcessingOutcome) -> dict[str, Any]:
    result: dict[str, Any] = {"result": outcome.result.value, "exception": None}
    if outcome.exception is not None:
        exception = asdict(outcome.exception)
        for key, value in exception.items():
            if isinstance(value, datetime):
                exception[key] = value.isoformat()
        result["exception"] = exception
    return result


def process_payload(
    payload: dict[str, Any],
    *,
    event_registry: InMemoryEventRegistry | None = None,
    freshness_threshold: timedelta = timedelta(minutes=30),
) -> ProcessingOutcome:
    evidence = detection_input_from_payload(payload)
    processor = ExceptionProcessor(
        event_registry or InMemoryEventRegistry(),
        freshness_threshold=freshness_threshold,
    )
    return processor.process(evidence)


def process_file(path: str | Path) -> dict[str, Any]:
    input_path = Path(path)
    with input_path.open(encoding="utf-8") as handle:
        payload = json.load(handle)
    return serialize_outcome(process_payload(payload))
