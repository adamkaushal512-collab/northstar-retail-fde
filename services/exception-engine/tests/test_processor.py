import unittest

from datetime import datetime, timedelta, timezone

from exception_engine.idempotency import InMemoryEventRegistry
from exception_engine.models import DetectionInput
from exception_engine.processor import ExceptionProcessor, ProcessingResult


class ExceptionProcessorTests(unittest.TestCase):
    def _create_evidence(
        self,
        *,
        observed_quantity: int | None = 0,
        observation_event_id: str = "observation-001",
        inventory_source_updated_at: datetime | None = None,
        observation_timestamp: datetime | None = None,
    ) -> DetectionInput:
        if inventory_source_updated_at is None:
            inventory_source_updated_at = datetime(
                2026, 9, 24, 13, 0, tzinfo=timezone.utc
            )

        if observation_timestamp is None:
            observation_timestamp = datetime(
                2026, 9, 24, 13, 45, tzinfo=timezone.utc
            )

        return DetectionInput(
            order_id="order-100045",
            store_id="store-042",
            product_id="product-98765",
            fulfillment_type="BOPIS",
            required_quantity=1,
            available_quantity=2,
            observed_quantity=observed_quantity,
            inventory_source_updated_at=inventory_source_updated_at,
            inventory_ingested_at=datetime(
                2026, 9, 24, 13, 2, tzinfo=timezone.utc
            ),
            observation_event_id=observation_event_id,
            observation_timestamp=observation_timestamp,
        )

    def test_creates_operational_exception_for_discrepancy(self):
        registry = InMemoryEventRegistry()
        processor = ExceptionProcessor(registry)
        evidence = self._create_evidence()

        outcome = processor.process(evidence)

        self.assertEqual(
            outcome.result,
            ProcessingResult.EXCEPTION_DETECTED,
        )
        self.assertIsNotNone(outcome.exception)

        exception = outcome.exception

        self.assertEqual(exception.exception_type, "INVENTORY_NOT_FOUND")
        self.assertEqual(exception.order_id, evidence.order_id)
        self.assertEqual(exception.store_id, evidence.store_id)
        self.assertEqual(exception.product_id, evidence.product_id)
        self.assertEqual(
            exception.required_quantity,
            evidence.required_quantity,
        )
        self.assertEqual(
            exception.available_quantity,
            evidence.available_quantity,
        )
        self.assertEqual(
            exception.observed_quantity,
            evidence.observed_quantity,
        )
        self.assertEqual(
            exception.inventory_source_updated_at,
            evidence.inventory_source_updated_at,
        )
        self.assertEqual(
            exception.inventory_ingested_at,
            evidence.inventory_ingested_at,
        )
        self.assertEqual(
            exception.observation_event_id,
            evidence.observation_event_id,
        )
        self.assertEqual(
            exception.observation_timestamp,
            evidence.observation_timestamp,
        )
        self.assertIsNotNone(exception.detected_at)

    def test_marks_stale_inventory_on_created_exception(self):
        registry = InMemoryEventRegistry()
        processor = ExceptionProcessor(
            registry,
            freshness_threshold=timedelta(minutes=30),
        )
        evidence = self._create_evidence(
            inventory_source_updated_at=datetime(
                2026, 9, 24, 13, 0, tzinfo=timezone.utc
            ),
            observation_timestamp=datetime(
                2026, 9, 24, 13, 45, tzinfo=timezone.utc
            ),
        )

        outcome = processor.process(evidence)

        self.assertEqual(
            outcome.result,
            ProcessingResult.EXCEPTION_DETECTED,
        )
        self.assertIsNotNone(outcome.exception)
        self.assertTrue(outcome.exception.inventory_is_stale)

    def test_rejects_duplicate_event_without_creating_second_exception(self):
        registry = InMemoryEventRegistry()
        processor = ExceptionProcessor(registry)
        evidence = self._create_evidence()

        first_outcome = processor.process(evidence)
        second_outcome = processor.process(evidence)

        self.assertEqual(
            first_outcome.result,
            ProcessingResult.EXCEPTION_DETECTED,
        )
        self.assertIsNotNone(first_outcome.exception)

        self.assertEqual(
            second_outcome.result,
            ProcessingResult.DUPLICATE_EVENT,
        )
        self.assertIsNone(second_outcome.exception)

    def test_returns_no_exception_when_observed_quantity_is_sufficient(self):
        registry = InMemoryEventRegistry()
        processor = ExceptionProcessor(registry)
        evidence = self._create_evidence(
            observed_quantity=1,
            observation_event_id="observation-002",
        )

        outcome = processor.process(evidence)

        self.assertEqual(
            outcome.result,
            ProcessingResult.NO_EXCEPTION,
        )
        self.assertIsNone(outcome.exception)


if __name__ == "__main__":
    unittest.main()
