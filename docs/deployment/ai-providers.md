# AI provider configuration

## Deterministic

Use `DT_AI_PROVIDER=deterministic` for development, CI, demos, and offline tests.
No network or secret is required.

## OpenAI-compatible

Set:

```text
DT_AI_PROVIDER=openai-compatible
DT_AI_BASE_URL=https://provider.example/v1
DT_AI_MODEL=approved-model-or-deployment
DT_AI_API_KEY=<runtime secret>
```

This adapter works with chat-completions-compatible gateways. Azure OpenAI may
require a dedicated adapter for its deployment path and headers. OCI Generative
AI, Google Gemini, and local model servers should each implement the `AIProvider`
protocol and provider-specific authentication outside the core.

Before production, add model allowlists, content filters, token/cost limits,
timeouts, retries, circuit breakers, red-team tests, and prompt/version audit.
