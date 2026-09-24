import unittest

from exception_engine.idempotency import InMemoryEventRegistry


class InMemoryEventRegistryTests(unittest.TestCase):
    def test_registers_new_event(self):
        registry = InMemoryEventRegistry()

        result = registry.register("observation-001")

        self.assertTrue(result)

    def test_rejects_duplicate_event(self):
        registry = InMemoryEventRegistry()

        first_result = registry.register("observation-001")
        second_result = registry.register("observation-001")

        self.assertTrue(first_result)
        self.assertFalse(second_result)

    def test_registers_different_events_independently(self):
        registry = InMemoryEventRegistry()

        first_result = registry.register("observation-001")
        second_result = registry.register("observation-002")

        self.assertTrue(first_result)
        self.assertTrue(second_result)


if __name__ == "__main__":
    unittest.main()
