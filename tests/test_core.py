from app.adapters.events import InMemoryEventPublisher
from app.adapters.knowledge import JsonKnowledgeProvider
from app.adapters.persistence import SQLiteRequestRepository
from app.core.models import Criticality
from app.services.advisor import AdvisorService


class StubAI:
    name = "stub"

    def __init__(self):
        self.calls = 0

    def generate(self, question, sources):
        self.calls += 1
        return f"answer:{question}:{len(sources)}"


def test_core_is_provider_independent(tmp_path):
    ai = StubAI()
    events = InMemoryEventPublisher()
    service = AdvisorService(
        ai=ai,
        knowledge=JsonKnowledgeProvider("examples/knowledge.json"),
        repository=SQLiteRequestRepository(f"sqlite:///{tmp_path / 'core.db'}"),
        events=events,
    )
    result = service.submit("Review cloud architecture security", Criticality.HIGH)
    assert result.status.value == "completed"
    assert ai.calls == 1
    assert [event[0] for event in events.events] == [
        "advisory.received",
        "advisory.completed",
    ]


def test_ai_is_not_called_for_critical_requests(tmp_path):
    ai = StubAI()
    service = AdvisorService(
        ai=ai,
        knowledge=JsonKnowledgeProvider("examples/knowledge.json"),
        repository=SQLiteRequestRepository(f"sqlite:///{tmp_path / 'critical.db'}"),
        events=InMemoryEventPublisher(),
    )
    result = service.submit("Critical cloud security incident", Criticality.CRITICAL)
    assert result.status.value == "human_review"
    assert ai.calls == 0
