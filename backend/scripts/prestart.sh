#! /usr/bin/env bash

set -ex

# Check the DB start
python app/app/utils/db_utils.py

cd "$(dirname "$0")/.." 

# Run migrations
alembic upgrade head
