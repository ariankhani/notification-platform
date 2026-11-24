#!/bin/sh
set -eu

cd /app/alembic
/app/.venv/bin/alembic upgrade head
cd /app

exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --reload
