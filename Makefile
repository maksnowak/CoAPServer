.ONESHELL:
TESTS=tests
POETRY=$(shell command -v poetry 2> /dev/null)
ENV_PREFIX=$(shell python -c "if __import__('pathlib').Path('.venv/bin/pip').exists(): print('.venv/bin/')")
PROJECT_NAME=$(PROJECT_NAME)

.DEFAULT_GOAL := help

.PHONY: all
all: install lint test

.PHONY: help
help:             ## Show the help.
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@fgrep "##" Makefile | fgrep -v fgrep

.PHONY: install
install: 
    @if [ -z $(POETRY) ]; then echo "Poetry could not be found. See https://python-poetry.org/docs/"; exit 2; fi
    $(POETRY) install

.PHONY: fmt
fmt:              ## Format code using ruff & isort.
	$(ENV_PREFIX)isort $(PROJECT_NAME)/
	$(ENV_PREFIX)ruff format $(PROJECT_NAME)/

.PHONY: lint
lint:             ## Run pep8, ruff, mypy linters.
	$(ENV_PREFIX)flake8 $(PROJECT_NAME)/
	$(ENV_PREFIX)mypy --ignore-missing-imports $(PROJECT_NAME)/
	$(ENV_PREFIX)ruff check --fix $(PROJECT_NAME)/


.PHONY: test
test: lint        ## Run tests and generate coverage report.
	$(ENV_PREFIX)pytest -v --cov-config .coveragerc --cov=$(PROJECT_NAME) -l --tb=short --maxfail=1 tests/
	$(ENV_PREFIX)coverage xml
	$(ENV_PREFIX)coverage html

.PHONY: clean
clean:
    # Delete all files in .gitignore
    git clean -Xdf

.PHONY: docs
docs:             ## Build the documentation.
	@echo "building documentation ..."
	@$(ENV_PREFIX)mkdocs build
	URL="site/index.html"; xdg-open $$URL || sensible-browser $$URL || x-www-browser $$URL || gnome-open $$URL || open $$URL
