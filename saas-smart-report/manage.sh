#!/usr/bin/env bash
set -Eeuo pipefail

# === Config ===
PROJECT_NAME="${COMPOSE_PROJECT_NAME:-srw}"
API_PORT_STD=8000
UI_PORT_STD=8501
API_PORT_ALT=8001
UI_PORT_ALT=8502

# Add MinIO ports (STD and ALT)
MINIO_PORT_STD=9000
MINIO_CONSOLE_PORT_STD=9001
MINIO_PORT_ALT=9002
MINIO_CONSOLE_PORT_ALT=9003

# Compose files we’ll include if present (in this order)
COMPOSE_ORDER=(
  "docker-compose.yaml"
  "docker-compose.override.fix-build.yml"
  "docker-compose.override.dev.yml"
  "docker-compose.override.redis.yml"
  "docker-compose.override.minio.yml"
  "docker-compose.override.db.yml"
  "docker-compose.override.env.yml"
)
# Optional extras (included when requested and present)
OLLAMA_FILE="docker-compose.override.ollama.yml"
PORTS_STD_FILE="docker-compose.override.ports.yml"
PORTS_ALT_FILE="docker-compose.override.ports-alt.yml"

# === Helpers ===
exists() { [ -f "$1" ]; }

compose_args() {
  local args=()
  for f in "${COMPOSE_ORDER[@]}"; do
    exists "$f" && args+=( -f "$f" )
  done
  # optional extras passed as "$@"
  for f in "$@"; do
    exists "$f" && args+=( -f "$f" )
  done
  echo "${args[@]}"
}

port_in_use() {
  # usage: port_in_use 8000
  ss -ltn "( sport = :$1 )" 2>/dev/null | grep -q ":$1"
}

ensure_ports_alt_file() {
  if ! exists "$PORTS_ALT_FILE"; then
    cat > "$PORTS_ALT_FILE" <<YAML
services:
  api:    { ports: ["${API_PORT_ALT}:${API_PORT_STD}"] }
  ui:     { ports: ["${UI_PORT_ALT}:${UI_PORT_STD}"] }
  minio:
    ports:
      - "${MINIO_PORT_ALT}:${MINIO_PORT_STD}"
      - "${MINIO_CONSOLE_PORT_ALT}:${MINIO_CONSOLE_PORT_STD}"
YAML
    echo "[info] Created ${PORTS_ALT_FILE} (API:${API_PORT_ALT}, UI:${UI_PORT_ALT}, MinIO:${MINIO_PORT_ALT}/${MINIO_CONSOLE_PORT_ALT})"
  fi
}

ensure_env_file() {
  if ! exists ".env" && exists ".env.example"; then
    cp .env.example .env
    echo "[info] .env was missing → copied from .env.example"
  fi
}

# === Commands ===

start_host() {
  ensure_env_file

  local extra_ports=()
  # If ANY standard port is busy (API, UI, or MinIO), switch to ALT
  if port_in_use "$API_PORT_STD" || port_in_use "$UI_PORT_STD" || port_in_use "$MINIO_PORT_STD" || port_in_use "$MINIO_CONSOLE_PORT_STD"; then
    echo "[warn] Standard ports busy → switching to alt ports (API:${API_PORT_ALT}, UI:${UI_PORT_ALT}, MinIO:${MINIO_PORT_ALT}/${MINIO_CONSOLE_PORT_ALT})"
    ensure_ports_alt_file
    extra_ports+=( "$PORTS_ALT_FILE" )
  elif exists "$PORTS_STD_FILE"; then
    extra_ports+=( "$PORTS_STD_FILE" )
  fi

  # Expect host Ollama on 127.0.0.1:11434
  export OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://host.docker.internal:11434}"

  docker compose $(compose_args "${extra_ports[@]}") \
    up -d --build db redis minio createbucket api worker ui

  echo "[ok] Stack up. API health:"
  local api_port=$API_PORT_STD
  if port_in_use "$API_PORT_ALT"; then api_port=$API_PORT_ALT; fi
  curl -sf "http://localhost:${api_port}/health/liveness" && echo || true

  local ui_port=$UI_PORT_STD
  if port_in_use "$UI_PORT_ALT"; then ui_port=$UI_PORT_ALT; fi
  echo "[hint] UI → http://localhost:${ui_port}"
}

start_internal_ollama() {
  ensure_env_file

  local extra=( "$OLLAMA_FILE" )
  local extra_ports=()
  if port_in_use "$API_PORT_STD" || port_in_use "$UI_PORT_STD" || port_in_use "$MINIO_PORT_STD" || port_in_use "$MINIO_CONSOLE_PORT_STD"; then
    echo "[warn] Standard ports busy → switching to alt ports (API:${API_PORT_ALT}, UI:${UI_PORT_ALT}, MinIO:${MINIO_PORT_ALT}/${MINIO_CONSOLE_PORT_ALT})"
    ensure_ports_alt_file
    extra_ports+=( "$PORTS_ALT_FILE" )
  elif exists "$PORTS_STD_FILE"; then
    extra_ports+=( "$PORTS_STD_FILE" )
  fi

  # Containers will talk to internal ollama service
  export OLLAMA_BASE_URL="${OLLAMA_BASE_URL:-http://ollama:11434}"

  docker compose $(compose_args "${extra[@]}" "${extra_ports[@]}") \
    up -d --build db redis minio createbucket api worker ui ollama

  echo "[ok] Stack (with internal Ollama) up. API health:"
  local api_port=$API_PORT_STD
  if port_in_use "$API_PORT_ALT"; then api_port=$API_PORT_ALT; fi
  curl -sf "http://localhost:${api_port}/health/liveness" && echo || true

  local ui_port=$UI_PORT_STD
  if port_in_use "$UI_PORT_ALT"; then ui_port=$UI_PORT_ALT; fi
  echo "[hint] UI → http://localhost:${ui_port}"
}

stop() {
  docker compose $(compose_args) down --remove-orphans
}

clean() {
  docker compose $(compose_args) down -v --remove-orphans
}

rebuild() {
  docker compose $(compose_args) build --no-cache api worker ui
}

status() {
  docker compose $(compose_args) ps
}

logs() {
  docker compose $(compose_args) logs -f api worker ui
}

health() {
  local port="${1:-$API_PORT_STD}"
  curl -sf "http://localhost:${port}/health/liveness" && echo || { echo "[err] health failed on ${port}"; exit 1; }
}

usage() {
  cat <<EOF
Usage: $0 <command>

Commands:
  start-host          Start stack using HOST Ollama (http://host.docker.internal:11434)
  start-internal      Start stack with internal Ollama service
  stop                Stop containers (keeps volumes)
  clean               Stop and remove containers + volumes (destructive)
  rebuild             Rebuild api/worker/ui images (no cache)
  status              Show docker compose ps
  logs                Tail api/worker/ui logs
  health [port]       Check API health (default port ${API_PORT_STD})

Notes:
- If ports ${MINIO_PORT_STD}/${MINIO_CONSOLE_PORT_STD} are busy, MinIO will be mapped to ${MINIO_PORT_ALT}/${MINIO_CONSOLE_PORT_ALT}.

Examples:
  $0 start-host
  $0 start-internal
  $0 stop
  $0 clean
  $0 rebuild
  $0 status
  $0 logs
  $0 health 8001
EOF
}

cmd="${1:-}"
case "${cmd}" in
  start-host)       start_host ;;
  start-internal)   start_internal_ollama ;;
  stop)             stop ;;
  clean)            clean ;;
  rebuild)          rebuild ;;
  status)           status ;;
  logs)             logs ;;
  health)           shift || true; health "${1:-}";;
  *)                usage; exit 1 ;;
esac
