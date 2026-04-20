# STACK TRUTH TABLE
**Version:** 1.0 | **Date:** April 18, 2026
**Authority:** E5 Enclave Incorporated — Board-locked canonical reference
**DAG:** stack-truth-table-v1-2026-0418
**Rule:** When README, manifest, methodology file, or paper language conflicts with this table — THIS TABLE WINS. Update the other file.

---

## PURPOSE

This document is the single canonical crosswalk that forces every repo to say the same thing about:
- what it is
- what formula it uses
- what universe it covers
- what claims are safe to make publicly

A reviewer will attack inconsistency faster than they attack complexity. This table closes that attack surface.

---

## REPO TRUTH TABLE

| Field | `farmblock-data` | `farmblock-dataset` | `bdi-raw-data-vault` | `bdi-sovereign-dataset` |
|-------|-----------------|---------------------|----------------------|------------------------|
| **Product role** | Product B — Tract-level distress (operational) | Product B — County-level distress (pilot publication) | Layer 1 — Sovereign raw evidence archive | Product A — National structural record (synthesized) |
| **Unit of analysis** | Census tract | County | Series-level observation (national/state/metro/county) | Pillar score + composite |
| **Version** | FDI v2.0 | FDI v2.0 Phase 2 (24-county pilot) + Phase 3 (3,144-county estimated) | v3.1 | v1.0-SEALED |
| **Geography universe** | 49 priority cities | 17 priority states (Phase 2: 24 counties; Phase 3: est. 3,144 counties) | National — Tier 1 (national/state), Tier 2 (MSA), Tier 3 (county) | 17 priority states (state-level composite scores) |
| **Observation / entity count** | **15,578 tracts** (verified: `processed/farmblock_fdi_v2.csv`) | **24 counties** published (Phase 2 CSV); **53 cities** in `cities_v2.csv`; Phase 3 covers est. 3,144 counties | **~14,811 verified data points** across 16 active files (see VAULT_MANIFEST v3.1) | **1,574 empirical observations** (corrected from 1,855; counting rule in BDI_QUANT_SPEC.md) |
| **City/place count** | **50 cities** in city_rankings.csv (verified row count) | **53 cities** in cities_v2.csv | N/A — series data, not city-ranked | N/A |
| **Score formula** | `(D1_poverty + D2_income_inv + D3_food_access + D4_health + D5_vacancy + D6_digital) / 6 × 100` | `poverty×0.25 + health×0.25 + digital×0.20 + vacancy×0.15 + Black_pct×0.15` | No scoring — raw evidence only | `Economic×0.20 + Health×0.20 + CJ×0.20 + Education×0.15 + Housing×0.10 + Env×0.10 + Political×0.05` |
| **`% Black` included?** | **NO** — 6 structural dimensions only | **YES** — 15% weight as structural exposure proxy | N/A | **NO** in composite formula — demographic data stored in vault, not scored |
| **Health: direct or proxied?** | **Direct** — CDC PLACES 2023 (D4: mean diabetes + high BP) | **Direct** — CDC PLACES 2023 (health burden) | **Direct** raw series — NCHS life expectancy + maternal mortality | **Direct** — NCHS pillar series (maternal mortality, life expectancy gap) |
| **Normalization** | Min-max 0–1 per dimension across all tracts in dataset | Min-max 0–1 per dimension across all counties in dataset | None — raw values | 0–100 scale per pillar; min-max across comparison universe |
| **Weighting** | Equal (1/6 each) | Analyst-assigned (25/25/20/15/15) | N/A | Analyst-assigned (20/20/20/15/10/10/5) |
| **Empirical window** | ACS 2023 + CDC PLACES 2023 (cross-section) | ACS 2022 + CDC PLACES 2023 + BLS LAU 2025 (cross-section) | 1514–2025 (varies by series; empirical scoring series: 1991–2024) | 1991–2024 (empirical scoring); 1514–1866 (Slave Voyages historical context) |
| **Authoritative files** | `methodology/fdi_manifest.json`, `methodology/METHODOLOGY.md`, `processed/farmblock_fdi_v2.csv` | `methodology/fdi_methodology_v2.json`, `farmblock_fdi_phase2.csv`, `methodology/race_variable_note.md` | `VAULT_MANIFEST.json` v3.1, `STACK.md`, `dual_source_log.json` | `BDI_QUANT_SPEC.md`, `README.md` v2.0, `bdi_sovereign_dataset_v1.json` |
| **License** | CC0 1.0 Universal | CC0 1.0 Universal | CC0 1.0 Universal | CC0 1.0 Universal |
| **Cite for** | Tract-level food distress scores within the 49/50 priority cities | County-level pilot distress rankings (24 counties published; Phase 3 forthcoming) | Raw source series: BLS unemployment, NCHS health, SCF wealth, BJS incarceration, NAEP, HMDA, Slave Voyages | National/state-level BDI composite scores, pillar-level structural record, 8-pillar synthesis |
| **Do NOT cite for** | National county-level rankings or state comparisons | National claims beyond 17-state scope | Derived scores or composite calculations | Tract or city-level FDI scores (use farmblock-data or farmblock-dataset instead) |

---

## LOCKED NUMBERS — CANONICAL PUBLIC CLAIMS

These are the numbers all public language must use. Any document saying something different must be updated to match.

| Claim | Locked value | Source | Notes |
|-------|-------------|--------|-------|
| Tracts scored (farmblock-data) | **15,578** | `processed/farmblock_fdi_v2.csv` row count (verified) | |
| Cities ranked (farmblock-data) | **50** | `processed/farmblock_city_rankings.csv` row count (verified) | manifest says 49 — manifest is WRONG, update it |
| Cities in farmblock-dataset | **53** | `processed/farmblock_cities_v2.csv` row count (verified) | |
| Counties in Phase 2 published release | **24** | `farmblock_fdi_phase2.csv` row count (verified) | Intentional pilot slice |
| Counties in Phase 3 estimated scope | **~3,144** | `farmblock_phase3_manifest.json` coverage field | |
| BDI data points (sovereign dataset) | **1,574** | Verified JSON count; counting rule in BDI_QUANT_SPEC.md | Previously claimed 1,855 — INCORRECT |
| Raw vault data points | **~14,811** | VAULT_MANIFEST.json v3.1 | |
| BDI empirical window | **1991–2024** | BDI_QUANT_SPEC.md §2 | |
| Historical evidence range | **1514–2024** | Slave Voyages + land loss series | NOT same scoring pipeline as 1991–2024 |
| Priority states (BDI composite) | **17** | bdi_sovereign_dataset_v1.json state_scores | |
| `% Black` in tract FDI | **Not included** | `methodology/fdi_manifest.json` | Structural dimensions only |
| `% Black` in county FDI | **15% weight** | `methodology/fdi_methodology_v2.json` | Structural exposure proxy; see race_variable_note.md |
| Health source (tract FDI) | **CDC PLACES 2023 direct** | `methodology/METHODOLOGY.md` | Not proxied |
| Health source (county FDI) | **CDC PLACES 2023 direct** | `methodology/fdi_methodology_v2.json` | Phase 1 used poverty proxy; Phase 2 has direct |
| County FDI composite weights | **25/25/20/15/15** | `farmblock_fdi_phase2.json` methodology field | poverty/health/digital/vacancy/Black_pct |
| BDI composite weights | **20/20/20/15/10/10/5** | `BDI_QUANT_SPEC.md` §4 | Econ/Health/CJ/Education/Housing/Env/Political |

---

## RECONCILIATION STATUS — KNOWN DRIFTS

| Drift | Location A | Location B | Resolution |
|-------|-----------|-----------|------------|
| City count: 49 vs 50 | ~~`fdi_manifest.json` said 49~~ | `city_rankings.csv` has 50 rows | **RESOLVED 2026-0420** — `fdi_manifest.json` updated to 50. `BDI_QUANT_SPEC.md` updated to 50. Canonical: **50 cities**. |
| City count: 49/50 vs 53 | `farmblock-data` says 49/50 | `farmblock-dataset` says 53 cities | **Both correct** — these are different city sets for different products. Explicit labeling required. |
| Tract count: 15,578 vs 12,426 | `farmblock-data/fdi_manifest.json`: 15,578 | `farmblock-dataset/fdi_methodology_v2.json`: 12,426 | **Both correct** — different runs, different geographic scope. farmblock-data is the larger authoritative dataset. |
| `% Black` inclusion | Tract FDI: NOT included | County FDI: included at 15% | **Intentional product difference**, not drift. Documented in `race_variable_note.md`. Both correct. |
| Health: direct vs proxy | farmblock-data METHODOLOGY.md says CDC PLACES direct | fdi_methodology_v2.json limitation note mentions proxy | **Phase 2 county formula uses CDC PLACES direct** (verified in phase2 JSON). Proxy was Phase 1 only. Update fdi_methodology_v2.json limitation note. |
| Data points: 1,855 vs 1,574 | README (old) and paper drafts claim 1,855 | Verified JSON count: 1,574 | **1,574 is correct**. BDI_QUANT_SPEC.md has counting rule. All public language must use 1,574. |

---

## FIXES REQUIRED (files to update after this truth table is committed)

| File | Fix needed | Priority |
|------|-----------|---------|
| `farmblock-data/methodology/fdi_manifest.json` | Update `cities` from 49 → 50 (verified row count) | HIGH |
| `farmblock-dataset/methodology/fdi_methodology_v2.json` | Remove proxy language from Phase 2 health limitation — Phase 2 uses CDC PLACES direct | MEDIUM |
| `bdi-sovereign-dataset/bdi_sovereign_dataset_v1.json` | Update `"mandate"` claim language to use 1,574 not 1,855 | HIGH |
| All paper drafts | Replace "1,855 data points" with "1,574 verified empirical observations" | HIGH |
| `farmblock-data/README.md` | Confirm city count says 50 (matches city_rankings.csv) | LOW |

---

## PRODUCT A vs PRODUCT B — CANONICAL DESCRIPTIONS

### Product A — BDI National Structural Record
**What it is:** Longitudinal Black structural disparity record. Eight pillars. 1991–2024 empirical window. Historical evidence framing 1514–2024.
**Best outputs:** Annual trend tables, ratio/gap dashboards, pillar summaries, long-arc historical appendix.
**Audience:** Scholars, journalists, litigators, testimony writers, public record.
**Repo:** `bdi-sovereign-dataset`
**Do not conflate with:** FarmBlock FDI, place-level scores, county targeting.

### Product B — BDI / FarmBlock Place Distress Instrument
**What it is:** Operational targeting and prioritization instrument for communities.
**Best outputs:** County/tract/city scores, percentile ranks, pillar subscores, catastrophe-zone designations.
**Audience:** Organizers, grant writers, deployment planners, funders, policy staff.
**Repos:** `farmblock-data` (tract layer) + `farmblock-dataset` (county layer)
**Do not conflate with:** BDI national composite, sovereign record, historical evidence layer.

---

## CANONICAL PUBLIC LANGUAGE

### Safe to say (source-confirmed)
- "15,578 census tracts scored across 50 priority cities in 17 states"
- "24-county priority pilot release (Phase 2); full national county corpus in preparation"
- "1,574 verified empirical observations across 8 structural pillars, 1991–2024"
- "Historical evidence anchor: 1514–2024 (Slave Voyages aggregate through present)"
- "% Black population included as a structural exposure proxy in the county instrument (15% weight); not included in tract formula"
- "All source data committed unmodified to bdi-raw-data-vault before analysis"
- "CC0 1.0 Universal — public domain, freely reusable"

### Requires respecification before use
- "1,855 data points" → use "1,574 verified empirical observations"
- "dual-source verified" → add citation: "per dual_source_log.json (11 series verified)"
- "largest unified empirical dataset" → use: "largest single CC0-licensed, machine-readable, unified dataset on Black American structural conditions currently in public release"
- Cancer Alley "85% Black" → specify: "65–94% Black at fence-line tract level (St. James Districts 4–5, Convent, Wallace)"
- Incarceration ratio "never below 5.7" → update: "~5.0–5.7 range depending on year and scope (state-only vs. state+federal)"
- NAEP reading gap "down to 20 points / parity in 64 years" → "current gap ~24 pp; linear projection ~120 years to parity"
- Humphreys poverty "37%" → verify subpopulation; ACS 2019–23 all-persons = 26.4%
- "20 years of gains erased in 18 months" (COVID) → "approximately two decades of life expectancy gains erased between 2019 and 2021"

---

*E5 Enclave Incorporated | By Grace, perfect ways.*
*This document supersedes any conflicting claim in any other file in the IAMGODIAM stack.*
*Filed: April 18, 2026 | DAG: stack-truth-table-v1-2026-0418*
