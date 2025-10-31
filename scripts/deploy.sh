#!/bin/bash
set -e  # Выход при любой ошибке

ENV_FILE="./.env"

# Обновление кода и деплой backend приложения
pushd ~/Synergy-consultant-AI-DB-layer/ || exit

# Останавливаем старые контейнеры микросервисов и запускаем новые, с обновлённым кодом
docker compose -f docker-compose.yml --env-file $ENV_FILE down --timeout=60 --remove-orphans
docker compose -f docker-compose.yml --env-file $ENV_FILE up --build --detach

popd || exit
