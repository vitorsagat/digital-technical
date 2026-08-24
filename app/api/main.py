from __future__ import annotations

import hmac
import logging
from collections.abc import Callable
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status

from app.adapters.ai import DeterministicAIProvider, OpenAICompatibleAIProvider
from app.adapters.events import LoggingEventPublisher
from app.adapters.knowledge import JsonKnowledgeProvider
from app.adapters.persistence import SQLiteRequestRepository
from app.api.schemas import AdvisoryInput, AdvisoryOutput, HealthOutput, SourceOutput
from app.config import Settings, get_settings
from app.core.models import AdvisoryRequest
from app.observability import configure_logging
from app.services.advisor import AdvisorService

logger = logging.getLogger(__name__)


def _build_ai(settings: Settings):
    if settings.ai_provider == "deterministic":
        return DeterministicAIProvider()
    if settings.ai_provider == "openai-compatible":
        return OpenAICompatibleAIProvider(
            base_url=settings.ai_base_url,
            api_key=settings.ai_api_key,
            model=settings.ai_model,
        )
    raise ValueError(f"Unsupported AI provider: {settings.ai_provider}")


def build_service(settings: Settings) -> AdvisorService:
    return AdvisorService(
        ai=_build_ai(settings),
        knowledge=JsonKnowledgeProvider(settings.knowledge_file),
        repository=SQLiteRequestRepository(settings.database_url),
        events=LoggingEventPublisher(),
    )


def to_output(request: AdvisoryRequest) -> AdvisoryOutput:
    return AdvisoryOutput(
        request_id=request.request_id,
        question=request.question,
        criticality=request.criticality,
        requester=request.requester,
        status=request.status,
        response=request.response,
        sources=[
            SourceOutput(title=source.title, url=source.url, excerpt=source.excerpt)
            for source in request.sources
        ],
        created_at=request.created_at,
        updated_at=request.updated_at,
    )


def create_app(
    settings: Settings | None = None,
    service_factory: Callable[[Settings], AdvisorService] = build_service,
) -> FastAPI:
    settings = settings or get_settings()
    configure_logging(settings.log_level)
    service = service_factory(settings)
    app = FastAPI(
        title="DIGITAL TECHNICAL API",
        version="0.1.0",
        description="Provider-independent technical advisory API.",
    )
    app.state.settings = settings
    app.state.service = service

    @app.middleware("http")
    async def request_context(request: Request, call_next):
        request_id = request.headers.get("x-request-id", str(uuid4()))
        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        logger.info(
            "http_request",
            extra={"request_id": request_id, "method": request.method, "path": request.url.path},
        )
        return response

    def authorize(x_api_key: str | None = Header(default=None)) -> None:
        if settings.require_api_key and not (
            x_api_key and hmac.compare_digest(x_api_key, settings.api_key)
        ):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")

    @app.get("/health", response_model=HealthOutput, tags=["operations"])
    def health() -> HealthOutput:
        return HealthOutput(
            service="DIGITAL TECHNICAL",
            status="ok",
            environment=settings.environment,
            ai_provider=settings.ai_provider,
            cloud_provider=settings.cloud_provider,
        )

    @app.post(
        "/v1/requests",
        response_model=AdvisoryOutput,
        status_code=status.HTTP_201_CREATED,
        dependencies=[Depends(authorize)],
        tags=["advisor"],
    )
    def submit(payload: AdvisoryInput) -> AdvisoryOutput:
        return to_output(service.submit(payload.question, payload.criticality, payload.requester))

    @app.get(
        "/v1/requests/{request_id}",
        response_model=AdvisoryOutput,
        dependencies=[Depends(authorize)],
        tags=["advisor"],
    )
    def get_request(request_id: str) -> AdvisoryOutput:
        result = service.get(request_id)
        if result is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Request not found")
        return to_output(result)

    return app


app = create_app()
