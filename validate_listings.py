#!/usr/bin/env python3
"""CLI tool to validate existing listings and update their status."""
import json, sys, time, os, argparse
from tqdm import tqdm
from listings import validate

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('file', help='JSONL file to validate')
    args = p.parse_args()
    
    if not os.path.exists(args.file):
        print(f"File not found: {args.file}", file=sys.stderr)
        sys.exit(1)
    
    # Load records
    records = []
    with open(args.file) as f:
        records = [json.loads(line) for line in f]
    
    # Validate with progress bar
    for i, rec, result in tqdm(validate(records), total=len(records), desc="Validating"):
        if result['status'] != 'active':
            tqdm.write(f"  {result['status']}: {rec.get('title', rec['url'])[:60]}")
        if i < len(records) - 1:
            time.sleep(1)
    
    # Write updated records
    with open(args.file, 'w') as f:
        for rec in records:
            f.write(json.dumps(rec) + '\n')
    
    active = sum(1 for r in records if r.get('status') == 'active')
    print(f"Done: {active} active, {len(records)-active} sold/deleted", file=sys.stderr)
