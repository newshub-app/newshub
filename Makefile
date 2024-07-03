PYTHON := poetry run python
MANAGE_PY := $(PYTHON) manage.py

APPS := authnz news
FIXTURES := admin_user categories

DOCKER_IMAGE_NAME := ghcr.io/newshub-app/newshub
DOCKER_IMAGE_TAG := latest
DOCKER_IMAGE := $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG)

PROD_COMPOSE_FILE := -f docker-compose.yml
DEV_COMPOSE_FILE := $(PROD_COMPOSE_FILE) -f docker-compose.dev.yml

all: image
.PHONY: all

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.PHONY: help

#
# Django
#

superuser: ## Create application admin
	@$(MANAGE_PY) createsuperuser
.PHONY: docker-create-superuser

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
	@$(MANAGE_PY) genfakedata --users --categories --links
.PHONY: fakedata

fakelinks: ## Generate fake links
	@$(MANAGE_PY) genfakedata --links --num-links 20

static: ## Collect static files
	@$(MANAGE_PY) collectstatic --noinput
.PHONY: static

test: ## Run unit tests
	@$(MANAGE_PY) test --keepdb
.PHONY: tests

#
# Docker
#

image: ## Build docker image
	@docker build --target production -t $(DOCKER_IMAGE) --pull --load .
.PHONY: image

image-dev: ## Build docker development image
	@docker build --target development -t $(DOCKER_IMAGE) --pull --load .

run: image ## Run docker compose stack
	@docker compose up
.PHONY: run

run-dev: image ## Run docker compose stack in dev mode
	@docker compose $(DEV_COMPOSE_FILE) up
.PHONY: run-dev
