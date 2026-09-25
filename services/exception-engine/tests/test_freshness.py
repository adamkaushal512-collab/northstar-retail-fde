from datetime import datetime, timedelta

from exception_engine.freshness import is_inventory_stale


def test_inventory_within_freshness_threshold_is_not_stale():
    inventory_source_updated_at = datetime(2026, 9, 25, 10, 0)
    observation_timestamp = datetime(2026, 9, 25, 10, 20)
    freshness_threshold = timedelta(minutes=30)

    result = is_inventory_stale(
        inventory_source_updated_at=inventory_source_updated_at,
        observation_timestamp=observation_timestamp,
        freshness_threshold=freshness_threshold,
    )

    assert result is False


def test_inventory_older_than_freshness_threshold_is_stale():
    inventory_source_updated_at = datetime(2026, 9, 25, 10, 0)
    observation_timestamp = datetime(2026, 9, 25, 10, 45)
    freshness_threshold = timedelta(minutes=30)

    result = is_inventory_stale(
        inventory_source_updated_at=inventory_source_updated_at,
        observation_timestamp=observation_timestamp,
        freshness_threshold=freshness_threshold,
    )

    assert result is True


def test_inventory_exactly_at_freshness_threshold_is_not_stale():
    inventory_source_updated_at = datetime(2026, 9, 25, 10, 0)
    observation_timestamp = datetime(2026, 9, 25, 10, 30)
    freshness_threshold = timedelta(minutes=30)

    result = is_inventory_stale(
        inventory_source_updated_at=inventory_source_updated_at,
        observation_timestamp=observation_timestamp,
        freshness_threshold=freshness_threshold,
    )

    assert result is False
