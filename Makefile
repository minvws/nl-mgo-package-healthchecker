COV_REPORT ?= term-missing

.SILENT: help
all: help

ruff-lint:  ## Run ruff lint checks
	ruff check

ruff-lint-fix:  ## Fix ruff lint issues
	ruff check --fix --show-fixes

ruff-format:  ## Show ruff format differences
	ruff format --diff

ruff-format-fix:  ## Fix ruff format issues
	ruff format

mypy:  ## Run type checks
	mypy

pytest:  ## Run tests with coverage
	pytest --cov --cov-fail-under=100 --cov-branch --cov-report=$(COV_REPORT)

check: ruff-lint ruff-format mypy pytest  ## Run all checks

fix: ruff-lint-fix ruff-format-fix  ## Fix the code style issues

help: ## Display available commands
	echo "Available make commands:"
	echo
	grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m  %-30s\033[0m %s\n", $$1, $$2}'
