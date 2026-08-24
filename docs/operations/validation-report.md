# Validation report

Validation date: 2026-08-24

## Application

- Runtime: Python 3.12.13
- Static analysis: Ruff passed
- Formatting check: 38 Python files passed
- Automated tests: 11 passed
- Statement coverage: 94 percent across `app` and `providers`
- Repository secret scan: passed
- Clean wheel installation in a new Python 3.12 virtual environment: passed
- Tests repeated from the clean environment: 11 passed

## Functional API flow

The application was started with the deterministic AI adapter and local SQLite
repository. The following real HTTP sequence passed:

1. `GET /health` returned `200` and provider metadata.
2. `POST /v1/requests` returned `201`, a generated recommendation, and an
   approved knowledge citation.
3. `GET /v1/requests/{request_id}` returned `200` with the persisted result.
4. Structured request and domain-event logs contained correlation identifiers.

No live AI credential or customer data was used.

## Infrastructure as code

- Terraform CLI: 1.5.7
- OCI provider: `oracle/oci` 8.28.0, locked in the OCI stack
- `terraform fmt -check -recursive`: passed
- `terraform init -backend=false`: passed
- `terraform validate`: passed
- `terraform plan`, `apply`, and `destroy`: not run during this repository check

## Existing OCI functional environment

The previously deployed test environment in Japan Central (Osaka) remains
independent from local runtime configuration. Its API Gateway health endpoint
returned HTTP 200 during deployment validation:

```text
https://hxzr7rzbkdj2cplwqaeh6sxob4.apigateway.ap-osaka-1.oci.customer-oci.com/advisor/health
```

The environment includes the networking, API Gateway, Functions Application,
Queue, NoSQL, Object Storage, logging, notification, and container repository
foundation. The Functions Application does not yet contain the Python API image;
therefore the deployed public route is a platform health route, not the complete
advisory API.

## Release interpretation

The repository is a validated functional MVP and a reproducible OCI foundation.
It is not yet approved for production data. Production readiness additionally
requires enterprise identity, secrets integration, provider-native persistence,
an executable workload image, RAG ingestion, mailbox integration, operational
alerts, security testing, and organizational approvals.
