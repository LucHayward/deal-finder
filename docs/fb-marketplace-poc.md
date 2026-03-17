# Facebook Marketplace PoC

> Canonical reference for FB Marketplace browser automation integration.
> Any agent working on this feature should read this doc first.

## Status: Step 1 — Dependencies

## Goal

Add Facebook Marketplace as a listing source alongside Carbonite.co.za. Browser automation approach since there's no official API.

## Architecture Decision

- **Camoufox** (modified Firefox with C++-level fingerprint spoofing) via Playwright-compatible API
- Cookie injection from manual login (no automated login — too risky for account bans)
- Headed mode preferred (less detectable), headless for CI/scheduled runs
- Human-speed delays between actions (3-7s page loads, 1-3s scrolls)
- Residential IP only (user's home connection is fine)

## Research Summary (from /tmp/fb_research_methods.md)

- No official FB Marketplace API exists. Meta killed Groups API Jan 2024.
- Browser automation is the only path. Playwright + Camoufox is the best open-source stealth stack.
- Cookie injection is the safest auth method — log in manually, export cookies, reuse.
- FB detects: navigator.webdriver, WebGL, canvas, TLS fingerprints, behavioral patterns, CDP artifacts.
- Camoufox handles most detection at C++ level. Add realistic delays for behavioral layer.
- Risk: account restrictions possible. Use a non-primary account. Rate limit aggressively.
- FB Marketplace URL pattern: `facebook.com/marketplace/{location}/search/?query={query}`
- Cape Town location slug: `capetown` or `cape-town` (needs verification)

## Implementation Plan

### Step 1: Install dependencies
```bash
uv add "camoufox[geoip]"
```
Camoufox bundles Playwright-compatible API + stealth Firefox. No separate playwright install needed.

### Step 2: Cookie login helper — `fb_login.py`
- Launch headed Camoufox browser
- Navigate to facebook.com
- User logs in manually
- Save cookies to `fb_cookies.json` (gitignored)
- Reuse cookies in scraper runs

### Step 3: Scraper — `fb_marketplace.py`
- Load cookies → navigate to Marketplace search URL → scroll to load listings → extract data
- Output: JSONL matching existing format (`url`, `title`, `price`, `location`, `source: "fb_marketplace"`)
- Start with GPU category as test case
- CLI: `uv run python fb_marketplace.py --query "GTX 1080" --location capetown --cookies fb_cookies.json`

### Step 4: Config integration
- Add optional `fb_query` field to config.json categories
- Add `fb_marketplace.py` call to refresh.sh for categories that have `fb_query`

## Output Format

Match existing JSONL schema but add `source` field:
```json
{"url": "https://facebook.com/marketplace/item/123", "title": "GTX 1080 8GB", "price": "R3500", "location": "Cape Town", "source": "fb_marketplace"}
```

## Files

| File | Purpose |
|------|---------|
| `fb_login.py` | One-time cookie export helper |
| `fb_marketplace.py` | Marketplace scraper |
| `fb_cookies.json` | Saved session cookies (gitignored) |
| `docs/fb-marketplace-poc.md` | This doc |

## Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| Account ban | Use non-primary account, rate limit aggressively |
| Login modal on Marketplace | Cookie injection bypasses this |
| Listing DOM changes | Extract via aria labels / data attributes where possible, fall back to CSS selectors |
| Rate limiting | 3-7s delays, max ~100 listings per session |
| Cookie expiry | Re-run fb_login.py when cookies expire (days to weeks) |

## Completed Steps

_(Updated as work progresses)_

- [x] Research completed (see /tmp/fb_research_methods.md, /tmp/fb_research_tools.md)
- [x] Step 1: Install camoufox dependency (`camoufox[geoip]` + playwright 1.58.0)
- [x] Step 2: fb_login.py cookie helper (launches headed Camoufox, saves to fb_cookies.json)
- [x] Step 3: fb_marketplace.py scraper (scroll-based extraction, JSONL output)
- [ ] Step 3b: Test with real cookies — need user to run `uv run python fb_login.py`
- [ ] Step 3c: Iterate on DOM selectors based on real page structure
- [ ] Step 4: Config/refresh.sh integration
