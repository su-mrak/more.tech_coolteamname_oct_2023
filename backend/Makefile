PYTHON ?= .venv/bin/python
PYTHON_PRE ?= ../.venv/bin/python

install:
	python3.10 -m venv .venv
	. .venv/bin/activate
	$(PYTHON) -m pip install poetry
	poetry update

run-web:
	cd app && $(PYTHON_PRE) -m poetry run python3 web_entrypoint.py

run-infra:
	docker compose -f docker-compose.yaml up  -d postgres

test-integration:
	cd app && $(PYTHON_PRE) -m pytest -v -s

lint:
	pre-commit run -a

run-docker-dev:
	docker compose -f docker-compose.yaml up -d
