#!/usr/bin/env sh
set -eu
exec .venv/bin/uvicorn app.api.main:app --host "${DT_HOST:-0.0.0.0}" --port "${DT_PORT:-8080}"
