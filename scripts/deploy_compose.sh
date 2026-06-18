#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

APP_DIR="${APP_DIR:-${GITHUB_WORKSPACE:-$REPO_ROOT}}"
COMPOSE_FILE="${COMPOSE_FILE:-compose.prod.yaml}"
HEALTH_URL="${HEALTH_URL:-http://127.0.0.1:8080/health}"

echo "[deploy] app dir: ${APP_DIR}"
echo "[deploy] compose file: ${COMPOSE_FILE}"
echo "[deploy] health url: ${HEALTH_URL}"
echo "[deploy] image name: ${IMAGE_NAME:-not set}"

cd "${APP_DIR}"

if [ ! -f "${COMPOSE_FILE}" ]; then
  echo "[deploy] ERROR: compose file not found: ${APP_DIR}/${COMPOSE_FILE}"
  exit 1
fi

echo "[deploy] pull image"
docker compose -f "${COMPOSE_FILE}" pull

echo "[deploy] start service"
docker compose -f "${COMPOSE_FILE}" up -d

echo "[deploy] show service status"
docker compose -f "${COMPOSE_FILE}" ps

echo "[deploy] wait for service"
sleep 5

echo "[deploy] check health"
curl -f "${HEALTH_URL}"

echo "[deploy] clean old images"
docker image prune -f

echo "[deploy] done"