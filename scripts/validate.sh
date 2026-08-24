#!/usr/bin/env sh
set -eu
.venv/bin/ruff check .
.venv/bin/ruff format --check .
.venv/bin/pytest --cov=app --cov=providers --cov-report=term-missing
.venv/bin/python scripts/secret_scan.py
