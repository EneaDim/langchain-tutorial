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

test-db: ## Testa scrittura/lettura su Postgres
	@docker compose exec -T postgres psql -U ai -d ai_doc -c "SELECT count(*) AS jobs_before FROM jobs;" || true
	@curl -s -F "file=@sample.pdf" http://localhost:8000/analyze > /dev/null
	@docker compose exec -T postgres psql -U ai -d ai_doc -c "SELECT count(*) AS jobs_after FROM jobs;"
	@docker compose exec -T postgres psql -U ai -d ai_doc -c "SELECT id, filename, left(summary,80) AS summary_prefix FROM jobs ORDER BY id DESC LIMIT 3;"

test-cache: ## Testa cache Redis (MISS vs HIT)
	@docker compose exec -T redis redis-cli FLUSHALL >/dev/null || true
	@curl -s -w "\nMISS_TIME=%{time_total}\n" -F "file=@sample.pdf" http://localhost:8000/analyze > /dev/null
	@curl -s -w "\nHIT_TIME=%{time_total}\n"  -F "file=@sample.pdf" http://localhost:8000/analyze > /dev/null
	@docker compose exec -T redis redis-cli --scan | head -n3 || true
	@$(COMPOSE) down

logs: ## Mostra i log
	@$(COMPOSE) logs -f --tail=200

clear-db: ## Drop all DB data and cache, then recreate schema
	@echo "🚨 Clearing PostgreSQL schema and Redis cache..."
	@docker compose exec -T postgres bash -lc 'psql -U ai -d ai_doc -v "ON_ERROR_STOP=1" -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO ai; GRANT ALL ON SCHEMA public TO public;"'
	@docker compose exec -T redis redis-cli FLUSHALL >/dev/null
	@echo "🧱 Recreating tables..."
	@docker compose exec -T backend python -c "from app.models.db import engine; from app.models.job import Job; Job.metadata.create_all(bind=engine); print('Schema recreated successfully.')"
	@echo "✅ Done."
