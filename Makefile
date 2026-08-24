.PHONY: install run test lint validate clean

install:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements-dev.txt

run:
	.venv/bin/uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8080

test:
	.venv/bin/pytest --cov=app --cov=providers --cov-report=term-missing

lint:
	.venv/bin/ruff check .
	.venv/bin/ruff format --check .

validate: lint test
	.venv/bin/python scripts/secret_scan.py

clean:
	rm -rf .venv .pytest_cache .ruff_cache .coverage htmlcov data
