from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


class RequestStatus(StrEnum):
    RECEIVED = "received"
    COMPLETED = "completed"
    HUMAN_REVIEW = "human_review"
    FAILED = "failed"


class Criticality(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class KnowledgeSource:
    title: str
    url: str
    excerpt: str
    approved: bool = True


@dataclass(slots=True)
class AdvisoryRequest:
    question: str
    criticality: Criticality = Criticality.MEDIUM
    requester: str = "anonymous"
    request_id: str = field(default_factory=lambda: str(uuid4()))
    status: RequestStatus = RequestStatus.RECEIVED
    response: str | None = None
    sources: list[KnowledgeSource] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def complete(self, response: str, sources: list[KnowledgeSource]) -> None:
        self.response = response
        self.sources = sources
        self.status = RequestStatus.COMPLETED
        self.updated_at = datetime.now(UTC)

    def require_review(self, reason: str, sources: list[KnowledgeSource] | None = None) -> None:
        self.response = reason
        self.sources = sources or []
        self.status = RequestStatus.HUMAN_REVIEW
        self.updated_at = datetime.now(UTC)

    def fail(self, reason: str) -> None:
        self.response = reason
        self.status = RequestStatus.FAILED
        self.updated_at = datetime.now(UTC)
