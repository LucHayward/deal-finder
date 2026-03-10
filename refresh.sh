#!/bin/bash
# One-click refresh: discover new listings and merge into DB
set -euo pipefail
cd "$(dirname "$0")"

CONCURRENCY=1
PARALLEL=1

refresh_target() {
    local TARGET="$1"
    DB=$(python3 -c "import json; print(json.load(open('config.json'))['$TARGET']['output'])")
    PAGES=15
    DAYS=60

    URLS=$(uv run python scrape_forum.py --target "$TARGET" --db "$DB" --pages "$PAGES" --days "$DAYS")

    if [ -z "$URLS" ]; then
        echo "No new listings found." >&2
        return 0
    fi

    echo "$URLS" | xargs uv run python fetch_listings.py --merge "$DB" -c "$CONCURRENCY"

    # Classify if a query is configured
    read -r QUERY PROVINCE < <(python3 -c "
import json; c=json.load(open('config.json'))['$TARGET']
print(c.get('query') or '', '\t', c.get('province') or '')
")
    if [ -n "$QUERY" ]; then
        CLASSIFY_ARGS=(uv run python classify.py "$DB" "$QUERY" --parallel "$PARALLEL" --only-new)
        [ -n "$PROVINCE" ] && CLASSIFY_ARGS+=(--province "$PROVINCE")
        "${CLASSIFY_ARGS[@]}"
    fi
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--concurrency) CONCURRENCY="$2"; shift 2 ;;
        -p|--parallel) PARALLEL="$2"; shift 2 ;;
        --all) ALL=1; shift ;;
        *) TARGET="$1"; shift ;;
    esac
done

if [ "${ALL:-}" = "1" ]; then
    for T in $(python3 -c "import json; print(' '.join(json.load(open('config.json')).keys()))"); do
        echo "=== Refreshing $T ==="
        refresh_target "$T"
    done
else
    refresh_target "${TARGET:-monitors}"
fi
