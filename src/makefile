PYTHON = python
APP = app
MAIN = main

GRPC_SERVER = app/server.py
OUT = ./app/internal/generated
INPUT = ../protos
PROTOS = $(INPUT)/*.proto


.PHONY: 
	clean, 
	gen-grpc,
	grpc-server,
	run

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