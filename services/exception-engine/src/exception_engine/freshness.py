from datetime import datetime, timedelta


def is_inventory_stale(
    inventory_source_updated_at: datetime,
    observation_timestamp: datetime,
    freshness_threshold: timedelta,
) -> bool:
    inventory_age = observation_timestamp - inventory_source_updated_at

    return inventory_age > freshness_threshold
