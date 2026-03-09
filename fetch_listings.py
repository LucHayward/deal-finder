#!/usr/bin/env python3
"""CLI tool to fetch listing data from URLs."""
import json, sys, time, os, argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from listings import fetch

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('urls', nargs='*')
    p.add_argument('--merge', '-m', help='Merge into existing JSONL file')
    p.add_argument('--concurrency', '-c', type=int, default=1, help='Number of concurrent requests (default: 1)')
    args = p.parse_args()
    
    if not args.urls:
        print("Usage: fetch_listings.py [--merge file.jsonl] [-c N] <url1> [url2] ...", file=sys.stderr)
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
    errors = []
    if args.concurrency == 1:
        for i, url in enumerate(tqdm(args.urls, desc="Fetching")):
            result = fetch(url)
            existing[url] = result
            if 'error' in result:
                errors.append((url, result['error']))
            if i < len(args.urls) - 1:
                time.sleep(1)
    else:
        with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
            futures = {executor.submit(fetch, url): url for url in args.urls}
            for future in tqdm(as_completed(futures), total=len(futures), desc="Fetching"):
                url = futures[future]
                result = future.result()
                existing[url] = result
                if 'error' in result:
                    errors.append((url, result['error']))
    
    if errors:
        print(f"⚠️  {len(errors)}/{len(args.urls)} requests failed:", file=sys.stderr)
        for url, err in errors[:5]:
            print(f"  {url}: {err}", file=sys.stderr)
        if len(errors) > 5:
            print(f"  ... and {len(errors) - 5} more", file=sys.stderr)
    
    # Output
    if args.merge:
        with open(args.merge, 'w') as f:
            for rec in existing.values():
                f.write(json.dumps(rec) + '\n')
        print(f"Wrote {len(existing)} records to {args.merge}", file=sys.stderr)
    else:
        for rec in existing.values():
            print(json.dumps(rec))
