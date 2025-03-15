#! /usr/bin/env bash

set -ex

cd "$(dirname "$0")/.." 


alembic upgrade head || exit 1

isort app && ruff format app


