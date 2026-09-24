import unittest
from datetime import datetime, timezone

from exception_engine.idempotency import InMemoryEventRegistry
from exception_engine.models import DetectionInput
from exception_engine.processor import ExceptionProcessor, ProcessingResult


class ExceptionProcessorTests(unittest.TestCase):
    def test_detects_exception_for_new_discrepancy_event(self):
        registry = InMemoryEventRegistry()
        processor = ExceptionProcessor(registry)

        evidence = DetectionInput(
            order_id="order-100045",
            store_id="store-042",
            product_id="product-98765",
            fulfillment_type="BOPIS",
            required_quantity=1,
            available_quantity=2,
            observed_quantity=0,
            inventory_source_updated_at=datetime(
                2026, 9, 24, 13, 0, tzinfo=timezone.utc
            ),
            inventory_ingested_at=datetime(
                2026, 9, 24, 13, 2, tzinfo=timezone.utc
            ),
            observation_event_id="observation-001",
            observation_timestamp=datetime(
                2026, 9, 24, 13, 45, tzinfo=timezone.utc
            ),
        )

        result = processor.process(evidence)

        self.assertEqual(
            result,
            ProcessingResult.EXCEPTION_DETECTED,
        )

    def test_rejects_duplicate_discrepancy_event(self):
        registry = InMemoryEventRegistry()
        processor = ExceptionProcessor(registry)

        evidence = DetectionInput(
            order_id="order-100045",
            store_id="store-042",
            product_id="product-98765",
            fulfillment_type="BOPIS",
            required_quantity=1,
            available_quantity=2,
            observed_quantity=0,
            inventory_source_updated_at=datetime(
                2026, 9, 24, 13, 0, tzinfo=timezone.utc
            ),
            inventory_ingested_at=datetime(
                2026, 9, 24, 13, 2, tzinfo=timezone.utc
            ),
            observation_event_id="observation-001",
            observation_timestamp=datetime(
                2026, 9, 24, 13, 45, tzinfo=timezone.utc
            ),
        )

        first_result = processor.process(evidence)
        second_result = processor.process(evidence)

        self.assertEqual(
            first_result,
            ProcessingResult.EXCEPTION_DETECTED,
        )
        self.assertEqual(
            second_result,
            ProcessingResult.DUPLICATE_EVENT,
        )

    def test_returns_no_exception_when_observed_quantity_is_sufficient(self):
        registry = InMemoryEventRegistry()
        processor = ExceptionProcessor(registry)

        evidence = DetectionInput(
            order_id="order-100045",
            store_id="store-042",
            product_id="product-98765",
            fulfillment_type="BOPIS",
            required_quantity=1,
            available_quantity=2,
            observed_quantity=1,
            inventory_source_updated_at=datetime(
                2026, 9, 24, 13, 0, tzinfo=timezone.utc
            ),
            inventory_ingested_at=datetime(
                2026, 9, 24, 13, 2, tzinfo=timezone.utc
            ),
            observation_event_id="observation-002",
            observation_timestamp=datetime(
                2026, 9, 24, 13, 50, tzinfo=timezone.utc
            ),
        )

        result = processor.process(evidence)

        self.assertEqual(
            result,
            ProcessingResult.NO_EXCEPTION,
        )


if __name__ == "__main__":
    unittest.main()
