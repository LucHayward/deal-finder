"""Fetch reviews and scores for matched listings using headless kiro agents."""
import json, subprocess, sys, os, argparse, re
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REVIEW_DIR = Path("reviews")
TIMEOUT = 180

def _extract_score(md_path, is_lens):
    """Parse the authoritative score from a review markdown file."""
    text = md_path.read_text()
    if is_lens:
        m = re.search(r'DxOMark[:\s]+(\d+)', text)
        return ("dxomark", int(m.group(1))) if m else (None, None)
    else:
        m = re.search(r'DPReview[:\s]+(\d+)%', text)
        return ("dpreview", int(m.group(1))) if m else (None, None)

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
    is_lens = not any(kw in title.lower() for kw in ("kit", "body", "camera")) and \
              any(kw in title.lower() for kw in ("mm f", "mm f/", "lens", "xf ", "xc "))

    if out_file.exists() and out_file.stat().st_size > 100:
        print(f"  [skip] {title} — already reviewed", file=sys.stderr)
        source, score = _extract_score(out_file, is_lens)
        return {"product": title, "file": str(out_file), "status": "cached",
                "type": "lens" if is_lens else "camera",
                "price": record.get("price"), "url": record.get("url"),
                "review_source": source, "review_score": score}

    if is_lens:
        score_instruction = (
            "For the score: find the DxOMark lab score for this lens (dxomark.com). "
            "Report it as 'DxOMark: XX' and note the best-in-class score for context. "
            "Do NOT use user reviews or aggregated scores."
        )
    else:
        score_instruction = (
            "For the score: find the DPReview editorial score (dpreview.com) as a percentage. "
            "Report it as 'DPReview: XX%' with the award tier if any (Gold/Silver/Bronze). "
            "Do NOT use user reviews or aggregated scores."
        )

    prompt = (
        f"Research reviews for this product: {title}\n\n"
        f"{score_instruction}\n"
        f"Write a concise review summary to {out_file.resolve()} with:\n"
        f"- Product name as heading\n"
        f"- Official score line (as described above)\n"
        f"- 3-5 bullet point pros and cons\n"
        f"- Best use cases\n"
        f"- Sources consulted (with URLs)\n"
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
        source, score = _extract_score(out_file, is_lens)
        return {"product": title, "file": str(out_file), "status": "ok",
                "type": "lens" if is_lens else "camera",
                "price": record.get("price"), "url": record.get("url"),
                "review_source": source, "review_score": score}
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

    # Write structured scores for comparison (deduplicated)
    seen_files = set()
    scores = []
    for r in ok:
        if r["file"] in seen_files:
            continue
        seen_files.add(r["file"])
        scores.append({k: r[k] for k in ("product", "type", "price", "url", "review_source", "review_score", "file") if r.get(k) is not None})
    scores_file = output_dir / "scores.json"
    scores_file.write_text(json.dumps(scores, indent=2, ensure_ascii=False) + "\n")
    print(f"Scores written to {scores_file}", file=sys.stderr)

if __name__ == "__main__":
    main()
