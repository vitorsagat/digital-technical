from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.api.main import create_app
from app.config import Settings


@pytest.fixture
def client(tmp_path: Path) -> TestClient:
    knowledge = Path(__file__).parents[1] / "examples" / "knowledge.json"
    settings = Settings(
        database_url=f"sqlite:///{tmp_path / 'test.db'}",
        knowledge_file=str(knowledge),
        ai_provider="deterministic",
        environment="test",
    )
    return TestClient(create_app(settings))
