#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="${PROJECT_DIR}/docker/compose.postgres.yaml"
DOCKER_BIN="${DOCKER_BIN:-docker}"

compose() {
  "${DOCKER_BIN}" compose -f "${COMPOSE_FILE}" "$@"
}

command="${1:-status}"
case "${command}" in
  up)
    compose up -d --wait
    ;;
  down)
    compose down
    ;;
  reset)
    echo "Removing the PostgreSQL validation container and project-owned volume."
    compose down --volumes
    ;;
  status)
    compose ps
    ;;
  logs)
    compose logs --tail=200 postgres
    ;;
  smoke)
    compose exec postgres psql \
      --username postgres \
      --dbname dsv_validation \
      --command "SELECT version(), current_setting('TimeZone') AS timezone"
    ;;
  psql)
    compose exec postgres psql --username postgres --dbname dsv_validation
    ;;
  *)
    echo "Usage: $0 {up|down|reset|status|logs|smoke|psql}" >&2
    exit 2
    ;;
esac
