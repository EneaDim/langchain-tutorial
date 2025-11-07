# Makefile for Smart Report Writer
# Usage:
#   make [PROFILE=dev|prod] <target>
# Examples:
#   make start
#   make PROFILE=prod start
#   make log LOG_SERVICE=api

SHELL := /bin/bash

PROJECT ?= smart-report-writer
COMPOSE ?= docker compose
PROFILE ?= dev
LOG_SERVICE ?= api

ifeq ($(PROFILE),prod)
COMPOSE_FILES := -f docker-compose.yaml -f docker-compose.prod.yaml
else
COMPOSE_FILES := -f docker-compose.yaml -f docker-compose.dev.yaml
endif

.PHONY: start stop build log clean help

start: ## Start the stack in detached mode (PROFILE=dev|prod)
	$(COMPOSE) $(COMPOSE_FILES) up -d

stop: ## Stop the stack (keeps named volumes)
	$(COMPOSE) $(COMPOSE_FILES) down

build: ## Build (or rebuild) all images for the selected profile
	$(COMPOSE) $(COMPOSE_FILES) build

log: ## Tail logs for a service (set LOG_SERVICE=name, default: api)
	$(COMPOSE) $(COMPOSE_FILES) logs -f $(LOG_SERVICE)

clean: ## Stop and remove containers, networks, and volumes; prune dangling images
	$(COMPOSE) $(COMPOSE_FILES) down -v
	docker image prune -f

help: ## Show this help
	@echo "Usage: make [PROFILE=dev|prod] <target>"
	@echo
	@echo "Current profile: $(PROFILE)"
	@echo
	@awk 'BEGIN {FS = ":.*##"; printf "Targets:\n"} /^[a-zA-Z0-9_.-]+:.*##/ { printf "  \033[36m%-12s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

