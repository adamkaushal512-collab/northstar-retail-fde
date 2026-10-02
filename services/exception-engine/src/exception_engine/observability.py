import json
import logging
from dataclasses import dataclass
from threading import Lock
from typing import Any


@dataclass(frozen=True)
class MetricsSnapshot:
    processed_events: int
    detected_exceptions: int
    duplicate_events: int
    no_exception_events: int
    invalid_inputs: int
    internal_errors: int
    total_processing_seconds: float

    @property
    def average_processing_seconds(self) -> float:
        return 0.0 if self.processed_events == 0 else self.total_processing_seconds / self.processed_events


class ServiceMetrics:
    """Small in-process metrics collector behind a replaceable interface."""

    def __init__(self) -> None:
        self._lock = Lock()
        self._counts = {
            "processed_events": 0,
            "detected_exceptions": 0,
            "duplicate_events": 0,
            "no_exception_events": 0,
            "invalid_inputs": 0,
            "internal_errors": 0,
        }
        self._total_processing_seconds = 0.0

    def record(self, outcome: str, elapsed_seconds: float) -> None:
        with self._lock:
            self._counts["processed_events"] += 1
            self._total_processing_seconds += elapsed_seconds
            mapping = {
                "exception_detected": "detected_exceptions",
                "duplicate_event": "duplicate_events",
                "no_exception": "no_exception_events",
                "invalid_input": "invalid_inputs",
                "internal_error": "internal_errors",
            }
            key = mapping.get(outcome)
            if key:
                self._counts[key] += 1

    def snapshot(self) -> MetricsSnapshot:
        with self._lock:
            return MetricsSnapshot(**self._counts, total_processing_seconds=self._total_processing_seconds)


def log_event(logger: logging.Logger, event: str, **fields: Any) -> None:
    """Emit one machine-readable JSON log record."""
    payload = {"event": event, **fields}
    logger.info(json.dumps(payload, sort_keys=True, default=str))
