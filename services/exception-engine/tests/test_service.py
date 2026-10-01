import json
from datetime import timedelta
from pathlib import Path

from exception_engine.config import ServiceConfig
from exception_engine.service import ExceptionEngineService


ROOT = Path(__file__).resolve().parents[3]
EXAMPLE = ROOT / "data" / "examples" / "bopis-inventory-discrepancy.json"


def _payload():
    with EXAMPLE.open(encoding="utf-8") as handle:
        return json.load(handle)


def _service(tmp_path):
    return ExceptionEngineService(
        ServiceConfig(
            database_path=tmp_path / "engine.db",
            freshness_threshold=timedelta(minutes=30),
        )
    )


def test_service_persists_detected_exception(tmp_path):
    service = _service(tmp_path)
    response = service.process(_payload())
    assert response.status_code == 200
    assert response.body["result"] == "exception_detected"
    event_id = response.body["exception"]["observation_event_id"]
    persisted = service.get_exception(event_id)
    assert persisted is not None
    assert persisted["exception_type"] == "INVENTORY_NOT_FOUND"


def test_service_idempotency_survives_restart(tmp_path):
    config = ServiceConfig(tmp_path / "engine.db", timedelta(minutes=30))
    first = ExceptionEngineService(config)
    assert first.process(_payload()).body["result"] == "exception_detected"

    restarted = ExceptionEngineService(config)
    assert restarted.process(_payload()).body["result"] == "duplicate_event"


def test_service_returns_structured_validation_error(tmp_path):
    payload = _payload()
    payload["store_observation"]["observed_quantity"] = -1
    response = _service(tmp_path).process(payload)
    assert response.status_code == 400
    assert response.body["error"]["code"] == "invalid_input"
