# FarmBlock Distress Index (FDI) — Methodology v2.0

**Publisher:** E5 Enclave Incorporated  
**Date:** April 17, 2026 | **License:** CC0 1.0 Universal | **Version:** 2.0

## Overview
The FDI is a composite index of structural community distress across census tracts.
It maps co-occurring conditions — economic deprivation, food access deficit, health burden,
vacancy/disinvestment, and digital exclusion. It is a correlation index, not a causal model.

## Data Sources
| Source | Variables | Vintage |
|--------|-----------|---------|
| Census Bureau ACS 5-Year | Poverty, income, race, internet, vacancy | 2023 |
| CDC PLACES | Diabetes, high BP, obesity, food insecurity | 2023 |
| USDA FARA (proxy) | Food desert designation (ACS poverty proxy used) | 2019/ACS |

## FDI Dimensions (equal weight 1/6 each)
| Dim | Variable | Source |
|-----|----------|--------|
| D1 — Economic | poverty_rate | Census ACS |
| D2 — Income deficit | inverted median_hh_income | Census ACS |
| D3 — Food access | food_desert_proxy × 60 + pct_no_internet × 0.4 | ACS proxy |
| D4 — Health burden | mean(pct_diabetes, pct_high_bp) | CDC PLACES 2023 |
| D5 — Vacancy | vacancy_rate | Census ACS |
| D6 — Digital exclusion | pct_no_internet | Census ACS |

All dimensions min-max normalized 0–1 across dataset. Final FDI = mean × 100.

## Food Desert Proxy
USDA FARA direct download was unavailable (HTTP 404). Proxy:
`food_desert_proxy = 1 WHERE poverty_rate >= 20 AND median_hh_income <= $65,000`
This approximates USDA LILA definition. Conservative — likely undercounts food deserts.

## Missing Data
- <10% missing: median imputation, rows flagged `{variable}_imputed=True`
- D4 missing: set to 0 (conservative, flagged `d4_health_imputed=True`)
- Zero-population tracts excluded (166 tracts — uninhabited)

## Limitations
See LIMITATIONS.md for complete list.

## Reproducibility
```bash
export CENSUS_API_KEY=your_key
python3 code/step1_census_pull.py   # Census ACS — 50 counties
python3 code/step2_validate_clean.py # Validate, clean, FIPS-key
python3 code/step3_usda_fara.py     # USDA food desert proxy
python3 code/step4_cdc_places.py    # CDC PLACES health outcomes
```

## Citation
E5 Enclave Incorporated. (2026). *FarmBlock Distress Index v2.0*. CC0.
https://github.com/IAMGODIAM/farmblock-data
