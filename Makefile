PYTHON := poetry run python
MANAGE_PY := $(PYTHON) manage.py
APPS := api news

run: ## Run django development server
	@$(MANAGE_PY) runserver
.PHONY: run

migrations: ## Generate database migrations
	@$(MANAGE_PY) makemigrations $(APPS)
.PHONY: migrations

migrate: migrations ## Apply database migrations
	@$(MANAGE_PY) migrate
.PHONY: migrate

fixtures: ## Generate database fixtures
	@$(MANAGE_PY) dumpdata --indent 2 news.Category > news/fixtures/categories.json

loaddata: ## Load database fixtures
	@$(MANAGE_PY) loaddata

static: ## Collect static files
	@$(MANAGE_PY) collectstatic --noinput
.PHONY: static

test: ## Run unit tests
	@$(MANAGE_PY) test

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help