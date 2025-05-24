OUT = ./app/internal/stubs
INPUT = ../protos
PROTOS = $(INPUT)/*.proto

MSG = ""

FASTAPI_SERVER = uvicorn


.PHONY: 
	clean, 
	gen-grpc,
	run,


install:
	poetry install --no-root


gen-grpc:
	poetry run python -m grpc_tools.protoc -I$(INPUT) --python_out=$(OUT) --grpc_python_out=$(OUT) $(PROTOS)


run:
	poetry run $(FASTAPI_SERVER) app.main:app --reload


migrate:
	poetry run alembic upgrade head

downgrade:
	poetry run alembic downgrade -1

makemigration:
	poetry run alembic revision --autogenerate -m "$(MSG)"


clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -r {} +
	find . -name "*.log" -delete
	find . -name "*.log.*" -delete
	find . -name ".ruff_cache" -type d -exec rm -r {} +
	find .. -name ".ruff_cache" -type d -exec rm -r {} +
	find .. -name ".mypy_cache" -type d -exec rm -r {} +
