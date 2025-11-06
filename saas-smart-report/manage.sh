#!/usr/bin/env bash
set -Eeuo pipefail

API_PORT_STD=8000
UI_PORT_STD=8501

exists(){ [ -f "$1" ]; }

compose_args() {
  local f; local args=()
  for f in \
    docker-compose.yaml \
    docker-compose.override.fix-build.yml \
    docker-compose.override.dev.yml \
    docker-compose.override.redis.yml \
    docker-compose.override.minio.yml \
    docker-compose.override.db.yml \
    docker-compose.override.env.yml \
    docker-compose.override.ports.yml \
    docker-compose.override.fix-dns.yml \
    docker-compose.override.add-api.yml \
    docker-compose.override.ollama.yml \
    docker-compose.override.ports-alt.yml
  do
    exists "$f" && args+=( -f "$f" )
  done
  echo "${args[@]}"
}

start() {
  docker compose $(compose_args) up -d --build db redis minio createbucket api ui
  echo "[ok] stack up"
  sleep 3
  echo "[health] host → http://localhost:${API_PORT_STD}/health/liveness"
  curl -sf "http://localhost:${API_PORT_STD}/health/liveness" && echo || true
  echo "[hint] UI → http://localhost:${UI_PORT_STD}"
}

stop()   { docker compose $(compose_args) down --remove-orphans; }
clean()  { docker compose $(compose_args) down -v --remove-orphans; }
ps()     { docker compose $(compose_args) ps; }
logs()   { docker compose $(compose_args) logs -f api worker ui || docker compose $(compose_args) logs -f api ui; }
health() { curl -sf "http://localhost:${1:-$API_PORT_STD}/health/liveness" && echo || { echo "[err] health failed"; exit 1; }; }

case "${1:-}" in
  start)  start ;;
  stop)   stop  ;;
  clean)  clean ;;
  ps)     ps    ;;
  logs)   logs  ;;
  health) shift || true; health "${1:-}";;
  *) echo "Usage: $0 {start|stop|clean|ps|logs|health}"; exit 1 ;;
esac
