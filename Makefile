PYTHON := poetry run python
MANAGE_PY := $(PYTHON) manage.py
APPS := authnz news #api
FIXTURES := admin_user categories
SAMPLE_FIXTURES := sample_links

#
# Django
#

run: ## Run django development server
	@$(MANAGE_PY) runserver
.PHONY: run

migrations: ## Generate database migrations
	@$(MANAGE_PY) makemigrations $(APPS)
.PHONY: migrations

migrate: migrations ## Apply database migrations
	@$(MANAGE_PY) migrate
.PHONY: migrate

loaddata: ## Load database fixtures
	@$(MANAGE_PY) loaddata $(FIXTURES)

loadsamples: loaddata ## Load sample data
	@$(MANAGE_PY) loaddata $(SAMPLE_FIXTURES)

static: ## Collect static files
	@$(MANAGE_PY) collectstatic --noinput
.PHONY: static

test: ## Run unit tests
	@$(MANAGE_PY) test

#
# Docker
#

docker-image: ## Build docker image
	@docker compose build --pull

docker-run: docker-image ## Run docker compose stack
	@docker compose up

docker-run-dev: docker-image ## Run docker compose stack in dev mode
	@docker compose -f docker-compose.yml -f docker-compose.dev.yml up

docker-create-superuser: ## Create superuser in docker container
	@docker compose exec -it app python manage.py createsuperuser

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
