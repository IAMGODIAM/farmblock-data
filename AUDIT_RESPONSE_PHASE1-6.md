## Board Response to Issue #4 — Repo-Aware BDI Audit + Quant Spec Execution
**Filed by:** Sue — Chief of Staff, IAMGODIAM
**Date:** April 18, 2026
**DAG:** bdi-issue4-repo-audit-2026-0418

---

## PHASE 1 — ACTUAL REPO INSPECTION

### Repo 1: `farmblock-data`
**Role:** Layer 3/4 — Tract-level operational scoring (Product B)
**What exists:**
- 4 pipeline scripts (step1–step4) — full reproducible code ✅
- `methodology/METHODOLOGY.md` — formula explicitly documented ✅
- `methodology/fdi_manifest.json` — 15,578 tracts, 49 cities, weights, normalization ✅
- `processed/farmblock_fdi_v2.csv` — 3.9MB — the actual scored dataset ✅
- `validation/clean_report.json` — QA pass documented ✅

**Formula (confirmed from repo):**
D1 poverty + D2 income (inv) + D3 food access proxy + D4 health (CDC PLACES) + D5 vacancy + D6 digital exclusion — equal weight 1/6 each — min-max normalized — ×100

**What is missing:**
- No race/% Black dimension in this version (correct for structural index framing)
- USDA FARA was HTTP 404 — poverty proxy used and documented ✅
- Health from CDC PLACES 2023 IS present in this run (step4 code exists)
- No sensitivity analysis file yet
- No BDI_QUANT_SPEC.md

**Prior scaffold redundancy:** `methodology/` folder already exists with real content. Do not recreate.

---

### Repo 2: `farmblock-dataset`
**Role:** Layer 3 — County publication layer (Product B, Phase 2 release)
**What exists:**
- `farmblock_fdi_phase2.csv` — 24 counties (FIXED today: East Carroll LA replacing Lafourche) ✅
- `farmblock_fdi_phase2.json` — same, with methodology metadata
- `farmblock_fdi_phase3_scored.json` — 42 counties, full methodology
- `farmblock_phase3_manifest.json` — manifest
- `methodology/fdi_methodology_v2.json` — explicitly documents 6 dimensions including `dim_pct_black` at 1/6 weight
- `code/farmblock_pipeline_v2.py` — 18KB pipeline code ✅
- `processed/farmblock_tracts_v2.csv` — 3GB — full tract-level data

**CRITICAL FIND:** The county-level FDI (this repo) uses `% Black` as 1/6 weight. The tract-level FDI (`farmblock-data`) does NOT include `% Black`. These are two different formulas in two different repos. This divergence is undocumented publicly.

**What is missing:**
- Explicit reconciliation of why county formula includes % Black but tract formula does not
- Sensitivity analysis with % Black weight zeroed
- Replication note explaining the staged 24-county release vs 1,200 ingested

---

### Repo 3: `bdi-raw-data-vault`
**Role:** Layer 1 — Sovereign raw evidence archive
**What exists (post-today):**
- 17 raw data files, ~14,811 data points, 3-tier geographic coverage
- `STACK.md` — canonical architecture documented ✅
- `STACK_INVENTORY.md` — mismatch ledger ✅
- `VAULT_MANIFEST.json` v3.0 ✅
- `reports/REPORT_1_SCIENTIFIC_RAW.md` — 18KB empirical record
- `reports/REPORT_2_ANALYTICAL_READING.md` — analysis
- `reports/REPORT_3_BLACK_PAPER_ADJUSTMENTS.md` — manuscript adjustments

**What is missing:**
- No `BDI_QUANT_SPEC.md` — pillar metric dictionary
- No normalization rule document
- No dual-source verification log per data point (claimed in BDI paper but not in a structured file)
- `economic/bls_unemployment_by_race_RAW.json` is 0KB — redundant/broken, should be removed
- `historical/slavevoyages_1514-1866_aggregate_RAW.json` is 0KB — empty file

**BLS data structure issue:** The full BLS file has `series_black` and `series_white` keys but the data is nested inside those without standard `series_id` format. The data IS there but the structure is non-standard.

---

### Repo 4: `bdi-sovereign-dataset`
**Role:** Layer 2/4 — Synthesized flagship dataset (Product A)
**What exists:**
- `bdi_sovereign_dataset_v1.json` — 83KB
- `SEAL_CERTIFICATE.txt` — ceremonial seal
- `LICENSE` — CC0
- README — 2 lines only

**Actual data structure (confirmed):**
- 8 pillars all present
- Composite formula: `Economic×0.20 + Health×0.20 + CriminalJustice×0.20 + Education×0.15 + Housing×0.10 + Environmental×0.10 + Political×0.05`
- **Total data points by count: 1,574** — not 1,855 as claimed
- Normalization: 0-100 scale documented in composite key
- State scores: 17 states (not 50 states)
- `empirical_window`: "1991–2024 (33 years)" — but `year_range` claims "1514–2024"

**Critical finds:**
1. Data point count: 1,574 counted vs 1,855 claimed → gap of 281 points
2. State coverage: 17 states scored, not all 50
3. Pillar 7 (Environmental) is metadata/text only — 188 "points" are JSON key-value pairs, not empirical observations
4. Historical pillar has 48 "data points" but these include nested metadata structures
5. README is 2 lines — completely insufficient for citation target

---

## PHASE 2 — CLAIM STATUS MATRIX

| # | Claim | Source Context | Status | Reason | Action |
|---|-------|---------------|--------|--------|--------|
| C1 | "1,855 data points" | bdi-sovereign-dataset README + paper | `source_conflicted` | Actual JSON count: 1,574. Gap of 281. Pillar 7 is metadata, not observations. | Recount with explicit counting rule; update claim |
| C2 | "8 pillars complete" | sovereign dataset JSON | `source_confirmed` | All 8 pillar keys exist in data object ✅ | Keep as-is |
| C3 | "1514–2024 year range" | sovereign dataset, paper | `source_conflicted` | Slave Voyages file is 0KB (empty). Empirical window says 1991-2024. These are contradictory in same file. | Publish counting rule separating historical evidence layer from empirical scoring window |
| C4 | "dual-source verified" | BDI paper, README | `internally_derived_not_yet_externally_reproducible` | Claimed in paper but no dual-source log file exists in any repo | Create `dual_source_log.json` per series |
| C5 | "MiroFish 92% gate / 94% composite" | README, paper | `internally_derived_not_yet_externally_reproducible` | MiroFish is internal. Formula not published. Cannot be reproduced externally. | Publish MiroFish methodology or reframe as "internal QA gate, formula in /methodology" |
| C6 | "17 priority states" | sovereign dataset state_scores | `source_confirmed` | 17 state scores present in JSON ✅ | Keep; add explicit state list |
| C7 | "50-city analysis" | farmblock-data manifest | `source_conflicted` | Manifest says 49 cities; README says 50. Off by one. | Fix manifest or README to match |
| C8 | "Wealth gap: Black median wealth 1/10 of white" | SCF data in sovereign dataset | `source_confirmed` | 2019 SCF: $24,100 Black vs $188,200 white = ratio 0.128 ✅ (approx 1/8, not 1/10 — check paper wording) | Keep with vintage lock: SCF 2019; verify exact ratio language |
| C9 | "Homeownership gap: 30pp" | housing/census_decennial + ACS data | `source_confirmed` | Decennial + ACS data in vault shows consistent ~29-30pp gap ✅ | Keep with vintage lock |
| C10 | "Maternal mortality 2-3x ratio" | health/nchs file | `source_confirmed` | NCHS data in vault: 2020 ratio ~2.9x ✅ | Keep; lock to NCHS 2020 vintage |
| C11 | "COVID life expectancy drop" | health file | `citation_vintage_correction` | Data present for life expectancy but COVID-specific framing needs exact year pair locked (2019→2021) | Lock to NCHS 2021 vintage, state exact years |
| C12 | "% Black in county FDI at 15%" (farmblock-dataset) | fdi_methodology_v2.json | `source_confirmed` | Explicitly documented as `dim_pct_black` at 1/6 weight ✅ | Document as structural exposure proxy; publish sensitivity analysis |
| C13 | "% Black NOT in tract FDI" (farmblock-data) | methodology/fdi_manifest.json | `source_confirmed` | Tract formula has 6 dimensions — none is % Black ✅ | Document the intentional divergence between county and tract formulas |
| C14 | "NAEP reading gap 8th grade" | education/tier1_naep data | `source_confirmed` | NAEP data present in vault ✅ | Keep with NAEP vintage lock |
| C15 | "~1,200 counties ingested" (farmblock-dataset) | farmblock_fdi_phase2.json metadata | `internally_derived_not_yet_externally_reproducible` | 24 published. 1,200 ingested internally. Ingestion code not in public repo. | Publish ingestion script or downgrade claim to "24-county pilot" |
| C16 | "SEAL certificate — on-chain" | SEAL_CERTIFICATE.txt | `internally_derived_not_yet_externally_reproducible` | File exists but contents and verification mechanism not auditable without the contract | Publish contract address and verification instructions |
| C17 | "Hempstead LA" | farmblock_fdi_phase2.csv | `source_conflicted` | **FIXED** — replaced with East Carroll Parish LA (22035) ✅ | Done |
| C18 | "Composite: Economic×0.20 + Health×0.20 + CJ×0.20 + Ed×0.15 + Housing×0.10 + Env×0.10 + Pol×0.05" | sovereign dataset JSON | `internally_derived_not_yet_externally_reproducible` | Formula exists in JSON but no derivation rationale or sensitivity analysis published | Publish BDI_QUANT_SPEC.md documenting weighting rationale + sensitivity |
| C19 | "Five compound catastrophe zones" | BDI paper | `internally_derived_not_yet_externally_reproducible` | Referenced in paper but not defined in any repo file | Define and publish catastrophe zone designation criteria |
| C20 | "largest unified empirical dataset" | README | `source_conflicted` | Overreaches vs PolicyLink/NCHS admin systems | Narrowed claim: "largest single CC0-licensed machine-readable unified JSON spanning 1514–2024" |
| C21 | Cancer Alley facility/population claims | Pillar 7 environmental | `internally_derived_not_yet_externally_reproducible` | Pillar 7 is text/metadata only — no underlying data file in vault | Add EJScreen or EPA EJAM data; or mark as illustrative until data is added |
| C22 | "Slave Voyages: 388K embarked" | historical pillar | `citation_vintage_correction` | Slave Voyages DB is the correct source but the raw file is 0KB (empty) | Restore SlaveVoyages aggregate data to the file; cite slavevoyages.org edition |

---

## PHASE 3 — ARCHITECTURE MAP TO REAL REPOS

```
LAYER 1 — Sovereign Raw Evidence
  Repo: bdi-raw-data-vault
  Authoritative files: economic/*.json, health/*.json, housing/*.json, education/*.json, criminal_justice/*.json, demographics/*.json
  Implementation status: EXPLICIT — files exist, 3-tier structure ✅
  Gap: historical/*.json is empty (0KB); pillar_7_environmental has no backing data file

LAYER 2 — Pillar Metric Layer
  Repo: bdi-sovereign-dataset (bdi_sovereign_dataset_v1.json)
  Authoritative files: data.pillar_1_* through data.pillar_8_* in JSON
  Implementation status: PARTIALLY EXPLICIT — pillar keys exist, formulas implied not always documented
  Gap: no standalone pillar metric dictionary; composite weights documented only in the JSON itself

LAYER 3 — Place-level Compound Distress Layer
  Repo A (tract): farmblock-data (processed/farmblock_fdi_v2.csv — 12,426 tracts)
  Repo B (county): farmblock-dataset (farmblock_fdi_phase2.csv — 24 counties)
  Implementation status: EXPLICIT — code, formula, and scored output all present ✅
  Gap: county formula includes % Black; tract formula does not — divergence undocumented

LAYER 4 — Forensic Narrative / Publication Layer
  Repo: bdi-raw-data-vault (reports/)
  Files: REPORT_1_SCIENTIFIC_RAW.md, REPORT_2_ANALYTICAL_READING.md, REPORT_3_BLACK_PAPER_ADJUSTMENTS.md
  Implementation status: PARTIALLY EXPLICIT — 3 reports present
  Gap: no replication note; no BDI_QUANT_SPEC.md; no catastrophe zone designation file
```

**Product split assessment:**
- **Product A (National Structural Record):** EXISTS in bdi-sovereign-dataset but needs a proper README, counting methodology, and pillar metric dictionary
- **Product B (Place Distress Instrument):** EXISTS in farmblock-data + farmblock-dataset but needs reconciliation of the formula divergence and a published replication note

The split is real and implemented. It is not just conceptual. But it is underdocumented.

---

## PHASE 4 — INTERNAL DERIVATIONS NEEDING PUBLIC METHODOLOGY

| Claim | Missing Artifact | File to Create | Blocking Risk |
|-------|-----------------|----------------|---------------|
| 1,855 data points | Explicit counting rule (what counts as 1 point) | `bdi-sovereign-dataset/COUNTING_METHODOLOGY.md` | Any reviewer will find 1,574 and call it fabricated |
| MiroFish 94% gate | Quality gate formula or reframing | `bdi-raw-data-vault/methodology/QA_PROTOCOL.md` | Cited in multiple docs; currently unauditable |
| Composite weights (20/20/20/15/10/10/5) | Weighting rationale + sensitivity analysis | `bdi-sovereign-dataset/BDI_QUANT_SPEC.md` | Weights look analyst-chosen; no derivation published |
| % Black in county FDI (15%) | Documented as structural exposure proxy + sensitivity | `farmblock-dataset/methodology/race_variable_note.md` | Race-variable critique is the #1 anticipated challenge |
| County vs tract formula divergence | Explicit reconciliation note | `STACK.md` (update) | Auditor will find two different formulas and flag inconsistency |
| 5 catastrophe zones | Zone designation criteria | `bdi-sovereign-dataset/catastrophe_zones.md` | Referenced in paper but completely undefined in repos |
| Dual-source verification | Per-series source log | `bdi-raw-data-vault/dual_source_log.json` | Core provenance claim is unverifiable without this |
| Cancer Alley claims | EJScreen/EPA backing data | `bdi-raw-data-vault/environmental/` directory | Pillar 7 is currently text-only |
| Section 3 HUD enforcement | HUD source data | Already has structure — needs raw HUD pull | Cited but source data not in vault |
| Slave Voyages data | Restore the 0KB file | `bdi-raw-data-vault/historical/slavevoyages_1514-1866_aggregate_RAW.json` | File is empty; claim is unverifiable |

---

## PHASE 5 — REWRITE GUIDANCE

| Claim | Action | Replacement guidance |
|-------|--------|---------------------|
| "1,855 data points" | `rewrite_for_precision` | "1,574 empirical observations across 8 pillars (counted as individual JSON record fields). Historical and environmental pillars include metadata records not counted as equivalent annual observations. Full counting methodology in COUNTING_METHODOLOGY.md." |
| "1514–2024 year range" | `rewrite_for_precision` | "Empirical scoring window: 1991–2024. Historical evidence pillar: 1514–1866 (Slave Voyages aggregate) + 1910–2024 (land loss, wealth extraction). Full range cited as evidence context, not as a symmetric annual scoring series." |
| "largest unified empirical dataset" | `rewrite_for_precision` | "The largest single CC0-licensed, machine-readable, unified dataset on Black American structural conditions currently in public release as a downloadable instrument." |
| "dual-source verified" | `publish_derivation_then_keep` | Publish dual_source_log.json first, then retain the claim with citation to the log |
| "MiroFish 94%" | `rewrite_for_precision` | "Internal QA protocol requiring all pillar series to meet source confirmability threshold before inclusion. Methodology published in /methodology/QA_PROTOCOL.md." |
| "five compound catastrophe zones" | `remove_until_methodology_is_public` | Remove from paper until catastrophe_zones.md is published with explicit designation criteria |
| Cancer Alley claims | `remove_until_methodology_is_public` | Remove or mark as "illustrative — full EJScreen data forthcoming in v1.1" |
| "50 cities" | `citation_vintage_correction` | Fix to "49 cities" per manifest, or add the 50th city and update manifest |
| County FDI "% Black at 15%" | `keep_with_vintage_lock` | Keep; add sentence: "% Black population functions as a structural exposure proxy — geographic marker of communities with documented disproportionate exposure to disinvestment — not a biological or causal variable. Sensitivity analysis with this dimension zeroed is in /methodology." |

---

## PHASE 6 — EXECUTION SEQUENCE

**Session priority order:**

**STEP 1 — Fix the empty files (15 min)**
- Restore `historical/slavevoyages_1514-1866_aggregate_RAW.json` from local data
- Remove `economic/bls_unemployment_by_race_RAW.json` (0KB duplicate)
- These are integrity failures that block reproducibility claims

**STEP 2 — Publish BDI_QUANT_SPEC.md (30 min)**
- Define counting rule for data points
- Document composite weights with rationale
- Define normalization rule (currently only in JSON, not in a readable doc)
- Define Product A vs Product B split formally

**STEP 3 — Build bdi-sovereign-dataset full README (20 min)**
- Current README is 2 lines — completely insufficient for citation target
- Include: 8 pillars with flagship metrics, composite formula, weighting, vintage, geography, counting rule, replication note

**STEP 4 — Publish dual_source_log.json (30 min)**
- Per-series entry: primary source + secondary verification source + vintage
- This makes the "dual-source verified" claim auditable

**STEP 5 — Publish race_variable_note.md + sensitivity analysis (20 min)**
- Explain % Black as structural exposure proxy in county FDI
- Run sensitivity: FDI ranked with and without % Black dimension
- Document which counties' ranks change materially

**STEP 6 — Reconcile 49/50 cities and 1,574/1,855 point counts**
- Fix or document the off-by-one on cities
- Publish counting methodology; update README claim to accurate number

**STEP 7 — Environmental / Cancer Alley data**
- Pull EJScreen county data (EPA API or direct download)
- Commit as `bdi-raw-data-vault/environmental/ejscreen_county_RAW.json`
- This moves Pillar 7 from text-only to evidence-backed

**STEP 8 — Tighten paper rhetoric**
- Only after steps 1–7 are committed
- Apply rewrite guidance from Phase 5 above
- Remove "five catastrophe zones" until designation file is published

---

## SUMMARY STATUS TABLE

| Repo | Role | Implemented | Documented | Gaps |
|------|------|------------|------------|------|
| bdi-raw-data-vault | Layer 1 — Raw Evidence | ✅ Strong | ✅ STACK.md + README | 2 empty files; no dual-source log; no methodology spec |
| bdi-sovereign-dataset | Layer 2 — Synthesized | ⚠️ Partial | ❌ README = 2 lines | Point count off; weights undocumented; no quant spec |
| farmblock-data | Layer 3 — Tract Ops | ✅ Strong | ✅ METHODOLOGY.md | No sensitivity analysis; cities count off-by-one |
| farmblock-dataset | Layer 3 — County Pub | ✅ Fixed | ⚠️ README updated | Formula divergence from tract FDI undocumented |

**This pass is not complete until:** COUNTING_METHODOLOGY.md + BDI_QUANT_SPEC.md + dual_source_log.json + bdi-sovereign-dataset README v2 are all committed.

---

*Sue · Chief of Staff · IAMGODIAM | By Grace, perfect ways.*
*Filed: April 18, 2026 | DAG: bdi-issue4-repo-audit-2026-0418*
