# Technical Design

## Architecture

```
┌─────────────────┐     URLs      ┌──────────────────┐     JSON
│  scrape_forum   │ ───────────▶  │  fetch_listings  │ ──────────▶  listings.json
│    (discover)   │   (stdout)    │    (extract)     │
└─────────────────┘               └──────────────────┘
```

Two scripts with separated concerns:

1. **scrape_forum.py** - Discovers listing URLs from forum pages
2. **fetch_listings.py** - Extracts metadata from individual listings

## Scripts

### scrape_forum.py

Scans Carbonite forum pages and outputs listing URLs.

**Input:** Forum URL, page count, optional day filter
**Output:** URLs to stdout (one per line)

```bash
python scrape_forum.py --pages 2 --days 7
```

**How it works:**
1. Builds filtered URL with `prefix_id=1` ([For Sale] only)
2. Fetches each page, extracts thread URLs via regex
3. Deduplicates and outputs to stdout

**Filter params:**
- `prefix_id=1` - [For Sale] listings only
- `last_days=N` - Listings from last N days (7, 14, 30)

### fetch_listings.py

Fetches full metadata from listing URLs.

**Input:** One or more URLs as CLI args
**Output:** JSON array to stdout (or file with `-o`)

```bash
python fetch_listings.py <url1> [url2] ... [-o output.json]
```

**Extracted fields:**
- `url`, `title`
- `city`, `province`
- `price`, `warranty`, `condition`
- `monitor_size`, `monitor_vert_resolution`, `monitor_refresh_rate`

## Carbonite HTML Structure

Listing metadata is in `<dl>` tags with `data-field` attributes:

```html
<div class="blockStatus-message">
  <dl data-field="city"><dt>Location</dt><dd>Cape Town</dd></dl>
  <dl data-field="price"><dt>Price</dt><dd>8000</dd></dl>
  <dl data-field="monitor_size"><dt>Monitor Size</dt><dd>32"</dd></dl>
  ...
</div>
```

BeautifulSoup extracts these with:
```python
for dl in soup.select('div.blockStatus-message dl[data-field]'):
    field = dl['data-field']
    value = dl.find('dd').get_text(strip=True)
```

## Usage Patterns

**Full pipeline:**
```bash
python scrape_forum.py --pages 5 --days 14 | xargs python fetch_listings.py -o listings.json
```

**Filter results with jq:**
```bash
# Western Cape 4K monitors
jq '.[] | select(.province=="Western Cape" and .monitor_vert_resolution=="2160p (4k)")' listings.json

# Sort by price
jq 'sort_by(.price | tonumber)' listings.json
```

**Step by step:**
```bash
python scrape_forum.py --pages 2 > urls.txt
python fetch_listings.py $(cat urls.txt) -o listings.json
```

## Dependencies

- `requests` - HTTP client
- `beautifulsoup4` - HTML parsing

Managed via uv. See [uv-primer.md](uv-primer.md) for setup.

## Rate Limiting

Both scripts include 1-second delays between requests to avoid hammering the server.
