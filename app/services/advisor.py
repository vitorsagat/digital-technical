from __future__ import annotations

import logging

from app.core.models import AdvisoryRequest, Criticality
from app.core.ports import AIProvider, EventPublisher, KnowledgeProvider, RequestRepository

logger = logging.getLogger(__name__)


class AdvisorService:
    def __init__(
        self,
        ai: AIProvider,
        knowledge: KnowledgeProvider,
        repository: RequestRepository,
        events: EventPublisher,
    ) -> None:
        self.ai = ai
        self.knowledge = knowledge
        self.repository = repository
        self.events = events

    def submit(
        self,
        question: str,
        criticality: Criticality = Criticality.MEDIUM,
        requester: str = "anonymous",
    ) -> AdvisoryRequest:
        request = AdvisoryRequest(
            question=question.strip(), criticality=criticality, requester=requester
        )
        self.repository.save(request)
        self.events.publish("advisory.received", self._event_payload(request))

        try:
            sources = [item for item in self.knowledge.search(request.question) if item.approved]
            if criticality == Criticality.CRITICAL:
                request.require_review(
                    (
                        "Critical requests require human validation before a "
                        "recommendation is released."
                    ),
                    sources,
                )
            elif not sources:
                request.require_review("No approved knowledge source matched the request.")
            else:
                request.complete(self.ai.generate(request.question, sources), sources)
        except Exception:
            logger.exception("advisor_processing_failed", extra={"request_id": request.request_id})
            request.fail("The request could not be processed safely.")

        self.repository.save(request)
        self.events.publish(f"advisory.{request.status.value}", self._event_payload(request))
        return request

    def get(self, request_id: str) -> AdvisoryRequest | None:
        return self.repository.get(request_id)

    @staticmethod
    def _event_payload(request: AdvisoryRequest) -> dict[str, object]:
        return {
            "request_id": request.request_id,
            "status": request.status.value,
            "criticality": request.criticality.value,
        }
