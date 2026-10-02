import json
import logging
from datetime import timedelta
from pathlib import Path

from exception_engine.config import ServiceConfig
from exception_engine.observability import ServiceMetrics
from exception_engine.service import ExceptionEngineService

ROOT = Path(__file__).resolve().parents[3]
EXAMPLE = ROOT / "data" / "examples" / "bopis-inventory-discrepancy.json"


def _payload():
    with EXAMPLE.open(encoding="utf-8") as handle:
        return json.load(handle)


def _service(tmp_path, **kwargs):
    return ExceptionEngineService(
        ServiceConfig(tmp_path / "engine.db", timedelta(minutes=30)),
        **kwargs,
    )


def test_metrics_count_detected_and_duplicate_events(tmp_path):
    service = _service(tmp_path)
    assert service.process(_payload()).body["result"] == "exception_detected"
    assert service.process(_payload()).body["result"] == "duplicate_event"
    metrics = service.metrics_snapshot()
    assert metrics.processed_events == 2
    assert metrics.detected_exceptions == 1
    assert metrics.duplicate_events == 1
    assert metrics.average_processing_seconds >= 0


def test_metrics_count_invalid_input(tmp_path):
    service = _service(tmp_path)
    payload = _payload()
    payload["store_observation"]["observed_quantity"] = -1
    assert service.process(payload).status_code == 400
    metrics = service.metrics_snapshot()
    assert metrics.processed_events == 1
    assert metrics.invalid_inputs == 1


def test_metrics_snapshot_is_zero_before_processing():
    snapshot = ServiceMetrics().snapshot()
    assert snapshot.processed_events == 0
    assert snapshot.average_processing_seconds == 0.0


def test_structured_log_contains_correlation_and_outcome(tmp_path, caplog):
    logger = logging.getLogger("test.exception-engine")
    service = _service(tmp_path, logger=logger)
    with caplog.at_level(logging.INFO, logger=logger.name):
        service.process(_payload(), correlation_id="corr-123")
    record = json.loads(caplog.records[-1].message)
    assert record["event"] == "exception_processing_completed"
    assert record["correlation_id"] == "corr-123"
    assert record["result"] == "exception_detected"
    assert record["observation_event_id"]


def test_health_reports_ok(tmp_path):
    response = _service(tmp_path).health()
    assert response.status_code == 200
    assert response.body == {"status": "ok"}


def test_readiness_reports_ready_when_database_available(tmp_path):
    response = _service(tmp_path).readiness()
    assert response.status_code == 200
    assert response.body == {"status": "ready"}
