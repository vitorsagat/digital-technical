# Provider capability contract

Every cloud implementation supplies these capabilities:

| Capability | Required behavior |
| --- | --- |
| Compute | Run the immutable application container with health checks |
| API | TLS termination, routing, throttling, request IDs |
| Database | Durable request storage and idempotent writes |
| Object storage | Private, encrypted, versioned knowledge objects |
| Messaging | At-least-once delivery, visibility timeout, dead-letter handling |
| Identity | Workload identity and external user/service authentication |
| Observability | Structured logs, metrics, traces, alerts, retention |
| Secrets | Runtime injection, rotation, audit, no source exposure |

Provider modules may differ internally. The container receives configuration and
implements the same HTTP and event contracts. Business logic must never import a
cloud SDK.
