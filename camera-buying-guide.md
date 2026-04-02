# Camera Buying Guide: Fuji vs Sony — A Decision Framework
**For:** A raw-shooting enthusiast in Cape Town, buying second-hand  
**Date:** March 2026  
**Context:** Recently shot a friend's Sony A7IV with Tamron 35-150mm f/2-2.8 and Sigma 85mm f/1.4 Art

---

## TL;DR

You're at a genuine fork in the road. Your experience with the A7IV + fast glass was clearly fun — shooting wide open at f/1.4–2.5 on an 85mm, and playing across 35–150mm at various focal lengths. That's a very "Sony full-frame" experience. The question is whether to chase that feeling, or whether Fuji APS-C gives you 90% of it at 60% of the cost.

**If you're going to shoot RAW and edit in Lightroom 90%+ of the time → Sony has fewer friction points.**  
**If you want the best APS-C ecosystem, smaller/lighter kit, and enjoy SOOC JPEGs → Fuji wins.**  
**If you want the shallow DOF and low-light you experienced with your friend's kit → Full-frame Sony.**

---

## Part 1: The Lightroom + RAW Question (This Matters More Than You Think)

### The Fuji X-Trans / Lightroom Situation

You're right that there's been a long-running issue. Fuji uses a unique X-Trans sensor pattern instead of the standard Bayer pattern that Sony/Canon/Nikon use. Lightroom's demosaicing algorithm has historically struggled with X-Trans, producing:

- "Worm" artifacts in fine detail (grass, fabric, hair)
- Mushy/painterly rendering compared to the same files in Capture One
- Less detail extraction at default settings

**The good news (as of 2025/2026):** Adobe Lightroom Classic 14.4+ added a "Raw Details" checkbox in the Detail panel that uses AI demosaicing. This largely solves the worm artifacts without needing to generate separate DNG files. It's now just a single checkbox per image. Thomas Fitzgerald (who's been covering this since 2012) considers the issue essentially resolved for practical purposes.

**The nuance:** It's still an extra step. Sony/Canon/Nikon Bayer RAW files just work perfectly in Lightroom with zero intervention. Fuji files need that checkbox toggled. For batch workflows this is minor, but it's not zero friction.

### Film Simulations in Lightroom

Fuji's film simulations (Classic Neg, Portra 400-esque recipes, etc.) are embedded in the JPEG, not the RAW. When you shoot RAW on a Fuji:

- Lightroom shows a "Camera Profile" dropdown with Fuji film sim names (Classic Chrome, Velvia, etc.)
- These are Adobe's *approximations* — they're close but not identical to the in-camera rendering
- The real magic of Fuji film sims is in the JPEG engine, not the RAW data
- Many Fuji shooters shoot RAW+JPEG specifically for this reason

**Bottom line:** If you're a "shoot RAW, edit everything in Lightroom" person, you're not getting the full Fuji film simulation experience. The film sims are a bonus for SOOC shooting, not a RAW editing advantage.

### What This Means For You

Since you're already comfortable shooting RAW on the A7IV and editing in Lightroom:
- Sony RAW files → Lightroom = seamless, zero friction
- Fuji RAW files → Lightroom = works well now (with Raw Details checkbox), but you lose the film sim magic that's half the reason people love Fuji
- If film sims don't matter to you → the Fuji color science advantage shrinks significantly in a RAW workflow

---

## Part 2: The Ecosystem Question — APS-C Commitment

### Fuji: APS-C First-Class Citizen ✅

You're absolutely right about this. Fuji's entire X-mount system is designed for APS-C:

- **45+ native XF lenses** all designed for the crop sensor
- Every lens is optimized for APS-C size/weight/price
- Fuji actively develops new APS-C lenses (recent: XF 16-50mm f/2.8-4.8, XF 56mm f/1.2 II)
- Third-party support is strong: Viltrox, Sigma, Tamron all make X-mount glass
- No "crop tax" — you're never paying for glass that covers a bigger sensor than you need

### Sony: Full-Frame First, APS-C Second ⚠️

Sony's heart is in full-frame. Their APS-C situation:

- **~15-20 dedicated APS-C (E) lenses** — limited selection
- Sony hasn't released a new APS-C-specific lens in years
- You *can* use full-frame FE lenses on APS-C bodies (they work perfectly) but they're bigger, heavier, and more expensive
- Third-party APS-C E-mount options help: Sigma 18-50mm f/2.8, Tamron 17-70mm f/2.8, Sony 70-350mm G
- The A6700 is excellent but feels like Sony's "one APS-C camera" rather than a system commitment

**The upgrade path argument:** Sony E-mount's big advantage is that if you ever go full-frame, your FE lenses come with you. Buy a Sigma 85mm f/1.4 Art for an A6700 today → it works perfectly on an A7IV tomorrow. With Fuji, you're locked into APS-C (unless you jump to GFX medium format, which is a different world).

---

## Part 3: Camera Lineup Diagrams

### Fuji X-Series Hierarchy (Current, 2026)

```
┌─────────────────────────────────────────────────────────────┐
│                    FUJIFILM X-SERIES                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  FLAGSHIP / PRO                                             │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │   X-H2S      │  │    X-H2      │                        │
│  │ 26MP stacked │  │  40MP hi-res │                        │
│  │ Speed demon  │  │  Detail king │                        │
│  │ Best AF+video│  │  8K video    │                        │
│  │ ~R30-35k used│  │ ~R28-32k used│                        │
│  └──────────────┘  └──────────────┘                        │
│         ▲ Best for action/video    ▲ Best for landscapes   │
│                                                             │
│  ENTHUSIAST / SWEET SPOT                                    │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │    X-T5      │  │    X-T4      │                        │
│  │  40MP sensor │  │  26MP sensor │                        │
│  │ Classic dials│  │ Classic dials│                        │
│  │ Tilt screen  │  │ Flip screen  │                        │
│  │ AI AF, 7-stop│  │ Older AF     │                        │
│  │ ~R22-28k used│  │ ~R15-20k used│  ← YOUR RESEARCH      │
│  └──────────────┘  └──────────────┘    SWEET SPOT          │
│         ▲ Best all-rounder         ▲ Best value pro body   │
│                                                             │
│  MID-RANGE / COMPACT                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    X-S20     │  │    X-S10     │  │    X-M5      │     │
│  │  26MP, AI AF │  │  26MP, older │  │  26MP, tiny  │     │
│  │ PASM dial    │  │ PASM dial    │  │ No viewfinder│     │
│  │ Best vlog    │  │ Budget IBIS  │  │ Content focus│     │
│  │ ~R15-19k used│  │ ~R9-11k used │  │ ~R15k used   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  FIXED LENS (special category)                              │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │   X100VI     │  │   X100V      │                        │
│  │  40MP, 23mm  │  │  26MP, 23mm  │                        │
│  │ Impossible   │  │ ~R22k used   │                        │
│  │ to find new  │  │ (if you can  │                        │
│  │              │  │  find one)   │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘

KEY SENSOR GENERATIONS:
  X-Trans 4 (26MP): X-T4, X-S10, X-T30 II — good AF, proven
  X-Trans 5 HR (40MP): X-T5, X-H2, X100VI — best detail
  X-Trans 5 HS (26MP stacked): X-H2S, X-S20, X-M5 — best AF + speed
```

### Sony Lineup Hierarchy (Current, 2026)

```
┌─────────────────────────────────────────────────────────────┐
│                      SONY ALPHA                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  FULL-FRAME (where Sony's heart is)                         │
│                                                             │
│  ┌─ HIGH-RES ──┐  ┌─ SPEED ─────┐  ┌─ ALL-ROUND ──┐      │
│  │   A7R V     │  │    A9 III   │  │    A7 IV     │      │
│  │  61MP       │  │  Global     │  │  33MP        │      │
│  │  Landscape  │  │  shutter    │  │  Best hybrid │      │
│  │  Studio     │  │  Sports/pro │  │  ← YOU USED  │      │
│  │  ~R45k+ used│  │  ~R80k+     │  │  ~R25-30k    │      │
│  └─────────────┘  └─────────────┘  └──────────────┘      │
│                                                             │
│  ┌─ COMPACT FF ─┐  ┌─ VIDEO ────┐  ┌─ CINEMA ────┐      │
│  │   A7C II     │  │   A7S III  │  │   FX3/FX6   │      │
│  │  33MP        │  │  12MP      │  │  Cinema line │      │
│  │  Same as A7IV│  │  Low-light │  │              │      │
│  │  but smaller │  │  king      │  │              │      │
│  │  ~R25-28k    │  │  ~R35k+    │  │              │      │
│  └──────────────┘  └─────────────┘  └──────────────┘      │
│         ▲                                                   │
│    A7C II = A7IV in a smaller body (same sensor+processor)  │
│                                                             │
│  APS-C (Sony's "other" system)                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │    A6700     │  │   ZV-E10 II │  │    A6400     │     │
│  │  26MP, AI AF │  │  Vlog focus  │  │  Older but   │     │
│  │  Best APS-C  │  │  Budget      │  │  solid AF    │     │
│  │  Sony makes  │  │  ~R10-12k    │  │  ~R10-13k    │     │
│  │  ~R28-35k    │  │              │  │              │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│                                                             │
│  DISCONTINUED BUT AVAILABLE USED                            │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │    A6600     │  │    A6500     │                        │
│  │  Good AF     │  │  Aging      │                        │
│  │  Great batt  │  │  Avoid      │                        │
│  │  ~R13-16k    │  │  ~R8-11k    │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

### Head-to-Head: The Models That Matter For You

```
BUDGET TIERS & WHAT YOU GET (SA used prices, ZAR)

R8-12k    ┃ Fuji X-S10          vs  Sony A6500/ZV-E10
          ┃ ✅ IBIS, film sims      ❌ Old AF (A6500) or no IBIS (ZV-E10)
          ┃ ✅ Great ecosystem       ⚠️ Limited APS-C lenses
          ┃ Winner: Fuji X-S10
          ┃
R13-20k   ┃ Fuji X-T4           vs  Sony A6600
          ┃ ✅ Pro build, dual SD    ✅ Best AF tracking in class
          ┃ ✅ 4K/60 10-bit          ❌ No 4K/60, single SD
          ┃ ✅ Flip screen            ✅ Monster battery
          ┃ Winner: Fuji X-T4 (unless AF tracking is #1 priority)
          ┃
R15-22k   ┃ Fuji X-S20 / X-T5   vs  Sony A6700 (stretch)
          ┃ ✅ AI AF on both         ✅ Best Sony APS-C ever
          ┃ ✅ X-T5 = 40MP!          ✅ AI AF, 4K/120
          ┃ ✅ Better lens ecosystem  ⚠️ Lens ecosystem weaker
          ┃ Toss-up: depends on your priorities
          ┃
R25-30k   ┃ (no Fuji equivalent)  vs  Sony A7IV / A7C II
          ┃                           ✅ FULL FRAME
          ┃                           ✅ 33MP, incredible AF
          ┃                           ✅ Seamless Lightroom RAW
          ┃                           ✅ The experience you already loved
          ┃                           ❌ Bigger, heavier, pricier lenses
```

---

## Part 4: The Full-Frame Question (Based on Your Experience)

This is the elephant in the room. You shot your friend's A7IV with:

- **Tamron 35-150mm f/2-2.8** — a full-frame zoom that doesn't exist in APS-C
- **Sigma 85mm f/1.4 Art** — on full-frame, this gives you razor-thin DOF

You were shooting at f/1.4–2.5 and loving it. Here's what you need to understand:

### Depth of Field: Full-Frame vs APS-C

```
EQUIVALENT DEPTH OF FIELD (approximate)

Full-frame 85mm f/1.4  ≈  APS-C 56mm f/0.9  (doesn't exist!)
Full-frame 85mm f/2.0  ≈  APS-C 56mm f/1.2  (Fuji XF 56mm f/1.2)
Full-frame 50mm f/1.4  ≈  APS-C 33mm f/0.9  (doesn't exist!)
Full-frame 35mm f/2.0  ≈  APS-C 23mm f/1.4  (Fuji XF 23mm f/1.4)

The 1.5x crop factor applies to BOTH focal length AND effective DOF.
To match FF f/1.4 bokeh on APS-C, you'd need f/0.9 — which doesn't exist.
The fastest APS-C lenses (f/1.2) match FF at roughly f/1.8.
```

**Translation:** The creamy subject isolation you got at f/1.4 on the 85mm Art on full-frame? You literally cannot replicate that on APS-C. The closest Fuji gets is the XF 56mm f/1.2 (≈ 85mm f/1.8 equivalent). It's still beautiful bokeh, but it's not the same.

### The Tamron 35-150mm f/2-2.8 Problem

This lens is a unicorn. There's nothing like it in APS-C land. On Fuji, to cover the equivalent range (23-100mm on APS-C ≈ 35-150mm FF), you'd need:

- XF 18-55mm f/2.8-4 (27-84mm equiv) — slower aperture
- XF 50-140mm f/2.8 (75-210mm equiv) — doesn't cover the wide end
- Or carry 2-3 primes

The Tamron is a full-frame luxury that APS-C can't match in a single lens.

---

## Part 5: Realistic Scenarios For You

### Scenario A: "I want what I experienced" → Sony Full-Frame

**Camera:** Sony A7C II or A7IV (used, R25-28k)  
**Why A7C II over A7IV:** Same sensor, same processor, same image quality. A7C II is smaller/lighter, has a slightly newer AF algorithm, and a flip screen. A7IV has a bigger grip, dual card slots, and a better EVF. For a hobbyist, A7C II is probably the better pick.

**Starter lens kit:**
- Tamron 35-150mm f/2-2.8 (~R25-30k used) — the do-everything lens
- OR start cheaper: Sony FE 28-70mm kit + Sigma 85mm f/1.4 Art (R15k on Carbonite in Stellenbosch right now!)

**Total cost:** R40-55k for body + one great lens  
**Pros:** Seamless Lightroom RAW, the DOF you loved, upgrade path to A7RV/A9 later  
**Cons:** Expensive, bigger kit, heavier

### Scenario B: "Best value APS-C system" → Fuji X-T4

**Camera:** Fuji X-T4 (used, R15-20k)  
**Why:** Pro build, weather sealed, dual cards, 4K/60 10-bit, IBIS, classic dials. Best value in the Fuji lineup right now.

**Starter lens kit:**
- XF 35mm f/2 WR (R3,900 on Carbonite in Somerset West!) — everyday prime
- XF 18-55mm f/2.8-4 (available on Carbonite in JHB) — versatile zoom
- Later: XF 56mm f/1.2 for portraits, XF 50-140mm f/2.8 (R13k on Carbonite in CT!)

**Total cost:** R20-25k for body + 1-2 lenses  
**Pros:** Cheaper, lighter, better APS-C lens ecosystem, film sims for SOOC  
**Cons:** Lightroom RAW needs the checkbox, can't match FF bokeh, older AF

### Scenario C: "Modern Fuji with best AF" → Fuji X-T5

**Camera:** Fuji X-T5 (used, R22-28k)  
**Why:** 40MP sensor (more detail than any Sony APS-C), AI subject detection AF, 7-stop IBIS, classic dials. The consensus "best Fuji for most people" in 2025/2026.

**Starter lens kit:** Same as Scenario B  
**Total cost:** R28-35k for body + lenses  
**Pros:** 40MP resolution rivals full-frame detail, modern AF, best Fuji stills camera  
**Cons:** Tilt screen (not flip), no 4K/60 internal, approaching FF Sony pricing

### Scenario D: "Budget entry, figure it out later" → Fuji X-S10

**Camera:** Fuji X-S10 (R9,999 at Cameras4Africa with warranty)  
**Why:** Cheapest way into a modern IBIS mirrorless with great image quality.

**Total cost:** R12-16k for body + a prime  
**Pros:** Lowest entry cost, still great images, full X-mount lens compatibility  
**Cons:** Older AF, no weather sealing, smaller battery, PASM dial (not Fuji dials)

---

## Part 6: What's Actually Available in Cape Town Right Now

From your Carbonite listings (Western Cape, active):

### Fuji Gear in/near Cape Town
| Item | Price | Location | Condition |
|------|-------|----------|-----------|
| XF 35mm f/2 WR | R3,900 | Somerset West | Excellent, with POP |
| XF 27mm f/2.8 WR | R6,000 | City Center | Excellent |
| XF 55-200mm f/3.5-4.8 | R4,000 | Cape Town | Good |
| XF 50-140mm f/2.8 | R13,000 | Northern Suburbs | Excellent |
| X-T1 body | R5,000 | Cape Town | Excellent |
| XA-7 body | R6,500-8,500 | Southern Suburbs | Good |
| XC 15-45mm kit lens | R2,500 | Northern Suburbs | Excellent |

### Sony Gear in/near Cape Town
| Item | Price | Location | Condition |
|------|-------|----------|-----------|
| Sigma 85mm f/1.4 Art (E) | R15,000 | Stellenbosch | Excellent, POP |
| Zeiss Loxia 21mm f/2.8 (E) | R10,000 | Stellenbosch | Good |
| A7C II + 28-60mm [SOLD] | R27,999 | Southern Suburbs | Excellent |
| ZV-E10 body | R11,000 | Southern Suburbs | Used |
| A6700 kit | R35,000 | Southern Suburbs | Excellent |
| Godox flash + trigger (Sony) | R5,000 | Stellenbosch | Excellent |

**Note:** The Sigma 85mm f/1.4 Art in Stellenbosch for R15k is a great deal — that's the exact lens you shot with on your friend's camera. If you go Sony, grab that.

---

## Part 7: Decision Matrix

```
                        FUJI        SONY APS-C    SONY FF
                        (X-T4/T5)   (A6700)       (A7IV/A7CII)
                        ─────────   ──────────    ────────────
RAW + Lightroom ease      7/10        9/10          10/10
Film sims / SOOC JPEG    10/10        3/10           3/10
APS-C lens ecosystem      9/10        5/10           N/A
Shallow DOF potential     6/10        6/10          10/10
AF tracking               7/10*       9/10           9/10
Body + 1 lens cost (ZAR) ~R20k       ~R35k         ~R40k+
Size & weight             8/10        8/10           5/10
Second-hand availability  7/10        5/10           7/10
  (in SA)
Upgrade path              6/10        8/10**         9/10
Fun factor / tactile      9/10        6/10           7/10

* X-T5 scores 9/10 for AF
** APS-C Sony lenses work on FF bodies too
```

---

## Part 8: My Honest Take

Given what you've told me:

1. **You shoot RAW and edit in Lightroom** → This tilts toward Sony. The Fuji film sim advantage evaporates in a RAW workflow.

2. **You loved shooting at f/1.4-2.5 on the 85mm Art** → This is a full-frame experience. APS-C can't replicate it. If that shallow DOF is what made you fall in love, you want full-frame.

3. **You enjoyed the 35-150mm zoom range** → That Tamron is a full-frame lens. No APS-C equivalent exists.

4. **You're in Cape Town and happy to buy second-hand** → Good second-hand Sony FF availability on Carbonite. Fuji bodies are harder to find locally but lenses are well-represented.

5. **You're a hobbyist/enthusiast** → You don't need dual card slots or weather sealing. The A7C II's compact size is a real advantage for carrying it around.

**If budget allows (R40-50k total):** Sony A7C II (used) + Sigma 85mm f/1.4 Art (R15k in Stellenbosch) + a versatile zoom later. You already know you love this combo.

**If budget is tighter (R20-25k total):** Fuji X-T4 + XF 35mm f/2 WR (R3,900 in Somerset West). Incredible value, and you can build out the lens kit cheaply over time. Just know you're trading the shallow DOF experience for a more compact, tactile, and affordable system.

**The "have your cake" option:** Buy a used Sony A6700 or A6600 now with the Sigma 85mm f/1.4 Art. Shoot APS-C Sony today, and when you're ready, upgrade the body to A7C II / A7IV and your lenses come with you. The 85mm Art on APS-C gives you a ~127mm f/1.4 equivalent field of view (though DOF is still APS-C-equivalent ~f/2.1).

---

## Sources

- Your existing `camera_research.md` — pricing and feature comparison data
- Your Carbonite listings — live second-hand availability in SA
- Your review files — scored assessments of specific gear
- [Thomas Fitzgerald Photography](https://blog.thomasfitzgeraldphotography.com/blog/2025/7/the-best-way-to-process-fujifilm-x-trans-files-in-lightroom-in-2025) — Lightroom X-Trans processing guide (content rephrased for compliance)
- [Mirrorless Comparison](https://mirrorlesscomparison.com/sony-vs-sony/a7c-ii-vs-a7-iv/) — A7C II vs A7IV analysis (content rephrased)
- [DPReview forums](https://www.dpreview.com/forums/) — community consensus on Fuji vs Sony APS-C
- [Alpha Shooters](https://www.alphashooters.com/) — Sony ecosystem comparisons (content rephrased)
