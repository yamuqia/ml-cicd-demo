#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${APP_DIR:-$HOME/projects/ml-cicd-demo}"
COMPOSE_FILE="${COMPOSE_FILE:-compose.prod.yaml}"
HEALTH_URL="${HEALTH_URL:-http://127.0.0.1:8080/health}"

echo "[deploy] app dir: ${APP_DIR}"

cd "${APP_DIR}"

echo "[deploy] update repository"
git fetch origin main
git reset --hard origin/main

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
