PYTHON := poetry run python
MANAGE_PY := $(PYTHON) manage.py

APPS := authnz news
FIXTURES := admin_user categories

DOCKER_IMAGE_NAME := ghcr.io/newshub-app/newshub
DOCKER_IMAGE_TAG := latest
DOCKER_IMAGE := $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)

PROD_COMPOSE_FILE := -f docker-compose.yml
DEV_COMPOSE_FILE := $(PROD_COMPOSE_FILE) -f docker-compose.dev.yml

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
.PHONY: loaddata

fakedata: ## Generate fake data
	@$(MANAGE_PY) genfakedata
.PHONY: fakedata

static: ## Collect static files
	@$(MANAGE_PY) collectstatic --noinput
.PHONY: static

test: ## Run unit tests
	@$(MANAGE_PY) test --keepdb
.PHONY: tests

#
# Docker
#

docker-image: ## Build docker image
	@docker build -t $(DOCKER_IMAGE) --pull --load .
.PHONY: docker-image

docker-run: docker-image ## Run docker compose stack
	@docker compose up
.PHONY: docker-run

docker-run-dev: docker-image ## Run docker compose stack in dev mode
	@docker compose $(DEV_COMPOSE_FILE) up
.PHONY: docker-run-dev

docker-create-superuser: ## Create superuser in docker container
	@docker compose exec -it app python manage.py createsuperuser
.PHONY: docker-create-superuser

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help
