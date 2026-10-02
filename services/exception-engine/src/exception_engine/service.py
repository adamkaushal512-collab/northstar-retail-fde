from dataclasses import dataclass
from enum import Enum
import logging
from pathlib import Path
from time import perf_counter
from typing import Any
from uuid import uuid4

from .config import ServiceConfig
from .observability import MetricsSnapshot, ServiceMetrics, log_event
from .persistence import SQLiteEventRegistry, SQLiteExceptionRepository
from .processor import ExceptionProcessor
from .prototype import PrototypeInputError, detection_input_from_payload, serialize_outcome


class ServiceErrorCode(Enum):
    INVALID_INPUT = "invalid_input"
    INTERNAL_ERROR = "internal_error"


@dataclass(frozen=True)
class ServiceResponse:
    status_code: int
    body: dict[str, Any]


class ExceptionEngineService:
    """Production-oriented application boundary around exception processing."""

    def __init__(
        self,
        config: ServiceConfig,
        *,
        metrics: ServiceMetrics | None = None,
        logger: logging.Logger | None = None,
    ) -> None:
        config.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._registry = SQLiteEventRegistry(config.database_path)
        self._repository = SQLiteExceptionRepository(config.database_path)
        self._processor = ExceptionProcessor(
            self._registry,
            freshness_threshold=config.freshness_threshold,
        )
        self._metrics = metrics or ServiceMetrics()
        self._logger = logger or logging.getLogger("exception_engine.service")

    def process(self, payload: dict[str, Any], correlation_id: str | None = None) -> ServiceResponse:
        started = perf_counter()
        request_id = correlation_id or str(uuid4())
        observation_event_id = _observation_event_id(payload)
        try:
            evidence = detection_input_from_payload(payload)
            outcome = self._processor.process(evidence)
            if outcome.exception is not None:
                self._repository.save(outcome.exception)
            body = serialize_outcome(outcome)
            elapsed = perf_counter() - started
            self._metrics.record(outcome.result.value, elapsed)
            log_event(
                self._logger,
                "exception_processing_completed",
                correlation_id=request_id,
                observation_event_id=evidence.observation_event_id,
                result=outcome.result.value,
                elapsed_seconds=round(elapsed, 6),
            )
            return ServiceResponse(status_code=200, body=body)
        except PrototypeInputError as exc:
            elapsed = perf_counter() - started
            self._metrics.record(ServiceErrorCode.INVALID_INPUT.value, elapsed)
            log_event(
                self._logger,
                "exception_processing_rejected",
                correlation_id=request_id,
                observation_event_id=observation_event_id,
                error_code=ServiceErrorCode.INVALID_INPUT.value,
                elapsed_seconds=round(elapsed, 6),
            )
            return ServiceResponse(
                status_code=400,
                body={"error": {"code": ServiceErrorCode.INVALID_INPUT.value, "message": str(exc)}},
            )
        except Exception:
            elapsed = perf_counter() - started
            self._metrics.record(ServiceErrorCode.INTERNAL_ERROR.value, elapsed)
            self._logger.exception(
                "exception processing failed",
                extra={"correlation_id": request_id, "observation_event_id": observation_event_id},
            )
            return ServiceResponse(
                status_code=500,
                body={"error": {"code": ServiceErrorCode.INTERNAL_ERROR.value, "message": "exception processing failed"}},
            )

    def get_exception(self, observation_event_id: str) -> dict[str, object] | None:
        return self._repository.get_by_event_id(observation_event_id)

    def metrics_snapshot(self) -> MetricsSnapshot:
        return self._metrics.snapshot()

    def health(self) -> ServiceResponse:
        return ServiceResponse(status_code=200, body={"status": "ok"})

    def readiness(self) -> ServiceResponse:
        try:
            self._repository.get_by_event_id("__readiness_probe__")
            return ServiceResponse(status_code=200, body={"status": "ready"})
        except Exception:
            return ServiceResponse(status_code=503, body={"status": "not_ready"})


def _observation_event_id(payload: dict[str, Any]) -> str | None:
    observation = payload.get("store_observation")
    if not isinstance(observation, dict):
        return None
    value = observation.get("observation_event_id")
    return value if isinstance(value, str) else None
