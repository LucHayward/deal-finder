# Multi-Source Scraper Expansion Plan

**Date:** 2026-03-17
**Status:** In Progress

## Overview

Expand deal-finder beyond Carbonite.co.za to scrape retail e-commerce sites for new/retail pricing alongside the existing second-hand classifieds. This enables price comparison between new and used markets.

## Current Architecture

```
config.json → scrape_forum.py → fetch_listings.py → listings.jsonl → classify.py
                (Carbonite-specific)  (Carbonite-specific)
```

Everything is hardcoded to Carbonite's forum HTML structure. `scrape_forum.py` discovers URLs from forum pages, `listings.py` extracts metadata from individual listing pages, and `fetch_listings.py` orchestrates fetching.

## Target Architecture

```
config.json → scrapers/<site>.py → fetch_listings.py → listings.jsonl → classify.py
               (per-site impl)      (source-agnostic)
```

Each site gets its own scraper module implementing a common interface. The pipeline remains the same but becomes source-aware.

## Target Sites

### Phase 1 (This Sprint)

| Site | Domain | Type | Categories | Platform | Notes |
|------|--------|------|------------|----------|-------|
| Orms Direct | ormsdirect.co.za | Retail | Cameras, Lenses | Shopify | `/collections/mirrorless-cameras`, `/collections/zoom-lenses`, `/collections/prime-lenses` |
| Cameraland | cameraland.co.za | Retail | Cameras, Lenses | Shopify | `/collections/mirrorless`, `/collections/zoom-lenses`, `/collections/prime-lenses` |
| Evetech | evetech.co.za | Retail | Monitors | Custom ASP.NET | `/components/monitor-87.aspx`, product pages at `/product-slug/best-deal/ID` |
| Wootware | wootware.co.za | Retail | Monitors | Custom | `/monitors-screens`, returns 403 to basic fetch — may need browser/headers |

### Phase 2 (Future)

| Site | Domain | Type | Notes |
|------|--------|------|-------|
| Takealot | takealot.com | Marketplace | Has API-like endpoints, existing scrapers on GitHub (`SilverCode/takealot`) |
| Amazon SA | amazon.co.za | Marketplace | Amazon MCP server exists (`Fewsats/amazon-mcp`), also `oxylabs/amazon-scraper` |

## Tasks

### Task 1: Scraper Interface & Registry

Create a base scraper interface and a registry that maps source names to implementations.

**File:** `scrapers/__init__.py`, `scrapers/base.py`

```python
# scrapers/base.py
class Scraper:
    """Base interface for all site scrapers."""
    def discover(self, url: str, **kwargs) -> list[dict]:
        """Discover products from a category/listing page.
        Returns list of dicts with at minimum: url, title, price, source."""
        raise NotImplementedError

    def fetch(self, url: str) -> dict:
        """Fetch full product details from a single product page.
        Returns dict with: url, title, price, status, source, fetched_at, and site-specific fields."""
        raise NotImplementedError
```

**Acceptance:** Existing Carbonite scraping refactored into `scrapers/carbonite.py` implementing this interface. All existing tests/workflows still work.

### Task 2: Add `source` Field to Data Model

Update the data pipeline to track where each listing came from.

**Changes:**
- Every record in JSONL gets a `source` field (e.g. `"carbonite"`, `"orms"`, `"evetech"`)
- `config.json` entries get a `source` field (defaults to `"carbonite"` for existing entries)
- `fetch_listings.py` passes source through
- `classify.py` and `filter.sh` remain source-agnostic (no changes needed)
- Backfill existing JSONL files with `"source": "carbonite"`

**Acceptance:** `jq '.source' listings/monitors.jsonl` returns `"carbonite"` for all existing records.

### Task 3: Config Schema Update

Extend `config.json` to support multiple sources per category.

**Current:**
```json
{
  "monitors": {
    "forum": "https://carbonite.co.za/...",
    "output": "listings/monitors.jsonl",
    "query": "..."
  }
}
```

**New:**
```json
{
  "monitors": {
    "sources": [
      {
        "name": "carbonite",
        "type": "carbonite",
        "url": "https://carbonite.co.za/index.php?forums/monitors.9/"
      },
      {
        "name": "evetech",
        "type": "evetech",
        "url": "https://www.evetech.co.za/components/monitor-87.aspx"
      },
      {
        "name": "wootware",
        "type": "wootware",
        "url": "https://www.wootware.co.za/monitors-screens"
      }
    ],
    "output": "listings/monitors.jsonl",
    "query": "27-34 inch 4K IPS monitors under R10000",
    "province": "Western Cape"
  }
}
```

**Backward compat:** If `sources` is absent, treat `forum` as a single Carbonite source (migration path).

**Acceptance:** `refresh.sh` works with both old and new config format.

### Task 4: Shopify Scraper (Orms + Cameraland)

Both Orms Direct and Cameraland run on Shopify. Shopify exposes a standard JSON API:
- Collection listing: `/collections/{handle}/products.json`
- Product detail: `/products/{handle}.json`

**File:** `scrapers/shopify.py`

This is the highest-value scraper because it covers two sites with one implementation.

**Key fields to extract:** title, price, url, availability, vendor, product_type, variants, images

**Acceptance:** Can discover and fetch camera listings from both ormsdirect.co.za and cameraland.co.za.

### Task 5: Evetech Scraper

Evetech uses a custom ASP.NET site. Product listing pages render HTML with product cards.

**File:** `scrapers/evetech.py`

**Approach:** Parse the category page HTML for product cards (title, price, URL). Individual product pages at `/product-slug/best-deal/ID` for full details.

**Acceptance:** Can discover and fetch monitor listings from evetech.co.za.

### Task 6: Wootware Scraper

Wootware returns 403 to basic requests — likely has bot protection.

**File:** `scrapers/wootware.py`

**Approach:** Try with proper headers/cookies first. If that fails, may need Playwright/Camoufox (already a dependency). Lower priority than Shopify and Evetech.

**Acceptance:** Can discover and fetch monitor listings from wootware.co.za, or documented as blocked with workaround plan.

### Task 7: Update refresh.sh and fetch_listings.py

Update the pipeline scripts to use the new multi-source config and scraper registry.

**Changes:**
- `refresh.sh`: Iterate over `sources` array per target, call appropriate scraper
- `fetch_listings.py`: Accept `--source` flag, delegate to correct scraper
- Maintain backward compatibility with existing single-source config

**Acceptance:** `./refresh.sh --all` scrapes all configured sources for all categories.

### Task 8: Carbonite Scraper Refactor

Move existing Carbonite-specific code into the scraper interface.

**File:** `scrapers/carbonite.py`

**Approach:** Wrap existing `scrape_forum.py` and `listings.py` logic into the `Scraper` interface. Minimal changes to actual scraping logic.

**Acceptance:** Existing Carbonite workflow works identically through the new interface.

## Existing Tools & Libraries Research

### Relevant GitHub Projects
- **SilverCode/takealot** — Python Takealot scraper (for Phase 2)
- **Fewsats/amazon-mcp** — Amazon MCP server for search & purchase (for Phase 2)
- **r123singh/amazon-mcp-server** — Amazon MCP server that scrapes product/search pages
- **oxylabs/amazon-scraper** — Amazon Scraper API (commercial, has free tier)
- **ScrapeGraphAI/Scrapegraph-ai** — AI-powered scraper that could handle arbitrary sites

### MCP Servers
- **amazon-mcp** — Could be used directly for Amazon.co.za in Phase 2
- **PriceMorphe MCP** — E-commerce price tracking with Bright Data integration
- **BigGo MCP Server** — Multi-platform product search and price history

### Key Insight: Shopify JSON API
Both Orms and Cameraland are Shopify stores. Shopify exposes `/products.json` and `/collections/{handle}/products.json` endpoints that return structured JSON — no HTML parsing needed. This is the cleanest approach for these two sites.

## Execution Order

1. **Task 1 + Task 8** — Scraper interface + Carbonite refactor (foundation, no behavior change)
2. **Task 2** — Add source field to data model
3. **Task 3** — Config schema update
4. **Task 4** — Shopify scraper (Orms + Cameraland — highest value, cleanest API)
5. **Task 5** — Evetech scraper
6. **Task 7** — Update pipeline scripts
7. **Task 6** — Wootware scraper (lowest priority, may be blocked)

## Notes

- All retail scrapers should respect rate limits (1s delay between requests minimum)
- Retail listings don't have "sold" status — they're either in-stock or out-of-stock
- Price field from retail sites is the new/retail price — useful for comparison against Carbonite second-hand prices
- Province is implicit for retail sites (Orms = Western Cape, Evetech = Gauteng but ships nationally)
