from datetime import datetime

from pydantic import BaseModel, Field

from app.core.models import Criticality, RequestStatus


class AdvisoryInput(BaseModel):
    question: str = Field(min_length=5, max_length=5000)
    criticality: Criticality = Criticality.MEDIUM
    requester: str = Field(default="anonymous", min_length=1, max_length=200)


class SourceOutput(BaseModel):
    title: str
    url: str
    excerpt: str


class AdvisoryOutput(BaseModel):
    request_id: str
    question: str
    criticality: Criticality
    requester: str
    status: RequestStatus
    response: str | None
    sources: list[SourceOutput]
    created_at: datetime
    updated_at: datetime


class HealthOutput(BaseModel):
    service: str
    status: str
    environment: str
    ai_provider: str
    cloud_provider: str
