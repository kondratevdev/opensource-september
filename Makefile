SHELL := /usr/bin/env bash

.DEFAULT_GOAL := help

.PHONY: help ci lint mypy

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*## "; printf "Usage: make <target>\n\nTargets:\n"} /^[a-zA-Z_-]+:.*## / {printf "  %-12s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

ci: lint mypy ## Run all CI checks

lint: ## Run all linters
	ruff check --exit-non-zero-on-fix
	ruff format --check --diff
	flake8 .
	import-linter lint

mypy: ## Run mypy type checking
	mypy .
