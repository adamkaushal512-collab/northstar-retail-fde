from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from enum import Enum

from .detector import should_create_inventory_not_found
from .freshness import is_inventory_stale
from .idempotency import InMemoryEventRegistry
from .models import DetectionInput, OperationalException


class ProcessingResult(Enum):
    EXCEPTION_DETECTED = "exception_detected"
    NO_EXCEPTION = "no_exception"
    DUPLICATE_EVENT = "duplicate_event"


@dataclass(frozen=True)
class ProcessingOutcome:
    result: ProcessingResult
    exception: OperationalException | None = None


class ExceptionProcessor:
    def __init__(
        self,
        event_registry: InMemoryEventRegistry,
        freshness_threshold: timedelta = timedelta(minutes=30),
    ) -> None:
        self._event_registry = event_registry
        self._freshness_threshold = freshness_threshold

    def process(self, evidence: DetectionInput) -> ProcessingOutcome:
        if not self._event_registry.register(evidence.observation_event_id):
            return ProcessingOutcome(
                result=ProcessingResult.DUPLICATE_EVENT,
            )

        if not should_create_inventory_not_found(evidence):
            return ProcessingOutcome(
                result=ProcessingResult.NO_EXCEPTION,
            )

        inventory_is_stale = is_inventory_stale(
            inventory_source_updated_at=evidence.inventory_source_updated_at,
            observation_timestamp=evidence.observation_timestamp,
            freshness_threshold=self._freshness_threshold,
        )

        exception = OperationalException(
            exception_type="INVENTORY_NOT_FOUND",
            order_id=evidence.order_id,
            store_id=evidence.store_id,
            product_id=evidence.product_id,
            required_quantity=evidence.required_quantity,
            available_quantity=evidence.available_quantity,
            observed_quantity=evidence.observed_quantity,
            inventory_source_updated_at=evidence.inventory_source_updated_at,
            inventory_ingested_at=evidence.inventory_ingested_at,
            observation_event_id=evidence.observation_event_id,
            observation_timestamp=evidence.observation_timestamp,
            detected_at=datetime.now(timezone.utc),
            inventory_is_stale=inventory_is_stale,
        )

        return ProcessingOutcome(
            result=ProcessingResult.EXCEPTION_DETECTED,
            exception=exception,
        )
