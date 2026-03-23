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
├── fb_login.py          # FB cookie export helper (Camoufox)
├── fb_marketplace.py    # FB Marketplace scraper (Camoufox)
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

## Facebook Marketplace (PoC)

Browser automation scraper using [Camoufox](https://camoufox.com/) (stealth Firefox with C++-level fingerprint spoofing). No official API exists for browsing Marketplace listings — this is the only path.

```bash
# First time: log in manually and save cookies
uv run python fb_login.py
# → Log into Facebook in the browser window, then press Enter

# Scrape listings
uv run python fb_marketplace.py --query "GTX 1080" --location capetown
uv run python fb_marketplace.py -q "Sony A6400" -l capetown -o listings/cameras-fb.jsonl
```

Status: core scraper works, pending real-cookie testing and DOM selector tuning. See [FB Marketplace PoC](docs/fb-marketplace-poc.md) for full details.

## TODO

- [ ] Tighten GPU query — 68 matches is too broad. Add price cap or target specific cards
- [ ] Review laptop (2) and keyboard (5) matches for quality
- [ ] Improve province-less listings — check city field against known WC cities for deterministic filtering
- [ ] Architecture improvements — cron scheduling, Python CLI, web dashboard, or notifications

## Docs

- [Technical Design](docs/technical-design.md) - Architecture details
- [FB Marketplace PoC](docs/fb-marketplace-poc.md) - Browser automation integration plan & status
- [uv Primer](docs/uv-primer.md) - Why we use uv
