#!/usr/bin/env bash
# Daily report runner for FW-Engineering-AI-System.
# Sets required env (Redmine creds, embedding model, append mode -> issue #68)
# and invokes the report script with the project venv python.
# Scheduled via cron (nightly). Keeps secrets out of the crontab line.
set -euo pipefail

PROJ="/home/alex_chiang/projects/FW-Engineering-AI-System"

# Redmine credentials: reuse ProBiz-CompanySim/.env (single source of truth).
# Export REDMINE_URL / REDMINE_API_KEY from it without printing them.
PROBIZ_ENV="/home/alex_chiang/projects/ProBiz-CompanySim/.env"
if [ -f "$PROBIZ_ENV" ]; then
    export REDMINE_URL="$(grep -E '^REDMINE_URL=' "$PROBIZ_ENV" | head -1 | cut -d= -f2-)"
    export REDMINE_API_KEY="$(grep -E '^REDMINE_API_KEY=' "$PROBIZ_ENV" | head -1 | cut -d= -f2-)"
fi

export EMBEDDING_MODEL="BAAI/bge-m3"
export REPORT_REDMINE_MODE="append"
export REPORT_REDMINE_ISSUE_ID="68"
export REPORT_REDMINE_PROJECT_ID="24"

cd "$PROJ"
exec "$PROJ/.venv/bin/python" scripts/daily_report.py
