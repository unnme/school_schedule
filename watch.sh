#!/usr/bin/env sh
set -e

while true; do
  docker-compose up --watch
  echo "❌ Контейнер завершился! Перезапуск через 10 секунд..."
  sleep 10
done
