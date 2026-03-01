#!/usr/bin/env python3
"""CLI tool to fetch listing data from URLs."""
import json, sys, time, os, argparse
from tqdm import tqdm
from listings import fetch

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('urls', nargs='*')
    p.add_argument('--merge', '-m', help='Merge into existing JSONL file')
    args = p.parse_args()
    
    if not args.urls:
        print("Usage: fetch_listings.py [--merge file.jsonl] <url1> [url2] ...", file=sys.stderr)
        sys.exit(1)
    
    # Load existing records if merging
    existing = {}
    if args.merge and os.path.exists(args.merge):
        with open(args.merge) as f:
            for line in f:
                rec = json.loads(line)
                existing[rec['url']] = rec
        print(f"Loaded {len(existing)} existing records", file=sys.stderr)
    
    # Fetch new/updated records
    for i, url in enumerate(tqdm(args.urls, desc="Fetching")):
        existing[url] = fetch(url)
        if i < len(args.urls) - 1:
            time.sleep(1)
    
    # Output
    if args.merge:
        with open(args.merge, 'w') as f:
            for rec in existing.values():
                f.write(json.dumps(rec) + '\n')
        print(f"Wrote {len(existing)} records to {args.merge}", file=sys.stderr)
    else:
        for rec in existing.values():
            print(json.dumps(rec))
