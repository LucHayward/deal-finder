#!/usr/bin/env python3
"""Classify monitor listings using kiro-cli chat in headless mode."""
import json, sys, subprocess

PROMPT = """Search Criteria:
- Size: 27" - 34"
- Resolution: 4K (2160p) preferred
- Panel: IPS or colour-accurate
- Location: Western Cape (within ~65km of Cape Town)

Classify as RELEVANT or NOT_RELEVANT.
Return ONLY valid JSON: {"relevant": true/false, "reason": "brief explanation"}

Listing:
"""

def classify(listing, model):
    prompt = PROMPT + json.dumps(listing, indent=2)
    result = subprocess.run(
        ["kiro-cli", "chat", "--model", model, "--no-interactive", "-a", prompt],
        capture_output=True, text=True, timeout=30
    )
    try:
        return json.loads(result.stdout.strip().split('\n')[-1])
    except:
        return {"relevant": False, "reason": "parse error"}

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('input', help='Input JSONL file')
    p.add_argument('-o', '--output', help='Output JSONL (relevant only)')
    p.add_argument('--model', default='claude-haiku-4.5')
    args = p.parse_args()
    
    with open(args.input) as f:
        listings = [json.loads(line) for line in f]
    
    print(f"Classifying {len(listings)} with {args.model}...", file=sys.stderr)
    relevant = []
    for i, listing in enumerate(listings, 1):
        title = listing.get('title', 'N/A')[:60]
        print(f"{i}/{len(listings)}: {title}...", file=sys.stderr)
        result = classify(listing, args.model)
        if result.get('relevant'):
            listing['classification'] = result
            relevant.append(listing)
            print(f"  ✓ {result.get('reason')}", file=sys.stderr)
    
    print(f"\nFound {len(relevant)}/{len(listings)} relevant", file=sys.stderr)
    
    out = open(args.output, 'w') if args.output else sys.stdout
    for item in relevant:
        print(json.dumps(item), file=out)
    if args.output:
        out.close()
