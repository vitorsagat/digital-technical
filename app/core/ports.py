from __future__ import annotations

from typing import Protocol

from app.core.models import AdvisoryRequest, KnowledgeSource


class AIProvider(Protocol):
    @property
    def name(self) -> str: ...

    def generate(self, question: str, sources: list[KnowledgeSource]) -> str: ...


class KnowledgeProvider(Protocol):
    def search(self, query: str, limit: int = 5) -> list[KnowledgeSource]: ...


class RequestRepository(Protocol):
    def save(self, request: AdvisoryRequest) -> None: ...

    def get(self, request_id: str) -> AdvisoryRequest | None: ...


class EventPublisher(Protocol):
    def publish(self, event_type: str, payload: dict[str, object]) -> None: ...


class ObjectStorage(Protocol):
    def put(self, key: str, content: bytes) -> None: ...

    def get(self, key: str) -> bytes: ...
