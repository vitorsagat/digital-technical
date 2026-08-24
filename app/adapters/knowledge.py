from __future__ import annotations

import json
from pathlib import Path

from app.core.models import KnowledgeSource


class JsonKnowledgeProvider:
    def __init__(self, path: str) -> None:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        self.sources = [KnowledgeSource(**item) for item in raw]

    def search(self, query: str, limit: int = 5) -> list[KnowledgeSource]:
        terms = {term.lower() for term in query.split() if len(term) > 2}
        ranked = []
        for source in self.sources:
            text = f"{source.title} {source.excerpt}".lower()
            score = sum(term in text for term in terms)
            if score:
                ranked.append((score, source))
        ranked.sort(key=lambda item: item[0], reverse=True)
        return [source for _, source in ranked[:limit]]
