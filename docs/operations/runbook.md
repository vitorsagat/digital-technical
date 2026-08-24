# Operations runbook

## Signals

- `/health` must return 200;
- API latency and 5xx rate;
- review and failure outcome rates;
- queue age and dead-letter count;
- database throttling and storage capacity;
- AI latency, errors, token usage, and cost;
- authentication failures and anomalous traffic.

## Incident sequence

1. Identify the request ID from the response header.
2. Correlate gateway and application logs.
3. Disable the affected provider adapter or switch to deterministic/human review.
4. Preserve audit evidence and avoid logging prompts containing confidential data.
5. Restore through a reviewed deployment and execute E2E smoke tests.

## Backup and recovery

Back up database state according to RPO/RTO, retain object versions, protect
Terraform state, and test restoration quarterly. Never treat container images as
the only copy of source or configuration.
