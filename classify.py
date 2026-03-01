"""Classify listings against a search query using an LLM."""
import json, re, subprocess, sys

BATCH_SIZE = 50

def _call_llm(summaries, query, model):
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

def classify(jsonl_path, query, model="claude-haiku-4.5"):
    with open(jsonl_path) as f:
        records = [json.loads(line) for line in f if line.strip()]

    summaries = [
        json.dumps({k: r.get(k) for k in ("url", "title", "price", "city", "province")}, ensure_ascii=False)
        for r in records
    ]

    matches = set()
    for i in range(0, len(summaries), BATCH_SIZE):
        batch = summaries[i:i + BATCH_SIZE]
        matches |= _call_llm(batch, query, model)

    for r in records:
        r["match"] = r.get("url") in matches

    matched = sum(1 for r in records if r["match"])
    print(f"{matched}/{len(records)} matched: {query}", file=sys.stderr)

    with open(jsonl_path, "w") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    classify(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "claude-haiku-4.5")
