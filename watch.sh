#!/usr/bin/env sh
set -e

while true; do
    docker-compose up --watch
    echo "❌ Контейнер завершился! Перезапуск через 5 секунд..."
    sleep 5
done
