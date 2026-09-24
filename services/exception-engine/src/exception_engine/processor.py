from enum import Enum
from .detector import should_create_inventory_not_found
from .idempotency import InMemoryEventRegistry
from .models import DetectionInput


class ProcessingResult(Enum):
    EXCEPTION_DETECTED = "exception_detected"
    NO_EXCEPTION = "no_exception"
    DUPLICATE_EVENT = "duplicate_event"


class ExceptionProcessor:
    def __init__(self, event_registry: InMemoryEventRegistry) -> None:
        self._event_registry = event_registry

    def process(self, evidence: DetectionInput) -> ProcessingResult:
        if not self._event_registry.register(evidence.observation_event_id):
            return ProcessingResult.DUPLICATE_EVENT

        if should_create_inventory_not_found(evidence):
            return ProcessingResult.EXCEPTION_DETECTED

        return ProcessingResult.NO_EXCEPTION
