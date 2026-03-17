#!/usr/bin/env python3
"""Scrape Facebook Marketplace listings using Camoufox."""
import json, sys, time, argparse, random
from camoufox.sync_api import Camoufox

COOKIE_FILE = "fb_cookies.json"
BASE_URL = "https://www.facebook.com/marketplace"

def load_cookies(path):
    with open(path) as f:
        return json.load(f)

def random_delay(lo=2, hi=5):
    time.sleep(random.uniform(lo, hi))

def scrape(query, location="capetown", cookies_path=COOKIE_FILE, max_scroll=5, headless=False):
    url = f"{BASE_URL}/{location}/search/?query={query}"
    cookies = load_cookies(cookies_path)

    with Camoufox(headless=headless) as browser:
        ctx = browser.new_context()
        ctx.add_cookies(cookies)
        page = ctx.new_page()

        print(f"Navigating to: {url}", file=sys.stderr)
        page.goto(url, wait_until="domcontentloaded")
        random_delay(3, 6)

        # Dismiss login modal if it appears
        try:
            close_btn = page.locator('[aria-label="Close"]').first
            if close_btn.is_visible(timeout=3000):
                close_btn.click()
                random_delay(1, 2)
        except Exception:
            pass

        # Scroll to load more listings
        for i in range(max_scroll):
            page.mouse.wheel(0, random.randint(800, 1200))
            random_delay(2, 4)
            print(f"Scroll {i+1}/{max_scroll}", file=sys.stderr)

        # Extract listings
        listings = []
        # FB Marketplace listings are typically in anchor tags linking to /marketplace/item/
        links = page.locator('a[href*="/marketplace/item/"]').all()
        print(f"Found {len(links)} listing links", file=sys.stderr)

        seen_urls = set()
        for link in links:
            try:
                href = link.get_attribute("href") or ""
                # Normalize URL
                if href.startswith("/"):
                    href = "https://www.facebook.com" + href
                # Dedupe
                item_url = href.split("?")[0]
                if item_url in seen_urls:
                    continue
                seen_urls.add(item_url)

                # Extract text content from the link container
                text = link.inner_text(timeout=2000).strip()
                lines = [l.strip() for l in text.split("\n") if l.strip()]

                # FB typically shows: price, title, location (in some order)
                price = next((l for l in lines if l.startswith("R") or l.startswith("Free")), None)
                # Title is usually the longest non-price line
                non_price = [l for l in lines if l != price]
                title = max(non_price, key=len) if non_price else text

                # Location is often the shortest remaining line
                remaining = [l for l in non_price if l != title]
                location_text = remaining[0] if remaining else None

                listings.append({
                    "url": item_url,
                    "title": title,
                    "price": price,
                    "location": location_text,
                    "source": "fb_marketplace",
                    "raw_lines": lines,
                })
            except Exception as e:
                print(f"Error extracting listing: {e}", file=sys.stderr)

        return listings

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--query", "-q", required=True)
    p.add_argument("--location", "-l", default="capetown")
    p.add_argument("--cookies", default=COOKIE_FILE)
    p.add_argument("--scrolls", "-s", type=int, default=5)
    p.add_argument("--headless", action="store_true")
    p.add_argument("--output", "-o", help="Output JSONL file")
    args = p.parse_args()

    results = scrape(args.query, args.location, args.cookies, args.scrolls, args.headless)

    if args.output:
        with open(args.output, "w") as f:
            for r in results:
                f.write(json.dumps(r) + "\n")
        print(f"Wrote {len(results)} listings to {args.output}", file=sys.stderr)
    else:
        for r in results:
            print(json.dumps(r))
