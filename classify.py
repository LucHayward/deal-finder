"""Classify listings against a search query using an LLM."""
import json, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

BATCH_SIZE = 50

TAG_HINTS = {
    "mount": "Lens mount compatibility (e.g. 'Sony E', 'Fujifilm X', 'Canon RF'). Use the mount the lens/camera fits, not the manufacturer",
    "format": "Sensor format (e.g. 'APS-C', 'Full-frame')",
}

def _build_prompt(summaries, query, tags=None):
    if tags:
        tag_desc = ", ".join(f'"{t}": {TAG_HINTS.get(t, t)}' for t in tags)
        return (
            f"Which of these listings match ALL of these criteria: {query}\n"
            "Be strict — every criterion must be met or clearly implied by the title.\n"
            f"For each match, also determine: {tag_desc}\n"
            "Return ONLY a JSON array of objects with keys: \"url\"" +
            "".join(f', "{t}"' for t in tags) +
            ". Return [] if none match.\n\n"
            + "\n".join(summaries)
        )
    return (
        f"Which of these listings match ALL of these criteria: {query}\n"
        "Be strict — every criterion must be met or clearly implied by the title.\n"
        "Return ONLY a JSON array of matching URLs, or [] if none match.\n\n"
        + "\n".join(summaries)
    )

def _call_llm(summaries, query, model, tags=None, batch_info=""):
    if batch_info:
        print(f"[kiro-cli] {batch_info}", file=sys.stderr)
    prompt = _build_prompt(summaries, query, tags)
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
                if tags and parsed and isinstance(parsed[0], dict):
                    return {d["url"]: {t: d.get(t) for t in tags} for d in parsed if "url" in d}
                return set(parsed) if not tags else {}
        except json.JSONDecodeError:
            pass
    return {} if tags else set()

def classify(jsonl_path, query, model="claude-haiku-4.5", parallel=1, province=None, only_new=False, tags=None):
    with open(jsonl_path) as f:
        records = [json.loads(line) for line in f if line.strip()]

    to_classify = []
    skipped_province = 0
    skipped_existing = 0
    for r in records:
        if province and r.get("province") and r["province"].lower() != province.lower():
            r["match"] = False
            skipped_province += 1
            continue
        if only_new and "match" in r:
            skipped_existing += 1
            continue
        to_classify.append(r)

    if skipped_province or skipped_existing:
        print(f"[classify] {len(to_classify)} to classify, {skipped_province} filtered by province, {skipped_existing} already classified", file=sys.stderr)

    if not to_classify:
        matched = sum(1 for r in records if r.get("match"))
        print(f"{matched}/{len(records)} matched: {query}", file=sys.stderr)
    else:
        summaries = [
            json.dumps({k: r.get(k) for k in ("url", "title", "price", "city", "province")}, ensure_ascii=False)
            for r in to_classify
        ]
        batches = [summaries[i:i + BATCH_SIZE] for i in range(0, len(summaries), BATCH_SIZE)]
        n = len(batches)

        if tags:
            all_tagged = {}
            if parallel > 1 and n > 1:
                print(f"[kiro-cli] Classifying {len(summaries)} listings in {n} batches ({parallel} parallel)...", file=sys.stderr)
                with ThreadPoolExecutor(max_workers=parallel) as ex:
                    futures = {ex.submit(_call_llm, b, query, model, tags, f"Batch {i+1}/{n}"): i for i, b in enumerate(batches)}
                    for f in as_completed(futures):
                        all_tagged.update(f.result())
            else:
                for i, batch in enumerate(batches):
                    all_tagged.update(_call_llm(batch, query, model, tags, f"Classifying batch {i+1}/{n} ({len(batch)} listings)..."))

            for r in to_classify:
                url = r.get("url")
                if url in all_tagged:
                    r["match"] = True
                    r.update(all_tagged[url])
                else:
                    r["match"] = False
        else:
            matches = set()
            if parallel > 1 and n > 1:
                print(f"[kiro-cli] Classifying {len(summaries)} listings in {n} batches ({parallel} parallel)...", file=sys.stderr)
                with ThreadPoolExecutor(max_workers=parallel) as ex:
                    futures = {ex.submit(_call_llm, b, query, model, None, f"Batch {i+1}/{n}"): i for i, b in enumerate(batches)}
                    for f in as_completed(futures):
                        matches |= f.result()
            else:
                for i, batch in enumerate(batches):
                    matches |= _call_llm(batch, query, model, None, f"Classifying batch {i+1}/{n} ({len(batch)} listings)...")

            for r in to_classify:
                r["match"] = r.get("url") in matches

        matched = sum(1 for r in records if r.get("match"))
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
    p.add_argument("--province", help="Pre-filter: only classify listings in this province (or unknown)")
    p.add_argument("--only-new", action="store_true", help="Only classify listings without existing match field")
    p.add_argument("--tags", nargs="*", help="Extra fields for LLM to tag on matches (e.g. mount format)")
    args = p.parse_args()
    classify(args.jsonl, args.query, args.model, args.parallel, args.province, args.only_new, args.tags)
