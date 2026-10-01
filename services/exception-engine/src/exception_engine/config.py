import os
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path


class ConfigurationError(ValueError):
    pass


@dataclass(frozen=True)
class ServiceConfig:
    database_path: Path
    freshness_threshold: timedelta

    @classmethod
    def from_env(cls) -> "ServiceConfig":
        database_path = Path(os.getenv("EXCEPTION_ENGINE_DB_PATH", "var/exception-engine.db"))
        raw_minutes = os.getenv("INVENTORY_FRESHNESS_MINUTES", "30")
        try:
            minutes = int(raw_minutes)
        except ValueError as exc:
            raise ConfigurationError("INVENTORY_FRESHNESS_MINUTES must be an integer") from exc
        if minutes <= 0:
            raise ConfigurationError("INVENTORY_FRESHNESS_MINUTES must be positive")
        return cls(database_path=database_path, freshness_threshold=timedelta(minutes=minutes))
