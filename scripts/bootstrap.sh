#!/usr/bin/env sh
set -eu

python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install -r requirements-dev.txt
[ -f .env ] || cp .env.example .env
mkdir -p data
echo "Bootstrap complete. Run: make validate"
