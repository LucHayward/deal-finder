# Monitor Search

Scraping Carbonite.co.za to find 4K monitor deals in the Cape Town area.

## Search Criteria
- Size: 27" - 34"
- Resolution: 4K (2160p) preferred
- Panel: IPS or colour-accurate
- Location: Western Cape (within ~65km of Cape Town)

## Usage

```bash
# Discover listing URLs (defaults: --pages 3 --days 7)
python scrape_forum.py --pages 15 --days 60 > urls.txt

# Fetch metadata as JSONL
grep "^https://" urls.txt | xargs python fetch_listings.py > listings.jsonl

# Filter Western Cape 4K monitors
jq -c 'select(.province=="Western Cape" and .monitor_vert_resolution=="2160p (4k)")' listings.jsonl
```

## Best Deals Found (Western Cape, 4K)
| Monitor | Price | Location |
|---------|-------|----------|
| Samsung 28" 4K | R2,000 | Cape Town |
| Dell S2817Q 28" 4K | R2,100 | Plettenberg Bay |
| Dell S2817Q 27" 4K | R2,500 | Cape Town (Southern Suburbs) |
| Samsung G7 240Hz | R6,000 | Mossel Bay |
| Samsung QN90B 43" 4K 144Hz | R6,500 | Cape Town |
| Dell G3223Q 32" 4K 144Hz IPS | R8,000 | Cape Town (Northern Suburbs) |

## Docs
- [Technical Design](docs/technical-design.md) - Architecture and script details
- [uv Primer](docs/uv-primer.md) - How uv works and why we use it
