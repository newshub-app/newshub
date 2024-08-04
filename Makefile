PYTHON := poetry run python
MANAGE_PY = $(PYTHON) manage.py

APPS := authnz news
FIXTURES := admin_user categories

DOCKER_IMAGE := ghcr.io/newshub-app/newshub
DOCKER_FILE := docker/Dockerfile
DOCKER_BUILD_OPTS = --pull --load -f $(DOCKER_FILE) --cache-from $(DOCKER_IMAGE):latest
DOCKER_BUILD = docker build $(DOCKER_BUILD_OPTS)

COMPOSE_OPTS = --force-recreate --remove-orphans --build --pull always
PROD_COMPOSE_FILE := docker/docker-compose.yml
DEV_COMPOSE_FILE := docker/docker-compose.dev.yml
PROD_COMPOSE_UP = -f $(PROD_COMPOSE_FILE) up $(COMPOSE_OPTS)
DEV_COMPOSE_UP = -f $(DEV_COMPOSE_FILE) $(PROD_COMPOSE_UP)

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
	@$(MANAGE_PY) genfakedata --users 5 --categories 10 --links 50
.PHONY: fakedata

fakelinks: ## Generate fake links
	@$(MANAGE_PY) genfakedata --links 20
.PHONY: fakelinks

schedules: ## Initialize scheduled tasks
	@$(MANAGE_PY) tasksinit
.PHONY: schedules

static: ## Collect static files
	@$(MANAGE_PY) collectstatic --noinput
.PHONY: static

test: ## Run unit tests
	@$(MANAGE_PY) test --keepdb
.PHONY: tests

#
# Docker
#

images: image-prod image-dev ## Build docker images
.PHONY: images

image-prod: ## Build docker production image
	@$(DOCKER_BUILD) --target prod -t $(DOCKER_IMAGE):latest .
.PHONY: image-prod

image-dev: ## Build docker development image
	@$(DOCKER_BUILD) --target dev -t $(DOCKER_IMAGE):dev .
.PHONY: image-dev

run: image-prod ## Run docker compose stack
	@docker compose $(PROD_COMPOSE_UP)
.PHONY: run

run-dev: image-dev ## Run docker compose stack in dev mode
	@docker compose $(DEV_COMPOSE_UP)
.PHONY: run-dev

docker-shell: ## Run Django shell inside the app container
	@docker compose -p newshub exec app python manage.py shell
.PHONY: docker-shell
