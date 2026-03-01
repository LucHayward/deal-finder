#!/bin/bash
# Semantic filter using a cheap LLM
# Usage: ./filter.sh <jsonl_file> "<query>"
FILE="$1"
QUERY="$2"
MODEL="${3:-glm-4.7-flash}"

echo "Filter: $QUERY (using $MODEL)" >&2
echo "Identify listings matching: $QUERY. Output ONLY matching JSON lines, no explanation:

$(jq -c '{title, price, city, province}' "$FILE")" | kiro-cli chat --model "$MODEL" --no-interactive 2>&1 | grep -E '^\{'
