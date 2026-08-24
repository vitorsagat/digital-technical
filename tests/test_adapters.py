import pytest

from app.adapters.ai import DeterministicAIProvider, OpenAICompatibleAIProvider
from app.adapters.storage import LocalObjectStorage
from app.core.models import KnowledgeSource
from providers.cloud.registry import CLOUD_PROVIDERS, get_cloud_capabilities


def test_deterministic_ai_uses_sources():
    result = DeterministicAIProvider().generate(
        "question", [KnowledgeSource("Approved", "https://example.com", "context")]
    )
    assert "Approved" in result


def test_openai_adapter_rejects_missing_secret():
    with pytest.raises(ValueError, match="DT_AI_API_KEY"):
        OpenAICompatibleAIProvider("https://example.com/v1", "", "model")


def test_storage_blocks_path_traversal(tmp_path):
    storage = LocalObjectStorage(str(tmp_path / "objects"))
    storage.put("safe/file.txt", b"ok")
    assert storage.get("safe/file.txt") == b"ok"
    with pytest.raises(ValueError):
        storage.put("../escape.txt", b"bad")


def test_cloud_registry_has_required_capabilities():
    assert set(CLOUD_PROVIDERS) == {"oci", "aws", "azure", "gcp"}
    assert get_cloud_capabilities("oci").messaging == "Queue"
    with pytest.raises(ValueError):
        get_cloud_capabilities("unknown")
