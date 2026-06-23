# Facebook Marketplace Scraping: Open-Source Python Tools (2025–2026)

## Executive Summary

Facebook Marketplace scraping remains **feasible but increasingly difficult** in 2025/2026. Meta treats Marketplace as core infrastructure and defends it with aggressive anti-bot measures. The open-source landscape is fragmented — most repos are small, under-maintained, and frequently break as Facebook rotates internal APIs. The two viable technical approaches are:

1. **Browser automation** (Playwright/Selenium) with authenticated sessions
2. **Direct GraphQL API calls** to Facebook's internal `/api/graphql/` endpoint

No public REST API exists for Marketplace. All approaches require either login cookies or browser-based authentication.

---

## Top Open-Source Repositories

### 1. passivebot/facebook-marketplace-scraper ⭐ 380 (ARCHIVED)

| Field | Value |
|-------|-------|
| **URL** | https://github.com/passivebot/facebook-marketplace-scraper |
| **Stars** | 380 |
| **Status** | **Archived** (Nov 23, 2024) — read-only |
| **Approach** | Playwright + BeautifulSoup |
| **Auth** | Uses Playwright browser session (user must be logged in) |
| **Features** | City-based search, query + max price filters, Streamlit GUI, FastAPI backend |
| **Output** | JSON via API; displays images, prices, locations, item URLs |

**Notes:** The most-starred FB Marketplace scraper on GitHub. Archived by the maintainer — likely due to constant breakage from Facebook's anti-bot updates. Still useful as a reference implementation for the Playwright approach. The same author (harmindersinghnijjar) has multiple related repos.

---

### 2. kyleronayne/marketplace-api ⭐ 70

| Field | Value |
|-------|-------|
| **URL** | https://github.com/kyleronayne/marketplace-api |
| **Stars** | 70 |
| **Status** | Active (17 commits) |
| **Approach** | **Direct GraphQL API** (wraps Facebook's internal GraphQL endpoint) |
| **Auth** | Claims **no login required** — uses Facebook's public GraphQL surface |
| **Features** | Location search (lat/long), keyword search, price filters, pagination, seller info |
| **Output** | JSON API with structured listing data |

**Notes:** The most interesting approach — it wraps Facebook's GraphQL API directly without browser automation. Returns listing ID, name, price, seller name/location/type, sale pending status, and photo URLs. The "no login" claim likely relies on unauthenticated GraphQL endpoints that Facebook may restrict at any time. High risk of breakage when Facebook rotates `doc_id` values.

---

### 3. JustSxm/Deals-Scraper ⭐ 101

| Field | Value |
|-------|-------|
| **URL** | https://github.com/JustSxm/Deals-Scraper |
| **Stars** | 101 |
| **Status** | Active (40 commits) |
| **Approach** | Scrapy-based HTTP scraping |
| **Auth** | **Requires user to be logged into Facebook in their browser** — scrapes using browser cookies |
| **Features** | Multi-site (FB Marketplace, Kijiji, eBay, Amazon, Lespacs), keyword search, price range, exclusions, strict mode, scheduled recurring runs, sort options |
| **Output** | Structured deal alerts |

**Notes:** Canadian-focused multi-marketplace deal finder. The Facebook module uses city IDs and supports sorting by distance, price, or creation time. Requires manual Facebook login first — it reads cookies from the user's browser session. Well-structured with config.ini for easy customization. MIT licensed.

---

### 4. jeisonchuquin/fb-marketplace-scraper ⭐ ~5

| Field | Value |
|-------|-------|
| **URL** | https://github.com/jeisonchuquin/fb-marketplace-scraper |
| **Stars** | ~5 |
| **Status** | Active |
| **Approach** | Selenium + BeautifulSoup + SQLite |
| **Auth** | Selenium browser session (user logs in via automated browser) |
| **Features** | Category navigation, product detail extraction, Tkinter GUI |
| **Output** | SQLite database |

**Notes:** Navigates through Marketplace categories, retrieves product details, stores in SQLite. Tkinter GUI for control. Simpler implementation but demonstrates the category-browsing pattern.

---

### 5. Marketscrape/marketscrape-web ⭐ 12

| Field | Value |
|-------|-------|
| **URL** | https://github.com/Marketscrape/marketscrape-web |
| **Stars** | 12 |
| **Status** | Active |
| **Approach** | Selenium-based scraping + AI valuation |
| **Auth** | Browser session (login required) |
| **Features** | Scrapes listings, uses ML/AI to assess listing value, helps find underpriced deals |
| **Output** | Web interface with deal recommendations |

**Notes:** Differentiator is the AI layer that evaluates whether a listing is a good deal. Combines scraping with price intelligence.

---

## Authentication Approaches

All tools handle Facebook's login requirement in one of three ways:

| Method | How it works | Pros | Cons |
|--------|-------------|------|------|
| **Browser automation login** | Playwright/Selenium opens FB, user logs in manually or credentials are provided | Full access to all Marketplace data | Slow, resource-heavy, checkpoint-prone |
| **Cookie injection** | Extract `c_user`, `xs`, `datr` cookies from a logged-in browser session | Fast, no browser overhead | Cookies expire; requires manual refresh |
| **GraphQL without auth** | Hit Facebook's public GraphQL surface directly | No account needed | Very limited data; Facebook restricts aggressively |

### Key tokens for authenticated GraphQL scraping:
- `c_user` — Facebook user ID
- `xs` — session token
- `datr` — browser fingerprint cookie
- `fb_dtsg` — CSRF token (must be extracted from page load)
- `doc_id` — precompiled GraphQL query hash (rotates every few weeks)

---

## Technical Approaches Comparison

| Approach | Tools | Speed | Stealth | Maintenance |
|----------|-------|-------|---------|-------------|
| **Playwright** | passivebot, Marketscrape | Medium | Good (real browser) | High (FB UI changes) |
| **Selenium** | jeisonchuquin, dataartist-og | Medium | Good (real browser) | High |
| **Direct GraphQL** | kyleronayne/marketplace-api | Fast | Low (easily fingerprinted) | Very High (doc_id rotation) |
| **HTTP + Proxies** | harmindersinghnijjar, Deals-Scraper | Fast | Depends on proxy quality | High |
| **Camoufox** | No dedicated FB Marketplace repo yet | Medium | Excellent (anti-detect Firefox) | Medium |

### Camoufox Note
[Camoufox](https://github.com/daijro/camoufox) (⭐ 6k+) is an anti-detect browser built on Firefox that integrates with Playwright. While no dedicated FB Marketplace scraper uses it yet, it's the emerging best practice for evading Meta's bot detection. Apify has a [generic Camoufox scraper actor](https://github.com/apify/actor-camoufox-scraper) that could be adapted.

---

## Facebook's Anti-Bot Defenses (2025/2026 State)

Facebook is described as **"the most aggressive anti-scraping target in 2026"** by multiple sources:

### Detection Methods:
- **IP reputation scoring** — datacenter IPs are instantly blocked
- **Session/IP drift detection** — changing IPs on a logged-in session triggers checkpoints within minutes
- **Browser fingerprinting** — canvas, WebGL, font enumeration, navigator properties
- **Behavioral analysis** — request timing, scroll patterns, mouse movements
- **Rate limiting** — ~30-60 requests/hour per IP for unauthenticated; ~200-400/hour for warmed accounts
- **Checkpoint challenges** — photo ID verification, phone re-verification
- **Shadow throttling** — returns empty results for known-good queries instead of blocking outright
- **`doc_id` rotation** — GraphQL query hashes change every few weeks, breaking direct API scrapers

### What Gets You Blocked:
- Using datacenter proxies (instant block)
- Rotating IPs on authenticated sessions
- Scraping immediately after account creation
- High request rates (>400/hour)
- Accessing regions that don't match your IP geolocation

### What Works:
- **Static residential (ISP) proxies** — one stable IP per account
- **Mobile LTE proxies** — for account warming (CGNAT provides cover)
- **Account warming** — 7+ days of normal browsing before scraping
- **Geo-matching** — proxy IP must match account's saved location
- **Low request rates** — 200-400 requests/hour per warmed account

---

## Feasibility Assessment (2025/2026)

### Is it still feasible? **Yes, but with significant investment.**

| Scenario | Feasibility | Cost |
|----------|-------------|------|
| **Casual/personal use** (< 100 listings/day) | ✅ Feasible | Free (use your own account + Playwright) |
| **Moderate volume** (1k-10k listings/day) | ⚠️ Feasible with effort | $50-200/month (proxies + accounts) |
| **High volume** (50k+ listings/day) | ⚠️ Expensive | $500+/month or use commercial APIs |
| **Commercial API approach** | ✅ Easiest | $2-5 per 1,000 listings (Apify, Bright Data, etc.) |

### Key Constraints:
1. **No official API** — Meta has no public Marketplace API and shows no signs of creating one
2. **Account risk** — never scrape from a personal account you care about
3. **Geographic lock-in** — results are heavily filtered by IP geolocation + account location
4. **Constant maintenance** — `doc_id` rotation, UI changes, and anti-bot updates require ongoing work
5. **Legal gray area** — violates Meta's ToS (grounds for account ban, not criminal); public listing data has been treated as scrapable in US case law

### Recommended Approach for a Deal-Finder Project:
1. Use **Playwright with Camoufox** for stealth
2. Maintain 2-3 **warmed Facebook accounts** on static residential proxies
3. Scrape at **low rates** (200 req/hour max per account)
4. Store session cookies and rotate accounts
5. Implement **retry logic** for checkpoint detection
6. Consider the **kyleronayne/marketplace-api** GraphQL approach as a faster alternative (but expect more breakage)

---

## Sources

- ⚠️ External link — [passivebot/facebook-marketplace-scraper](https://github.com/passivebot/facebook-marketplace-scraper) — accessed 2026-05-14
- ⚠️ External link — [kyleronayne/marketplace-api](https://github.com/kyleronayne/marketplace-api) — accessed 2026-05-14
- ⚠️ External link — [JustSxm/Deals-Scraper](https://github.com/JustSxm/Deals-Scraper) — accessed 2026-05-14
- ⚠️ External link — [jeisonchuquin/fb-marketplace-scraper](https://github.com/jeisonchuquin/fb-marketplace-scraper) — accessed 2026-05-14
- ⚠️ External link — [Marketscrape/marketscrape-web](https://github.com/Marketscrape/marketscrape-web) — accessed 2026-05-14
- ⚠️ External link — [daijro/camoufox](https://github.com/daijro/camoufox) — accessed 2026-05-14
- ⚠️ External link — [How to Scrape Facebook Marketplace (2026) — SpyderProxy](https://spyderproxy.com/blog/how-to-scrape-facebook-marketplace) — accessed 2026-05-14
- ⚠️ External link — [Facebook Scraper in Python — PromptCloud](https://www.promptcloud.com/blog/python-facebook-scraper/) — accessed 2026-05-14
- ⚠️ External link — [How to Scrape Facebook — ScrapFly](https://scrapfly.io/blog/posts/how-to-scrape-facebook) — accessed 2026-05-14
- ⚠️ External link — [7 Tools & Methods to Scrape Facebook — Thunderbit](https://thunderbit.com/blog/tools-to-scrape-facebook) — accessed 2026-05-14
