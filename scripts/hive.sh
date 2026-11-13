#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="${PROJECT_DIR}/docker/compose.hive.yaml"
DOCKER_BIN="${DOCKER_BIN:-docker}"

compose() {
  "${DOCKER_BIN}" compose -f "${COMPOSE_FILE}" "$@"
}

command="${1:-status}"
case "${command}" in
  up)
    "${PROJECT_DIR}/scripts/bootstrap_hive.sh"
    compose up -d --wait
    ;;
  down)
    compose down
    ;;
  reset)
    echo "Removing Hive containers and project-owned persistent volumes."
    compose down --volumes
    ;;
  status)
    compose ps
    ;;
  logs)
    compose logs --tail=200 "${2:-hiveserver2}"
    ;;
  smoke)
    compose exec \
      -e 'JAVA_TOOL_OPTIONS=--enable-preview --enable-native-access=ALL-UNNAMED' \
      hiveserver2 /opt/hive/bin/beeline \
      -u 'jdbc:hive2://127.0.0.1:10000/default' \
      --silent=true \
      --showHeader=true \
      -e "SELECT version() AS hive_version, current_timestamp AS checked_at"
    ;;
  beeline)
    compose exec hiveserver2 /opt/hive/bin/beeline \
      -u 'jdbc:hive2://127.0.0.1:10000/default'
    ;;
  *)
    echo "Usage: $0 {up|down|reset|status|logs [service]|smoke|beeline}" >&2
    exit 2
    ;;
esac

