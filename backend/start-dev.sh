#!/usr/bin/env bash
set -e


exec /app/.venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
