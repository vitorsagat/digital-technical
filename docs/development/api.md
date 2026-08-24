# API contract

The application exposes an HTTP API under `/v1` and publishes an OpenAPI schema
at `/openapi.json`. Interactive documentation is available at `/docs`.

## Endpoints

### `GET /health`

Returns the runtime status and configured provider labels. It performs no
credentialed provider operation and is suitable for platform health probes.

### `POST /v1/requests`

Accepts a technical question, optional context, and a criticality level. The
service retrieves approved knowledge, generates a recommendation, applies the
safety policy, persists the result, and emits an event.

Example request:

```json
{
  "question": "How should a production cloud change be validated?",
  "context": "Customer-facing database migration",
  "criticality": "high"
}
```

The response contains an immutable request identifier, processing status,
recommendation, citations, risk notes, and whether human review is required.

### `GET /v1/requests/{request_id}`

Returns the persisted result or `404` when the identifier is unknown.

## Authentication

Set `DT_REQUIRE_API_KEY=true` and provide `DT_API_KEY` to enable the development
API-key guard. Clients then send `x-api-key`. In production, terminate OIDC or
OAuth 2.0 at the API gateway and pass verified identity claims to the workload;
the built-in key mechanism is not a replacement for enterprise identity.

## Errors and tracing

Validation errors use FastAPI's standard `422` response. Unauthorized requests
return `401`, unknown records return `404`, and unhandled failures return `500`.
Every response contains `x-request-id`; callers may provide that header to
correlate retries with structured application logs.

Clients should retry only idempotent reads and transient `429` or `5xx`
responses, using exponential backoff and a bounded retry budget.
