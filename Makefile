.ONESHELL:
TESTS=tests
POETRY=$(shell command -v poetry 2> /dev/null)
ENV_PREFIX=$(shell python3 -c "import pathlib; print('.venv/bin/' if pathlib.Path('.venv/bin/pip').exists() else '')")
PROJECT_NAME=coap_server

.DEFAULT_GOAL := help

.PHONY: all
all: install lint test ## Install dependencies, run linters, and tests.

.PHONY: help
help:             ## Show the help message.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install:          ## Install dependencies using Poetry.
	@if [ -z "$(POETRY)" ]; then \
		echo "Poetry could not be found. See https://python-poetry.org/docs/"; \
		exit 2; \
	fi
	$(POETRY) install
	$(ENV_PREFIX)pre-commit install

.PHONY: fmt
fmt: install       ## Format code using isort & ruff.
	$(ENV_PREFIX)isort $(PROJECT_NAME)/
	$(ENV_PREFIX)ruff format $(PROJECT_NAME)/

.PHONY: lint
lint: install     ## Run mypy and ruff.
	$(ENV_PREFIX)mypy --ignore-missing-imports $(PROJECT_NAME)/
	$(ENV_PREFIX)ruff check --fix $(PROJECT_NAME)/

.PHONY: run
run: install      ## Run the project.
	@if [ -z "$(ENV_PREFIX)" ]; then
		echo "Virtual environment not found."; \
		exit 1; \
	fi
	$(ENV_PREFIX)python -m $(PROJECT_NAME)

.PHONY: test
test: lint        ## Run tests and generate coverage reports.
	$(ENV_PREFIX)pytest -v --cov-config .coveragerc --cov=$(PROJECT_NAME) -l --tb=short --maxfail=1 $(TESTS)/
	$(ENV_PREFIX)coverage xml
	$(ENV_PREFIX)coverage html

.PHONY: clean
clean:            ## Clean project by deleting files in .gitignore.
	git clean -Xdf

.PHONY: docs
docs: install      ## Build and open the documentation.
	@echo "Building documentation ..."
	$(ENV_PREFIX)mkdocs build
	URL="site/index.html"; \
	xdg-open $$URL || sensible-browser $$URL || x-www-browser $$URL || gnome-open $$URL || open $$URL

