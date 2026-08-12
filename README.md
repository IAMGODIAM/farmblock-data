# FarmBlock Distress Index (FDI) — v2.1
**Produced by:** E5 Enclave Incorporated
**License:** CC0 1.0 Universal (Public Domain)
**Date:** August 1, 2026
**Version:** 2.1

---

## What This Is

The FarmBlock Distress Index (FDI) is a composite measure of structural food insecurity and community disinvestment across American urban census tracts. It is designed to identify communities where multiple converging conditions — poverty, food access deficit, economic exclusion, infrastructure absence — create the conditions that E5 Enclave's FarmBlock program is built to address.

This dataset covers **15,507 census tracts** across **49 counties (48 cities, 25 states)** with documented histories of structural disinvestment. It is the foundation for E5 Enclave's national expansion research (Option C — all 74,000 US tracts — is in progress).

---

## The FDI Score (0–100)

Each tract receives a score from 0 (low distress) to 100 (highest distress), computed as the equal-weighted mean of 6 normalized dimensions:

| Dimension | Variable | Source |
|-----------|----------|--------|
| D1 Economic | Poverty rate | Census ACS 2023 B17001 |
| D2 Income | Median household income (inverted) | Census ACS 2023 B19013 |
| D3 Food access | Food-desert proxy × 60 + % without internet × 0.4 | ACS-derived proxy (documented) |
| D4 Health burden | Mean of diabetes % and high blood pressure % | CDC PLACES 2023 (tract) |
| D5 Housing vacancy | % vacant housing units | Census ACS 2023 B25002 |
| D6 Digital exclusion | % without internet access | Census ACS 2023 B28002 |

**Normalization:** min-max 0–1 per dimension across all 15,507 tracts in this dataset.
**Weighting:** Equal (1/6 each). This is an explicit assumption; sensitivity analysis with alternate weightings is recommended for peer review.
**Integrity:** the published score is independently reproducible from this specification (r = 0.9999 on recomputation; see `validation/v2_1_hygiene_report.json`).

---

## Key Findings (v2.1)

- **15,507 tracts** analyzed across 49 counties in 25 states
- **61.2 million people** in covered communities
- **165 high-distress tracts** (FDI ≥ 60) identified
- **Top cities by average FDI:** Albany GA (46.8), Macon GA (41.5), Shreveport LA (41.4), Jackson MS (41.1), Augusta GA (38.7)
- The pattern is consistent: high-FDI tracts share elevated poverty, depressed median incomes, and concentrated Black populations
- This is not a coincidence. It is a documented structural pattern.

---

## Data Files

```
/raw/
  census_manifest.json            — Census ACS pull manifest (source, vintage, SHA-256)
  fara_manifest.json              — USDA FARA reference manifest
/processed/
  farmblock_fdi_v2.csv            — 15,507 tracts with FDI scores + all variables
  farmblock_city_rankings.csv     — 48-city aggregates (median/max FDI, population, poverty)
/methodology/
  fdi_manifest.json               — Scoring specification + integrity hashes (v2.1)
  METHODOLOGY.md                  — Methods summary
  METHODOLOGY_CHAPTER_v2.md       — Full methodology chapter
  LIMITATIONS.md                  — Limitations register
/validation/
  clean_report.json               — Pipeline cleaning log (v2.0)
  v2_1_hygiene_report.json        — v2.1 dedup + correction audit trail
/code/
  step1_census_pull.py … step4_cdc_places.py — Reproducible pipeline (see below)
```

---

## Limitations

1. **USDA FARA vintage 2019** — food access conditions may have changed; ACS-derived proxy used and labeled
2. **Census ACS 5-year rolling estimates** — not point-in-time measurements
3. **CDC PLACES 2023 crude prevalence estimates** — not direct measurement; D4 imputed to 0 where unavailable (flagged per row)
4. **Equal weighting is an assumption** — not empirically derived
5. **FDI is a correlation index** — it does not establish causation
6. **Coverage limited to 49 counties** — national expansion (all 74K tracts) is the next phase
7. **Selma, AL was removed in v2.1** — its v2.0 rows were Montgomery County duplicates from a pull-configuration error; a legitimate Dallas County (Selma) pull is queued for a future release

---

## Changelog

**v2.1 (2026-08-01) — hygiene release, no methodology change:**
- Removed 71 duplicate tract rows (Montgomery County, AL tracts double-pulled under city "Selma"); every remaining row is byte-identical to v2.0
- Per-dimension min/max verified unchanged → all v2.0 FDI scores remain valid (no recomputation needed)
- Removed the corresponding Selma clone row from city rankings
- Regenerated README statistics from the CSV; corrected stale file references; aligned the dimension table with `fdi_manifest.json`
- Full audit trail: `validation/v2_1_hygiene_report.json`

**v2.0 (2026-04-17):** initial tract-level release.

---

## Reproducibility

```bash
export CENSUS_API_KEY=your_key_here
pip install -r code/requirements.txt
python3 code/step1_census_pull.py && python3 code/step2_validate_clean.py
python3 code/step3_usda_fara.py   && python3 code/step4_cdc_places.py
```

All code is CC0. All source data is from US government open data APIs.
Results are deterministic given the same source data vintage.

---

## Citation

> E5 Enclave Incorporated. (2026). *FarmBlock Distress Index v2.1: Structural Food Insecurity Across American Urban Census Tracts.* CC0 1.0 Universal. GitHub: IAMGODIAM/farmblock-data

---

## About E5 Enclave Incorporated

E5 Enclave Incorporated (EIN: 99-3822441) is a 501(c)(3) nonprofit building permanent community infrastructure in American cities where disinvestment has been policy, not accident. FarmBlock is our flagship program — integrating urban agriculture, IoT sensor networks, and supply-chain transparency into communities identified by this dataset.

**Contact:** IAMGODIAM@e5enclave.com | iamgodiam.net
**SAM.gov:** UEI H8NGXEYE2HH8 | CAGE 07E88
