DOCKER_COMPOSE_FILES ?= $(shell find . -maxdepth 1 -type f -name "*.yaml" -exec printf -- '-f %s ' {} +; echo)

## ▸▸▸ Docker commands ◂◂◂
.PHONY: config
config:			## Show Docker config
	docker compose ${DOCKER_COMPOSE_FILES} config

.PHONY: build
build:			## Run Docker services
	docker compose ${DOCKER_COMPOSE_FILES} build

.PHONY: up
up:			## Run Docker services
	@COMPOSE_BAKE=true docker compose ${DOCKER_COMPOSE_FILES} up -d --build

.PHONY: down
down:			## Stop Docker services
	docker compose ${DOCKER_COMPOSE_FILES} down --remove-orphans

.PHONY: ps
ps:			## Show Docker containers info
	docker ps --size --all --filter "name=theatre*"