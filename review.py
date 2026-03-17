"""Fetch reviews and scores for matched listings using headless kiro agents."""
import json, subprocess, sys, os, argparse, re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REVIEW_DIR = Path("reviews")
TIMEOUT = 180

def extract_products(jsonl_path):
    """Extract unique product names from matched listings."""
    with open(jsonl_path) as f:
        records = [json.loads(l) for l in f if l.strip()]
    matched = [r for r in records if r.get("match") and r.get("status") != "sold"]
    # Deduplicate by title (close enough for now)
    seen = {}
    for r in matched:
        title = r["title"]
        # Strip common prefixes
        clean = re.sub(r"^\[(?:For Sale|Sold)\]\s*-?\s*", "", title, flags=re.I).strip()
        if clean not in seen:
            seen[clean] = r
    return list(seen.values())

def review_product(record, output_dir):
    """Launch headless kiro to research a product and write review."""
    title = re.sub(r"^\[(?:For Sale|Sold)\]\s*-?\s*", "", record["title"], flags=re.I).strip()
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60]
    out_file = output_dir / f"{slug}.md"

    if out_file.exists() and out_file.stat().st_size > 100:
        print(f"  [skip] {title} — already reviewed", file=sys.stderr)
        return {"product": title, "file": str(out_file), "status": "cached"}

    prompt = (
        f"Research reviews for this product: {title}\n\n"
        f"Search DPReview (dpreview.com), RTINGS, photography blogs, and other reputable sources.\n"
        f"Write a concise review summary to {out_file.resolve()} with:\n"
        f"- Product name as heading\n"
        f"- Score out of 10 (aggregate from sources found, or your best estimate)\n"
        f"- 3-5 bullet point summary of pros and cons\n"
        f"- Best use cases\n"
        f"- Sources consulted\n"
        f"- Listing price: R{record.get('price', '?')}\n"
        f"Keep it under 30 lines. Be direct, no fluff."
    )

    print(f"  [review] {title}...", file=sys.stderr)
    result = subprocess.run(
        ["timeout", str(TIMEOUT) + "s", "kiro-cli", "chat",
         "--model", "claude-sonnet-4.6", "--no-interactive", "-a", prompt],
        capture_output=True, text=True,
    )

    if out_file.exists() and out_file.stat().st_size > 50:
        return {"product": title, "file": str(out_file), "status": "ok"}
    else:
        return {"product": title, "file": str(out_file), "status": "failed",
                "error": (result.stderr or result.stdout)[:200]}

def main():
    p = argparse.ArgumentParser(description="Fetch reviews for matched listings")
    p.add_argument("jsonl", nargs="+", help="JSONL file(s) with matched listings")
    p.add_argument("-p", "--parallel", type=int, default=2, help="Parallel review agents")
    p.add_argument("-o", "--output-dir", default="reviews", help="Output directory for reviews")
    args = p.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)

    # Collect products from all JSONL files
    products = []
    for jf in args.jsonl:
        products.extend(extract_products(jf))

    if not products:
        print("No matched (unsold) listings to review.", file=sys.stderr)
        return

    print(f"Reviewing {len(products)} products ({args.parallel} parallel)...", file=sys.stderr)

    results = []
    with ThreadPoolExecutor(max_workers=args.parallel) as ex:
        futures = {ex.submit(review_product, r, output_dir): r for r in products}
        for f in as_completed(futures):
            results.append(f.result())

    # Print summary
    ok = [r for r in results if r["status"] in ("ok", "cached")]
    failed = [r for r in results if r["status"] == "failed"]
    print(f"\n{'='*50}", file=sys.stderr)
    print(f"Reviews: {len(ok)} complete, {len(failed)} failed", file=sys.stderr)
    for r in ok:
        print(f"  ✓ {r['product']} → {r['file']}", file=sys.stderr)
    for r in failed:
        print(f"  ✗ {r['product']}: {r.get('error', 'unknown')[:80]}", file=sys.stderr)

if __name__ == "__main__":
    main()
