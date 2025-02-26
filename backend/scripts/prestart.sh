#! /usr/bin/env bash

set -ex

# Check the DB start
python app/app/utils/check_db_conn.py

cd "$(dirname "$0")/.." 

# Run migrations
alembic upgrade head
