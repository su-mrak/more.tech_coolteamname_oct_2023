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
	docker compose -f docker-compose.yaml up -d postgres redis

run-upload:
	$(PYTHON) app/upload_entrypoint.py

test-integration:
	cd app && $(PYTHON_PRE) -m pytest -v -s

lint:
	pre-commit run -a

run-docker-dev:
	docker compose -f docker-compose.yaml up -d

jup:
	. .venv/bin/activate
	$(PYTHON) -m jupyterlab

jup-darwin:
	. .venv/bin/activate
	$(PYTHON) -m jupyterlab --app-dir=/opt/homebrew/share/jupyter/lab
