# Scrapers Module — Design Document

**Date:** 2026-04-07
**Status:** Draft

## Problem

deal-finder is hardcoded to Carbonite.co.za. The scraping logic (`scrape_forum.py`, `listings.py`) assumes Carbonite's forum HTML structure, URL patterns, and data fields. To add new sites we'd have to fork the entire pipeline per site.

## Goal

A pluggable scraper system where each site has its own implementation behind a common interface. The rest of the pipeline (fetching, classification, storage) stays source-agnostic.

## Interface

```python
# scrapers/base.py
from abc import ABC, abstractmethod

class Scraper(ABC):

    @abstractmethod
    def discover(self, url: str, **kwargs) -> list[dict]:
        """Discover listings from a category/listing page.

        Args:
            url: The category or forum page URL.
            **kwargs: Scraper-specific options (pages, days, known_urls, etc.)

        Returns:
            List of dicts, each with at minimum:
            - url: str        — canonical product/listing URL
            - source: str     — scraper name (e.g. "carbonite", "orms")
        """

    @abstractmethod
    def fetch(self, url: str) -> dict:
        """Fetch full details from a single listing/product page.

        Returns dict with:
            Required fields:
            - url: str          — canonical URL
            - title: str        — product/listing title
            - source: str       — scraper name
            - status: str       — "active", "sold", "deleted", "out_of_stock", "error"
            - fetched_at: str   — ISO 8601 UTC timestamp

            Common optional fields:
            - price: str        — price as string (e.g. "8000", "R 12,999.00")
            - error: str        — error message if fetch failed

            Site-specific fields vary (city, province, condition, warranty,
            monitor_size, vendor, product_type, variants, etc.)
        """
```

### Design Decisions

**Why `discover` returns minimal dicts, not full records:**
Discovery is about finding URLs efficiently. For forums (Carbonite), we scan paginated listing pages. For retail (Shopify), we can get title+price from the collection JSON. But we don't want discovery to be slow — full detail fetching happens in a separate `fetch` pass, which can be parallelized and rate-limited independently.

**Why `source` is a required field on every record:**
Records from different sites end up in the same JSONL file (e.g. `listings/cameras.jsonl` will have Carbonite second-hand listings alongside Orms retail prices). The `source` field lets us filter, deduplicate, and compare across sources.

**Why `status` uses a fixed vocabulary:**
Carbonite has "active"/"sold"/"deleted". Retail sites have "active"/"out_of_stock". Normalizing to a small set of statuses keeps the downstream pipeline simple. The classify step doesn't care about source-specific status nuances.

**Why `price` is a string, not a number:**
Carbonite prices are bare numbers ("8000"). Retail sites may include currency symbols and formatting ("R 12,999.00"). Normalization to cents/int is a downstream concern — the scraper captures what the site shows.

## Registry

```python
# scrapers/__init__.py
_REGISTRY: dict[str, type[Scraper]] = {}

def register(name: str):
    """Decorator to register a scraper class under a name."""
    def wrapper(cls):
        _REGISTRY[name] = cls
        return cls
    return wrapper

def get_scraper(name: str) -> Scraper:
    """Instantiate a scraper by its registered name."""
    return _REGISTRY[name]()
```

Scrapers self-register via decorator:

```python
@register("carbonite")
class CarboniteScraper(Scraper): ...

@register("shopify")
class ShopifyScraper(Scraper): ...

@register("evetech")
class EvetechScraper(Scraper): ...
```

The registry import in `__init__.py` triggers registration. New scrapers just need to be imported there.

## Config Schema

Current config ties each category to a single Carbonite forum URL:

```json
{
  "cameras": {
    "forum": "https://carbonite.co.za/index.php?forums/photo-video-security.93/",
    "output": "listings/cameras.jsonl",
    "query": "...",
    "province": "Western Cape"
  }
}
```

New config supports multiple sources per category:

```json
{
  "cameras": {
    "sources": [
      {
        "name": "carbonite",
        "type": "carbonite",
        "url": "https://carbonite.co.za/index.php?forums/photo-video-security.93/"
      },
      {
        "name": "orms",
        "type": "shopify",
        "url": "https://www.ormsdirect.co.za/collections/mirrorless-cameras"
      },
      {
        "name": "cameraland",
        "type": "shopify",
        "url": "https://www.cameraland.co.za/collections/mirrorless"
      }
    ],
    "output": "listings/cameras.jsonl",
    "query": "...",
    "province": "Western Cape"
  }
}
```

- `name` — unique identifier, becomes the `source` field on records
- `type` — which scraper to use (maps to registry key)
- `url` — entry point URL for that scraper

**Backward compatibility:** If `sources` is absent, the pipeline treats `forum` as a single source with `type: "carbonite"` and `name: "carbonite"`. No migration required for existing configs.

## Data Model Changes

Every JSONL record gains a `source` field:

```json
{"url": "...", "title": "...", "source": "carbonite", "price": "8000", "status": "active", ...}
{"url": "...", "title": "...", "source": "orms", "price": "R 24,995.00", "status": "active", ...}
```

Existing records get backfilled with `"source": "carbonite"` via a one-time migration script.

## Scraper Implementations

### Carbonite (`scrapers/carbonite.py`) — Done

Wraps existing `scrape_forum.py` + `listings.py` logic. Already implemented.

- `discover`: Scans forum pages, filters `[For Sale]` prefix, deduplicates against known URLs
- `fetch`: Parses thread page for `<dl data-field>` metadata blocks
- Carbonite-specific kwargs: `pages`, `days`, `known_urls`

### Shopify (`scrapers/shopify.py`) — Covers Orms + Cameraland

Both sites run Shopify, which exposes a standard JSON API:
- `/collections/{handle}/products.json?limit=250` — paginated product list
- `/products/{handle}.json` — single product detail

No HTML parsing needed. One implementation covers any Shopify store.

- `discover`: Paginate through collection JSON, extract product URLs + basic info
- `fetch`: Hit `/products/{handle}.json` for full variant/pricing/availability data
- The `name` field in config distinguishes "orms" from "cameraland"

Key URLs:
- Orms: `/collections/mirrorless-cameras`, `/collections/zoom-lenses`, `/collections/prime-lenses`
- Cameraland: `/collections/mirrorless`, `/collections/zoom-lenses`, `/collections/prime-lenses`

### Evetech (`scrapers/evetech.py`)

Custom ASP.NET site. Requires HTML parsing.

- `discover`: Parse category page (`/components/monitor-87.aspx`) for product cards
- `fetch`: Parse individual product page (`/product-slug/best-deal/ID`) for specs and price
- Product cards on the listing page contain title and link; prices may need the detail page

### Wootware (`scrapers/wootware.py`) — Stretch Goal

Returns HTTP 403 to basic requests. Options:
1. Try with realistic browser headers + session cookies
2. Fall back to Playwright/Camoufox (already a project dependency)
3. Defer to Phase 2 if neither works easily

## Pipeline Changes

### refresh.sh

Currently calls `scrape_forum.py` → `fetch_listings.py` per target. Updated flow:

```bash
for each target in config:
    for each source in target.sources:
        urls = python discover.py --target $TARGET --source $SOURCE_NAME
        urls | xargs python fetch_listings.py --merge $DB --source $SOURCE_NAME
    classify (unchanged)
```

A new `discover.py` script replaces `scrape_forum.py` as the entry point, using the registry to dispatch to the right scraper.

### fetch_listings.py

Gains a `--source` flag. When set, uses `get_scraper(source).fetch(url)` instead of the old `listings.fetch()`. When unset, falls back to the old behavior for backward compat.

### classify.py

No changes needed. It operates on JSONL records regardless of source. The `source` field is just another field that passes through.

## Migration Path

1. Commit scraper interface + registry + Carbonite refactor
2. Backfill `source` field on existing JSONL data
3. Update config to new schema (backward-compat, old format still works)
4. Update pipeline scripts to use registry
5. Add new scrapers (Shopify, Evetech) on feature branches
6. Merge and add new sources to config
7. Deprecate old `scrape_forum.py` / `listings.py` once stable

Old standalone scripts (`scrape_forum.py`, `listings.py`) remain functional throughout. They just won't be called by `refresh.sh` anymore after step 4.

## File Structure

```
scrapers/
├── __init__.py      # Registry + imports
├── base.py          # Scraper ABC
├── carbonite.py     # Carbonite forum scraper
├── shopify.py       # Shopify JSON API scraper (Orms, Cameraland)
├── evetech.py       # Evetech HTML scraper
└── wootware.py      # Wootware scraper (stretch)
```
