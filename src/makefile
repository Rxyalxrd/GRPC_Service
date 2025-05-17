PYTHON = python
APP = app
MAIN = main

GRPC_SERVER = app/server.py
OUT = ./app/internal/stubs
INPUT = ../protos
PROTOS = $(INPUT)/*.proto
MSG = ""

.PHONY: 
	clean, 
	gen-grpc,
	grpc-server,
	run

install:
	poetry install --no-root

clean:
	@echo "Cleaning up Python directories..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -r {} +
	find . -name "*.log" -delete
	find . -name "*.log.*" -delete
	find . -name ".ruff_cache" -type d -exec rm -r {} +
	find . -name ".mypy_cache" -type d -exec rm -r {} +

gen-grpc:
	poetry run python -m grpc_tools.protoc -I$(INPUT) --python_out=$(OUT) --grpc_python_out=$(OUT) $(PROTOS)

run:
	poetry run uvicorn $(APP).$(MAIN):$(APP) --reload

grpc-server:
	poetry run $(PYTHON) $(GRPC_SERVER)

migrate:
	poetry run alembic upgrade head

downgrade:
	poetry run alembic downgrade -1

makemigration:
	poetry run alembic revision --autogenerate -m "$(MSG)"
