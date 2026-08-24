from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from pathlib import Path

from app.core.models import AdvisoryRequest, Criticality, KnowledgeSource, RequestStatus


class SQLiteRequestRepository:
    def __init__(self, database_url: str) -> None:
        prefix = "sqlite:///"
        if not database_url.startswith(prefix):
            raise ValueError("Only sqlite:/// URLs are supported by the local adapter")
        self.path = database_url.removeprefix(prefix)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS advisory_requests (
                    request_id TEXT PRIMARY KEY,
                    question TEXT NOT NULL,
                    criticality TEXT NOT NULL,
                    requester TEXT NOT NULL,
                    status TEXT NOT NULL,
                    response TEXT,
                    sources_json TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

    def save(self, request: AdvisoryRequest) -> None:
        sources_json = json.dumps(
            [
                {
                    "title": source.title,
                    "url": source.url,
                    "excerpt": source.excerpt,
                    "approved": source.approved,
                }
                for source in request.sources
            ]
        )
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO advisory_requests VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(request_id) DO UPDATE SET
                    status=excluded.status,
                    response=excluded.response,
                    sources_json=excluded.sources_json,
                    updated_at=excluded.updated_at
                """,
                (
                    request.request_id,
                    request.question,
                    request.criticality.value,
                    request.requester,
                    request.status.value,
                    request.response,
                    sources_json,
                    request.created_at.isoformat(),
                    request.updated_at.isoformat(),
                ),
            )

    def get(self, request_id: str) -> AdvisoryRequest | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM advisory_requests WHERE request_id = ?", (request_id,)
            ).fetchone()
        if row is None:
            return None
        return AdvisoryRequest(
            request_id=row["request_id"],
            question=row["question"],
            criticality=Criticality(row["criticality"]),
            requester=row["requester"],
            status=RequestStatus(row["status"]),
            response=row["response"],
            sources=[KnowledgeSource(**item) for item in json.loads(row["sources_json"])],
            created_at=datetime.fromisoformat(row["created_at"]),
            updated_at=datetime.fromisoformat(row["updated_at"]),
        )
