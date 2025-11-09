# Docker-only Makefile
# Usa: make <target>
# Targets: help, setup, build, start, stop

.DEFAULT_GOAL := help
SHELL := /bin/bash
COMPOSE := docker compose

.PHONY: help setup build start stop

help: ## Mostra questo help
	@echo "Targets disponibili:"
	@awk 'BEGIN {FS=":.*##"; printf ""} /^[a-zA-Z0-9_\-]+:.*##/ {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: ## Prepara l'ambiente Docker (validate + pull immagini), senza creare .env
	@$(COMPOSE) config >/dev/null
	@echo "docker compose config ✅"
	@$(COMPOSE) pull || true
	@echo "Pull immagini completato ✅"

build: ## Build delle immagini Docker
	@$(COMPOSE) build --pull

start: ## Avvia lo stack in background (backend, ui, postgres, redis)
	@$(COMPOSE) up -d
	@$(COMPOSE) ps

stop: ## Ferma e rimuove i container (conserva i volumi)
	@$(COMPOSE) down
