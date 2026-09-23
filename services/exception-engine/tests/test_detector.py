import unittest
from datetime import datetime

from exception_engine.detector import should_create_inventory_not_found
from exception_engine.models import DetectionInput


class InventoryNotFoundDetectorTests(unittest.TestCase):

    def test_detects_inventory_not_found(self):
        evidence = DetectionInput(
            order_id="order-100045",
            store_id="store-042",
            product_id="product-98765",
            fulfillment_type="BOPIS",
            required_quantity=1,
            available_quantity=2,
            observed_quantity=0,
            inventory_source_updated_at=datetime.fromisoformat(
                "2026-09-23T13:00:00"
            ),
            inventory_ingested_at=datetime.fromisoformat(
                "2026-09-23T13:02:00"
            ),
            observation_event_id="observation-001",
            observation_timestamp=datetime.fromisoformat(
                "2026-09-23T13:45:00"
            ),
        )

        result = should_create_inventory_not_found(evidence)

        self.assertTrue(result)

    def test_does_not_detect_without_physical_observation(self):
        evidence = DetectionInput(
            order_id="order-100045",
            store_id="store-042",
            product_id="product-98765",
            fulfillment_type="BOPIS",
            required_quantity=1,
            available_quantity=2,
            observed_quantity=None,
            inventory_source_updated_at=datetime.fromisoformat(
                "2026-09-23T13:00:00"
            ),
            inventory_ingested_at=datetime.fromisoformat(
                "2026-09-23T13:02:00"
            ),
            observation_event_id="observation-002",
            observation_timestamp=datetime.fromisoformat(
                "2026-09-23T13:45:00"
            ),
        )

        result = should_create_inventory_not_found(evidence)

        self.assertFalse(result)
    def test_does_not_detect_when_observed_quantity_is_sufficient(self):
        evidence = DetectionInput(
            order_id="order-100045",
            store_id="store-042",
            product_id="product-98765",
            fulfillment_type="BOPIS",
            required_quantity=1,
            available_quantity=2,
            observed_quantity=1,
            inventory_source_updated_at=datetime.fromisoformat(
                "2026-09-23T13:00:00"
            ),
            inventory_ingested_at=datetime.fromisoformat(
                "2026-09-23T13:02:00"
            ),
            observation_event_id="observation-003",
            observation_timestamp=datetime.fromisoformat(
                "2026-09-23T13:45:00"
            ),
        )

        result = should_create_inventory_not_found(evidence)

        self.assertFalse(result)


    def test_detects_when_observed_quantity_is_below_required_quantity(self):
        evidence = DetectionInput(
            order_id="order-100046",
            store_id="store-042",
            product_id="product-98765",
            fulfillment_type="BOPIS",
            required_quantity=3,
            available_quantity=5,
            observed_quantity=2,
            inventory_source_updated_at=datetime.fromisoformat(
                "2026-09-23T13:00:00"
            ),
            inventory_ingested_at=datetime.fromisoformat(
                "2026-09-23T13:02:00"
            ),
            observation_event_id="observation-004",
            observation_timestamp=datetime.fromisoformat(
                "2026-09-23T13:45:00"
            ),
        )

        result = should_create_inventory_not_found(evidence)

        self.assertTrue(result)

    def test_does_not_detect_for_non_bopis_fulfillment(self):
        evidence = DetectionInput(
            order_id="order-100047",
            store_id="store-042",
            product_id="product-98765",
            fulfillment_type="SHIP_TO_HOME",
            required_quantity=1,
            available_quantity=2,
            observed_quantity=0,
            inventory_source_updated_at=datetime.fromisoformat(
                "2026-09-23T13:00:00"
            ),
            inventory_ingested_at=datetime.fromisoformat(
                "2026-09-23T13:02:00"
            ),
            observation_event_id="observation-005",
            observation_timestamp=datetime.fromisoformat(
                "2026-09-23T13:45:00"
            ),
        )

        result = should_create_inventory_not_found(evidence)

        self.assertFalse(result)

    def test_does_not_detect_when_inventory_already_reports_insufficient_stock(self):
        evidence = DetectionInput(
            order_id="order-100048",
            store_id="store-042",
            product_id="product-98765",
            fulfillment_type="BOPIS",
            required_quantity=3,
            available_quantity=2,
            observed_quantity=0,
            inventory_source_updated_at=datetime.fromisoformat(
                "2026-09-23T13:00:00"
            ),
            inventory_ingested_at=datetime.fromisoformat(
                "2026-09-23T13:02:00"
            ),
            observation_event_id="observation-006",
            observation_timestamp=datetime.fromisoformat(
                "2026-09-23T13:45:00"
            ),
        )

        result = should_create_inventory_not_found(evidence)

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
