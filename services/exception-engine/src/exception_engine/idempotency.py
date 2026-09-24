class InMemoryEventRegistry:
    def __init__(self) -> None:
        self._processed_event_ids: set[str] = set()

    def register(self, event_id: str) -> bool:
        if event_id in self._processed_event_ids:
            return False

        self._processed_event_ids.add(event_id)
        return True
