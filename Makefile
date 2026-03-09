COV_REPORT ?= term-missing

.SILENT: help
all: help

run:
	docker compose up -d

ruff-lint:
	ruff check

ruff-lint-fix:
	ruff check --fix --show-fixes

ruff-format:
	ruff format --diff

ruff-format-fix:
	ruff format

mypy:
	mypy

pytest:
	pytest --cov --cov-fail-under=100 --cov-branch --cov-report=$(COV_REPORT)

check: ruff-lint ruff-format mypy pytest

fix: ruff-lint-fix ruff-format-fix

help: ## Display available commands
	echo "Available make commands:"
	echo
	grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'
