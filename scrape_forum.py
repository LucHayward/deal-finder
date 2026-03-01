#!/usr/bin/env python3
"""Scrape listing URLs from Carbonite forum pages."""
import sys, time, re
import requests

BASE = "https://carbonite.co.za"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_listing_urls(forum_url, pages=1, days=None, known_urls=None):
    """Get listing URLs from forum with filters."""
    urls = []
    known_urls = known_urls or set()
    params = '&prefix_id=1'  # [For Sale] only
    if days:
        params += f'&last_days={days}'
    
    for page in range(1, pages + 1):
        url = forum_url + params
        if page > 1:
            url += f'&page={page}'
        print(f"Scanning page {page}...", file=sys.stderr)
        
        r = requests.get(url, headers=HEADERS, timeout=15)
        matches = re.findall(r'href="(/index\.php\?threads/[^"]+)"', r.text)
        found_known = 0
        for href in matches:
            if 'guide-for-safe' in href or '/latest' in href or '/post-' in href:
                continue
            full_url = BASE + href
            if full_url in known_urls:
                found_known += 1
                continue
            if full_url not in urls:
                urls.append(full_url)
        if found_known > 0:
            print(f"  Found {found_known} known URLs, stopping early", file=sys.stderr)
            break
        time.sleep(1)
    return urls

if __name__ == '__main__':
    import argparse, json, os
    p = argparse.ArgumentParser(description='Get listing URLs from Carbonite forum')
    p.add_argument('--pages', type=int, default=3, help='Number of forum pages to scan')
    p.add_argument('--days', type=int, default=7, help='Filter to listings from last N days')
    p.add_argument('--forum', help='Forum URL (overrides --target)')
    p.add_argument('--target', '-t', help='Target from config.json (e.g. monitors, audio)')
    p.add_argument('--config', default='config.json', help='Config file path')
    p.add_argument('--db', default='listings.jsonl', help='Existing DB to check for known URLs')
    args = p.parse_args()
    
    forum_url = args.forum
    if args.target:
        with open(args.config) as f:
            cfg = json.load(f)[args.target]
        forum_url = cfg['forum']
    forum_url = forum_url or f'{BASE}/index.php?forums/monitors.9/'
    
    known_urls = set()
    if os.path.exists(args.db):
        with open(args.db) as f:
            for line in f:
                rec = json.loads(line)
                known_urls.add(rec['url'])
        print(f"Loaded {len(known_urls)} known URLs from {args.db}", file=sys.stderr)
    
    urls = get_listing_urls(forum_url, args.pages, args.days, known_urls)
    print(f"Found {len(urls)} new listings", file=sys.stderr)
    for url in urls:
        print(url)
