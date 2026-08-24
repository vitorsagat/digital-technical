# Architecture overview

## Principles

1. The domain has no cloud SDK, HTTP framework, database, or model-vendor import.
2. Application services orchestrate ports defined by the core.
3. Adapters translate vendor protocols at the boundary.
4. Configuration chooses adapters; it does not change business rules.
5. Critical requests and missing approved sources always require human review.

## Layers

- **Business logic:** request lifecycle, criticality, source approval, safety outcome.
- **Application layer:** `AdvisorService` orchestration and domain events.
- **Provider adapters:** AI, knowledge, repository, event, storage, API transport.
- **Cloud/AI providers:** local runtime or services selected for an environment.

The API currently processes synchronously. An event-driven worker can call the
same `AdvisorService` without changing the core.
