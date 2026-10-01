from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from .config import ServiceConfig
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

    def __init__(self, config: ServiceConfig) -> None:
        config.database_path.parent.mkdir(parents=True, exist_ok=True)
        self._registry = SQLiteEventRegistry(config.database_path)
        self._repository = SQLiteExceptionRepository(config.database_path)
        self._processor = ExceptionProcessor(
            self._registry,
            freshness_threshold=config.freshness_threshold,
        )

    def process(self, payload: dict[str, Any]) -> ServiceResponse:
        try:
            evidence = detection_input_from_payload(payload)
            outcome = self._processor.process(evidence)
            if outcome.exception is not None:
                self._repository.save(outcome.exception)
            return ServiceResponse(status_code=200, body=serialize_outcome(outcome))
        except PrototypeInputError as exc:
            return ServiceResponse(
                status_code=400,
                body={
                    "error": {
                        "code": ServiceErrorCode.INVALID_INPUT.value,
                        "message": str(exc),
                    }
                },
            )
        except Exception:
            return ServiceResponse(
                status_code=500,
                body={
                    "error": {
                        "code": ServiceErrorCode.INTERNAL_ERROR.value,
                        "message": "exception processing failed",
                    }
                },
            )

    def get_exception(self, observation_event_id: str) -> dict[str, object] | None:
        return self._repository.get_by_event_id(observation_event_id)
