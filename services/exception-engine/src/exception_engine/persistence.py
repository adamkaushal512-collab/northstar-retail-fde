import json
import sqlite3
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from .models import OperationalException


class SQLiteEventRegistry:
    """Durable, atomic idempotency registry backed by SQLite."""

    def __init__(self, database_path: str | Path) -> None:
        self._database_path = str(database_path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path, timeout=5.0)
        connection.execute("PRAGMA busy_timeout = 5000")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS processed_events (
                    event_id TEXT PRIMARY KEY,
                    processed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def register(self, event_id: str) -> bool:
        if not event_id:
            raise ValueError("event_id must be non-empty")
        try:
            with self._connect() as connection:
                connection.execute(
                    "INSERT INTO processed_events(event_id) VALUES (?)",
                    (event_id,),
                )
            return True
        except sqlite3.IntegrityError:
            return False


class SQLiteExceptionRepository:
    """Durable store for detected operational exceptions."""

    def __init__(self, database_path: str | Path) -> None:
        self._database_path = str(database_path)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self._database_path, timeout=5.0)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA busy_timeout = 5000")
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS operational_exceptions (
                    observation_event_id TEXT PRIMARY KEY,
                    order_id TEXT NOT NULL,
                    exception_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def save(self, exception: OperationalException) -> None:
        payload = asdict(exception)
        for key, value in payload.items():
            if isinstance(value, datetime):
                payload[key] = value.isoformat()
        with self._connect() as connection:
            connection.execute(
                """
                INSERT OR IGNORE INTO operational_exceptions(
                    observation_event_id, order_id, exception_type, payload_json
                ) VALUES (?, ?, ?, ?)
                """,
                (
                    exception.observation_event_id,
                    exception.order_id,
                    exception.exception_type,
                    json.dumps(payload, sort_keys=True),
                ),
            )

    def get_by_event_id(self, event_id: str) -> dict[str, object] | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT payload_json FROM operational_exceptions WHERE observation_event_id = ?",
                (event_id,),
            ).fetchone()
        return None if row is None else json.loads(row["payload_json"])
