from pathlib import Path
from tempfile import TemporaryDirectory

from exception_engine.persistence import SQLiteEventRegistry


def test_sqlite_registry_persists_duplicate_detection_across_instances():
    with TemporaryDirectory() as directory:
        path = Path(directory) / "engine.db"
        first = SQLiteEventRegistry(path)
        assert first.register("event-1") is True

        restarted = SQLiteEventRegistry(path)
        assert restarted.register("event-1") is False


def test_sqlite_registry_tracks_distinct_events():
    with TemporaryDirectory() as directory:
        registry = SQLiteEventRegistry(Path(directory) / "engine.db")
        assert registry.register("event-1") is True
        assert registry.register("event-2") is True
