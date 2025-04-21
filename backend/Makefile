SHELL := bash

.PHONY: default
default: help

.PHONY: help
help:
	@grep -E '^[a-zA-Z_.-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

requirements.txt: requirements.in ## Builds prod requirements.txt based on requirements.in
	@pip-compile -q --strip-extras requirements.in

requirements-dev.txt: requirements.txt requirements-dev.in ## Main way to add dependencies (builds both dev and prod requirements)
	@pip-compile -q --strip-extras requirements-dev.in

.PHONY: setup-dev
setup-dev: ## Setupping latest version of the environment for development
	@pip install -r requirements.txt -r requirements-dev.txt

.PHONY: setup
setup: ## Setupping latest version of the production environment
	@pip install -r requirements.txt

.PHONY: run
run: ## Run backend
	@fastapi dev app.py
