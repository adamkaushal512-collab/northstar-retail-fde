from datetime import timedelta

import pytest

from exception_engine.config import ConfigurationError, ServiceConfig


def test_service_config_reads_environment(monkeypatch, tmp_path):
    path = tmp_path / "northstar.db"
    monkeypatch.setenv("EXCEPTION_ENGINE_DB_PATH", str(path))
    monkeypatch.setenv("INVENTORY_FRESHNESS_MINUTES", "45")
    config = ServiceConfig.from_env()
    assert config.database_path == path
    assert config.freshness_threshold == timedelta(minutes=45)


def test_service_config_rejects_invalid_threshold(monkeypatch):
    monkeypatch.setenv("INVENTORY_FRESHNESS_MINUTES", "zero")
    with pytest.raises(ConfigurationError):
        ServiceConfig.from_env()
