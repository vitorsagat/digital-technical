from __future__ import annotations

import logging


class LoggingEventPublisher:
    def __init__(self) -> None:
        self.logger = logging.getLogger("digital_technical.events")

    def publish(self, event_type: str, payload: dict[str, object]) -> None:
        self.logger.info("domain_event", extra={"event_type": event_type, **payload})


class InMemoryEventPublisher:
    def __init__(self) -> None:
        self.events: list[tuple[str, dict[str, object]]] = []

    def publish(self, event_type: str, payload: dict[str, object]) -> None:
        self.events.append((event_type, payload))
