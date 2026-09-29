from datetime import datetime, timezone

from exception_engine.copilot import investigate
from exception_engine.investigation import InvestigationContext, PolicySection
from exception_engine.models import OperationalException


def _context(stale=True, movements=()):
    now = datetime(2026, 9, 22, 18, 45, tzinfo=timezone.utc)
    exc = OperationalException(
        exception_type="INVENTORY_NOT_FOUND", order_id="order-1", store_id="store-1",
        product_id="product-1", required_quantity=1, available_quantity=2, observed_quantity=0,
        inventory_source_system="INVENTORY", inventory_source_updated_at=now,
        inventory_ingested_at=now, observation_event_id="obs-1", observation_timestamp=now,
        detected_at=now, inventory_is_stale=stale,
    )
    return InvestigationContext(exc, {}, {}, {}, tuple(movements), (PolicySection("P1", "1", "Investigation", "review evidence"),))


def test_copilot_surfaces_inventory_observation_conflict():
    brief = investigate(_context())
    assert brief.conflicts
    assert "reports 2 available" in brief.conflicts[0]


def test_copilot_labels_staleness_as_possible_not_proven_cause():
    brief = investigate(_context())
    assert any("not proof of root cause" in item for item in brief.possible_explanations)


def test_copilot_reports_missing_movements():
    brief = investigate(_context(movements=()))
    assert brief.missing_evidence
