# Security model

## Trust boundaries

- The API gateway is the public boundary and should enforce TLS, identity,
  throttling, request-size limits, and web application firewall policies.
- The application trusts only gateway-verified identity claims and validated
  request bodies.
- Provider adapters are outbound boundaries. They receive only the minimum data
  required for their operation.
- Knowledge and generated output are untrusted content until the safety policy
  has completed.

## Identity and secrets

- Use workload identity, instance principals, resource principals, or equivalent
  short-lived cloud identity instead of static cloud keys.
- Store AI credentials and integration secrets in the selected cloud secret
  manager. Inject them at runtime and never expose them through Terraform output.
- Use separate identities and least-privilege policies for CI, deployment, API,
  worker, and operational access.
- Require SSO and MFA for administrative access and retain auditable role grants.

## Data protection

- Encrypt traffic with TLS 1.2 or newer and use provider-managed encryption at
  rest, with customer-managed keys when policy requires them.
- Classify input, retrieved knowledge, prompts, responses, and logs before using
  production data. Redact secrets and personal data from telemetry.
- Configure explicit retention and deletion periods for the database, object
  storage, queue dead letters, logs, and model-provider histories.
- Restrict knowledge ingestion to approved sources and retain source provenance.

## AI safety

- Keep system instructions outside user-controlled fields and treat retrieved
  documents as data, never executable instructions.
- Require human review for critical requests, low-confidence output, missing
  citations, or actions with operational impact.
- Allowlist tools and outbound destinations. The reference implementation does
  not execute infrastructure actions from generated text.
- Evaluate model changes against a versioned safety and quality dataset before
  promotion.

## Production checklist

- Private networking or restricted ingress configured where supported.
- Enterprise OIDC/OAuth enabled; development API key disabled.
- WAF, throttling, payload limits, and denial-of-service controls enabled.
- Secret rotation and emergency revocation tested.
- Database backup, restore, retention, and disaster recovery tested.
- Central logs, metrics, traces, alerts, and audit events enabled.
- Dependency, container, IaC, and secret scanning required in CI.
- Incident response contacts, runbooks, and evidence retention approved.
- Penetration testing and threat-model review completed before production data.
