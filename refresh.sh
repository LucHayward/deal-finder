#!/bin/bash
# One-click refresh: discover new listings and merge into DB
set -euo pipefail
cd "$(dirname "$0")"

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

    echo "$URLS" | xargs uv run python fetch_listings.py --merge "$DB"

    # Classify if a query is configured
    QUERY=$(python3 -c "import json; q=json.load(open('config.json'))['$TARGET'].get('query'); print(q or '')")
    if [ -n "$QUERY" ]; then
        uv run python classify.py "$DB" "$QUERY"
    fi
}

if [ "${1:-}" = "--all" ]; then
    for TARGET in $(python3 -c "import json; print(' '.join(json.load(open('config.json')).keys()))"); do
        echo "=== Refreshing $TARGET ==="
        refresh_target "$TARGET"
    done
else
    refresh_target "${1:-monitors}"
fi
