# Deal Finder

A CLI toolkit for scraping [Carbonite.co.za](https://carbonite.co.za) classifieds and finding deals that match your criteria using LLM-powered filtering.

## How It Works

```mermaid
flowchart LR
    A[Carbonite Forum] -->|scrape_forum.py| B[URLs]
    B -->|fetch_listings.py| C[listings.jsonl]
    C -->|classify.py| D[Matched Listings]
```

1. **Scrape** - Discover listing URLs from forum pages
2. **Fetch** - Extract metadata (title, price, location, specs) into JSONL
3. **Classify** - Use an LLM to filter listings matching your search criteria

## Quick Start

```bash
# Install dependencies
uv sync

# Refresh all configured categories
./refresh.sh --all

# Or refresh a specific category
./refresh.sh monitors
```

## Configuration

Edit `config.json` to define your search targets:

```json
{
  "monitors": {
    "forum": "https://carbonite.co.za/index.php?forums/monitors.9/",
    "output": "listings/monitors.jsonl",
    "query": "27-34 inch 4K IPS monitors in Western Cape under R10000"
  }
}
```

Each target has:
- `forum` - The Carbonite forum URL to scrape
- `output` - Where to store the listings
- `query` - Natural language criteria for LLM filtering (optional)

## Current Categories

| Category | Query |
|----------|-------|
| monitors | 27-34" 4K IPS, Western Cape, under R10k |
| laptops | MacBook M-series, 32GB+ RAM |
| gpu | Upgrade from GTX 1070, Western Cape |
| keyboards | Wireless mechanical, TKL/65%/75%, tactile/linear |
| drones | DJI with camera, Western Cape, under R15k |
| cameras | Sony A6xxx / Fujifilm X-series mirrorless |

## Manual Usage

```bash
# Discover URLs (defaults: 3 pages, 7 days)
uv run python scrape_forum.py --target monitors --pages 15 --days 60

# Fetch metadata from URLs
echo "https://carbonite.co.za/..." | xargs uv run python fetch_listings.py --merge listings/monitors.jsonl

# Classify against criteria
uv run python classify.py listings/monitors.jsonl "4K monitor under R5000"

# Filter with jq
jq -c 'select(.match==true)' listings/monitors.jsonl
```

## Project Structure

```
deal-finder/
├── config.json          # Search targets and criteria
├── refresh.sh           # One-command refresh script
├── scrape_forum.py      # URL discovery from forum pages
├── fetch_listings.py    # Metadata extraction
├── classify.py          # LLM-powered filtering
├── listings.py          # Core fetch/validate functions
└── listings/            # JSONL data files
    ├── monitors.jsonl
    ├── laptops.jsonl
    └── ...
```

## Requirements

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) for dependency management
- [kiro-cli](https://github.com/aws/kiro-cli) for LLM classification
- [jq](https://jqlang.github.io/jq/) for filtering (optional)

## TODO

- [ ] Tighten GPU query — 68 matches is too broad. Add price cap or target specific cards
- [ ] Review laptop (2) and keyboard (5) matches for quality
- [ ] Improve province-less listings — check city field against known WC cities for deterministic filtering
- [ ] Architecture improvements — cron scheduling, Python CLI, web dashboard, or notifications

## Docs

- [Technical Design](docs/technical-design.md) - Architecture details
- [uv Primer](docs/uv-primer.md) - Why we use uv
