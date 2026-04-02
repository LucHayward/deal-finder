# Camera–Lens Cross-Referencing Design

## Problem

Camera bodies and lenses are listed separately on forums. A buyer needs to know which lenses fit which bodies, and ideally see compatible pairings ranked by value. Today the data exists in two JSONL files with `mount` and `format` tags, but nothing connects them.

## Current State

Both `cameras.jsonl` and `camera-lenses.jsonl` have matched listings tagged with:

```json
{
  "title": "Sony Alpha a7C II ...",
  "price": "27999",
  "match": true,
  "mount": "Sony E",
  "format": "Full-frame"
}
```

Mount values: `Sony E`, `Fujifilm X`, `Canon RF`, etc.
Format values: `Full-frame`, `APS-C`.

## Compatibility Rules

Lens–body compatibility isn't just mount matching. Key rules:

| Lens | Body | Compatible? | Notes |
|------|------|-------------|-------|
| Sony FE (FF) | Sony FF body | ✅ | Native |
| Sony FE (FF) | Sony APS-C body | ✅ | Works with crop factor |
| Sony E (APS-C) | Sony APS-C body | ✅ | Native |
| Sony E (APS-C) | Sony FF body | ⚠️ | Works in crop mode, reduced resolution |
| Fujifilm XF | Fujifilm X body | ✅ | Native |
| Fujifilm XF | Sony body | ❌ | Wrong mount |

Summary: within the same mount system, FF lenses work on both FF and APS-C bodies. APS-C lenses on FF bodies is technically possible but suboptimal.

## Proposed Design

### match.py

A standalone script that reads both JSONL files and outputs pairings.

```bash
uv run python match.py [--format table|json] [--include-crop-mode]
```

**Logic:**
1. Load matched (`match: true`, `status != sold`) cameras and lenses
2. Group by mount
3. For each camera, find compatible lenses:
   - Same mount = compatible
   - FF lens on APS-C body = compatible (note crop factor)
   - APS-C lens on FF body = only if `--include-crop-mode`
4. Output pairings sorted by total kit price (body + lens)

**Output (table mode):**
```
Sony E / Full-frame
  Body: Sony A7C II — R27,999 (Stellenbosch)
  Compatible lenses:
    Sigma 85mm f/1.4 DG DN Art — R15,000 (FF native)
    Zeiss Loxia 21mm f/2.8 — R10,000 (FF native)
    Sony 10-18mm f/4 OSS — R7,500 (APS-C, crop mode)

Sony E / APS-C
  Body: Sony ZV-E10 — R11,000 (Cape Town)
  Compatible lenses:
    Sony 10-18mm f/4 OSS — R7,500 (APS-C native)
    Sigma 85mm f/1.4 DG DN Art — R15,000 (FF, 127mm equiv)
    ...
```

**Output (json mode):**
```json
[
  {
    "body": { "title": "...", "price": "27999", "mount": "Sony E", "format": "Full-frame" },
    "lenses": [
      { "title": "...", "price": "15000", "compatibility": "native" },
      { "title": "...", "price": "7500", "compatibility": "crop-mode" }
    ],
    "cheapest_kit": 37999
  }
]
```

### Integration with refresh.sh

No integration needed. This is a read-only view layer that runs on demand, separate from the scraping/classification pipeline.

### Future Extensions

- **Kit budget filter:** `--max-kit-price 30000` to only show combos under a budget
- **Crop factor display:** Show effective focal length when FF lens is on APS-C (×1.5 Sony, ×1.5 Fuji)
- **Deal scoring:** Compare kit prices against new retail to flag good deals
- **Notification:** Alert when a new listing completes a body+lens combo under a price threshold

## Non-Goals

- No changes to scraping or classification pipeline
- No persistent storage of pairings — computed on the fly from JSONL
- No cross-mount adapter support (too niche)

## Dependencies

None beyond Python stdlib + the existing JSONL files.
