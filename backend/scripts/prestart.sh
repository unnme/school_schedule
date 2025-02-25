#! /usr/bin/env bash

set -e
set -x

# Check the DB start
python app/app/backend_pre_start.py

# Change to project root (app/) to ensure alembic.ini is found
cd "$(dirname "$0")/.." 

# Run migrations
alembic upgrade head

# Create initial data in DB
# python app/initial_data.py
