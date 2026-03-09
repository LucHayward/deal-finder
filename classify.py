"""Classify listings against a search query using an LLM."""
import json, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

BATCH_SIZE = 50

def _call_llm(summaries, query, model, batch_info=""):
    if batch_info:
        print(f"[kiro-cli] {batch_info}", file=sys.stderr)
    prompt = (
        f"Which of these listings match ALL of these criteria: {query}\n"
        "Be strict — every criterion must be met or clearly implied by the title.\n"
        "Return ONLY a JSON array of matching URLs, or [] if none match.\n\n"
        + "\n".join(summaries)
    )
    result = subprocess.run(
        ["kiro-cli", "chat", "--model", model, "--no-interactive"],
        input=prompt, capture_output=True, text=True,
    )
    output = re.sub(r"\x1b\[[0-9;?]*[a-zA-Z]", "", result.stdout + result.stderr)
    output = re.sub(r"[^\x20-\x7e\n]", "", output)
    m = re.search(r'\[[\s\S]*?\]', output)
    if m:
        try:
            parsed = json.loads(m.group())
            if isinstance(parsed, list):
                return set(parsed)
        except json.JSONDecodeError:
            pass
    return set()

def classify(jsonl_path, query, model="claude-haiku-4.5", parallel=1):
    with open(jsonl_path) as f:
        records = [json.loads(line) for line in f if line.strip()]

    summaries = [
        json.dumps({k: r.get(k) for k in ("url", "title", "price", "city", "province")}, ensure_ascii=False)
        for r in records
    ]

    batches = [summaries[i:i + BATCH_SIZE] for i in range(0, len(summaries), BATCH_SIZE)]
    n = len(batches)
    matches = set()

    if parallel > 1 and n > 1:
        print(f"[kiro-cli] Classifying {len(summaries)} listings in {n} batches ({parallel} parallel)...", file=sys.stderr)
        with ThreadPoolExecutor(max_workers=parallel) as ex:
            futures = {ex.submit(_call_llm, b, query, model, f"Batch {i+1}/{n}"): i for i, b in enumerate(batches)}
            for f in as_completed(futures):
                matches |= f.result()
    else:
        for i, batch in enumerate(batches):
            matches |= _call_llm(batch, query, model, f"Classifying batch {i+1}/{n} ({len(batch)} listings)...")

    for r in records:
        r["match"] = r.get("url") in matches

    matched = sum(1 for r in records if r["match"])
    print(f"{matched}/{len(records)} matched: {query}", file=sys.stderr)

    with open(jsonl_path, "w") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("jsonl")
    p.add_argument("query")
    p.add_argument("--model", default="claude-haiku-4.5")
    p.add_argument("--parallel", "-p", type=int, default=1)
    args = p.parse_args()
    classify(args.jsonl, args.query, args.model, args.parallel)
