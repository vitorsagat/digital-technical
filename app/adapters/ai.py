from __future__ import annotations

import httpx

from app.core.models import KnowledgeSource


class DeterministicAIProvider:
    name = "deterministic"

    def generate(self, question: str, sources: list[KnowledgeSource]) -> str:
        titles = ", ".join(source.title for source in sources)
        return (
            f"Technical assessment for: {question}\n"
            f"Validated against approved sources: {titles}.\n"
            "Recommendation: confirm assumptions in a non-production environment, "
            "record evidence, and use an approved change process."
        )


class OpenAICompatibleAIProvider:
    """Adapter for OpenAI-compatible chat-completions endpoints."""

    name = "openai-compatible"

    def __init__(self, base_url: str, api_key: str, model: str, timeout: float = 30.0) -> None:
        if not api_key:
            raise ValueError("DT_AI_API_KEY is required for the openai-compatible provider")
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def generate(self, question: str, sources: list[KnowledgeSource]) -> str:
        context = "\n".join(
            f"- {source.title} ({source.url}): {source.excerpt}" for source in sources
        )
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "temperature": 0.1,
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "You are DIGITAL TECHNICAL. Use only the approved context, "
                            "separate facts from assumptions, and do not invent citations."
                        ),
                    },
                    {"role": "user", "content": f"Question: {question}\nContext:\n{context}"},
                ],
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        return str(response.json()["choices"][0]["message"]["content"])
