SHELL := /usr/bin/bash
PYENV_VER := 3.10.6
NAME := $$(basename $$PWD)
ENV_NAME := $(PYENV_VER)/envs/$(NAME)
DB_IMAGE_NAME := test-db
DB_IMAGE_TAG := latest

.DEFAULT_GOAL := help

env: ## Install the development environment
	@pyenv install -s $(PYENV_VER)
	@pyenv virtualenv $(PYENV_VER) $(NAME)
	@ln -s $$(pyenv root)/versions/$(NAME) .venv
	@source $${PWD}/.venv/bin/activate
	@poetry install

rmenv: ## Remove the local development environment
	@pyenv virtualenv-delete -f $(ENV_NAME)
	@rm -f .venv

kill: ## Teardown local containers
	-@docker compose -f docker-compose.src.yml -f docker-compose.subset.yml -f docker-compose.factory.yml down --remove-orphans
	-@docker kill test_db

src: ## Build and populate the source database
	@docker compose -f docker-compose.src.yml -f docker-compose.factory.yml up --remove-orphans --build factory

subset: ## Build a destination database and subset it with data from the source
	@docker compose -f docker-compose.src.yml -f docker-compose.subset.yml up --remove-orphans --build subset

archive: ## Create a backup of the destination database
	@docker exec -it dst_db /usr/bin/bash -c "mariabackup --user=root --password=toor --backup --stream=xbstream | zstd > /host-mnt/music.zst"

image: ## Build a database image with the backup initialized
	@docker build -t $(DB_IMAGE_NAME):$(DB_IMAGE_TAG) -f db-build/Dockerfile .

database: subset archive image ## Create a database image with the desired data subset
	@echo ""

help:
	@echo "Utilities for the $(NAME) package using python $(PYENV_VER)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
 