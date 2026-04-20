# Chapter 3: Research Methodology

**Project:** Black Distress Index + FarmBlock Distress Index
**Publisher:** E5 Enclave Incorporated | EIN: 99-3822441
**Version:** 2.0 | **Date:** April 20, 2026
**Authority:** Built directly from GitHub canonical sources
**DAG:** methodology-chapter-v2-2026-0420
**License:** CC0 1.0 Universal

---

## 3.1 Research Design Overview

This research employs a mixed-method observational design combining longitudinal secondary data analysis with cross-sectional composite index construction. The project produces two distinct but architecturally linked instruments:

**Product A — The Black Distress Index (BDI):** A national longitudinal structural record documenting eight dimensions of Black community disparity from 1991 through 2024, with historical framing extending to 1514. The BDI operates as a forensic documentation system — it does not model cause and effect. It records what happened and when, across verifiable federal and institutional data series.

**Product B — The FarmBlock Food Distress Index (FDI):** A place-based intervention prioritization instrument scoring structural co-occurrence at the census tract level (15,578 tracts, 50 cities) and at the county level (24-county published pilot; approximately 3,144 counties in estimated full coverage). The FDI is a correlation instrument. It identifies communities where structural burdens cluster. It does not assert that any one dimension causes another.

The two instruments share a source architecture and governance protocol but serve different analytical functions. The BDI answers the question: *What has the structural record shown across time?* The FDI answers: *Where do these conditions concentrate now, and in what combination?*

Neither instrument makes causal claims. Both are designed for use in grant applications, policy testimony, litigation support, community organizing, and academic research contexts where evidentiary precision — not narrative assertion — is the standard.

---

## 3.2 Dataset Architecture

The data stack is organized into four layers. Each layer has a defined scope, unit of analysis, and governance rule. Layers do not substitute for one another.

### Layer 1 — Sovereign Raw Evidence Archive
**Repository:** `bdi-raw-data-vault` (GitHub: IAMGODIAM)
**Unit of analysis:** Series-level observations — annual, decennial, event-count, and aggregate records
**Content:** Approximately 14,811 verified data points across 17 active files
**Rule:** Primary source data is committed unmodified before any analysis. No scoring at this layer. All transformations happen downstream.
**Sources include:** BLS Local Area Unemployment Statistics, U.S. Census Bureau (ACS, CPS, decennial), NCHS National Vital Statistics, BJS Prisoners series, Slave Voyages Database, NAEP Main Assessment, CFPB HMDA, Mapping Police Violence, EPA EJScreen (via Public Environmental Data Partners), USDA FARA

### Layer 2 — Pillar Metric Layer (National Structural Record)
**Repository:** `bdi-sovereign-dataset`
**Unit of analysis:** Flagship pillar metrics — disparity ratios, percentage-point gaps, absolute burden measures
**Content:** 1,574 verified empirical observations across 8 pillars
**Empirical window:** 1991–2024 (scoring series); 1514–1866 (Slave Voyages historical context — separate framing, separate pipeline)
**Formula:** See Section 3.4

### Layer 3 — Place-Level Compound Distress Layer
**Repository (tract):** `farmblock-data` — 15,578 census tracts, 50 priority cities
**Repository (county):** `farmblock-dataset` — 24-county pilot published; ~3,144-county estimated full scope across 17 states
**Unit of analysis:** FDI composite score (0–100) per tract or county
**Formula:** See Section 3.4

### Layer 4 — Forensic Narrative and Analytical Record
**Repository:** `bdi-raw-data-vault/reports/`
**Content:** Analytical reports, claim triage records, scientific adjustment memos, peer review documentation

The architecture enforces a principle of evidentiary separation: raw data is never modified, transformation logic is documented in methodology files, and canonical numbers for public use are locked in the Stack Truth Table (see Section 3.4).

---

## 3.3 Data Sourcing

### 3.3.1 BDI National Structural Record — Eight Pillars

**Pillar 1 — Economic**
- Federal Reserve Survey of Consumer Finances (SCF): wealth data, 1989–2022 vintages
- U.S. Census Bureau Current Population Survey (CPS): poverty rates, 1991–2022
- U.S. Census Bureau American Community Survey (ACS): homeownership, income, 2022–2023 vintages
- BLS Local Area Unemployment Statistics: annual unemployment by race, 1991–2024

**Pillar 2 — Health**
- NCHS National Center for Health Statistics: life expectancy by race, 1991–2022; maternal mortality rates, 2018–2024 (Hoyert 2024)
- CDC PLACES: small-area modeled estimates for chronic disease burden (diabetes, hypertension, obesity), 2023 vintage

**Pillar 3 — Criminal Justice**
- BJS Prisoners series: incarceration rates by race, 1980–2022
- Mapping Police Violence: police killing rates by race, 2013–2024
- Sentencing Project: supplementary incarceration ratio documentation

**Pillar 4 — Education**
- NAEP Main Assessment: 4th and 8th grade reading and math scores by race, 1992–2022

**Pillar 5 — Housing**
- U.S. Census Bureau / CPS: homeownership by race, decennial and annual vintages
- CFPB HMDA: mortgage denial rates by race, 2023 public dataset
- Graetz et al. (2023) PNAS: eviction and eviction filing rates by race

**Pillar 6 — Environmental**
- EPA EJScreen (via Public Environmental Data Partners, screening-tools.com/epa-ejscreen; note: removed from EPA.gov February 5, 2025)
- Tessum et al. (2021) and Mikati et al. (2018): supplementary corroboration

**Pillar 7 — Political and Civic**
- U.S. Census Bureau Current Population Survey November supplement: voter registration and turnout by race
- NCSL and Brennan Center: voting rights restriction documentation

**Pillar 8 — Historical Structural Context**
- Slave Voyages Database (slavevoyages.org, 2023 edition): 12.5 million Africans embarked; 10.7 million disembarked in the Americas; first recorded voyage 1514
- Federal Reserve / NCRC: redlining and lending discrimination studies
- FHWA and academic literature: urban highway displacement documentation

### 3.3.2 FDI Place-Level Instrument — Tract Layer

| Source | Variables | Vintage |
|--------|-----------|---------|
| Census Bureau ACS 5-Year | Poverty rate, median household income, internet access, housing vacancy rate, racial composition | 2023 |
| CDC PLACES | Diabetes prevalence, hypertension prevalence, obesity prevalence | 2023 |
| USDA FARA (proxy) | Food desert designation | 2019 proxy via ACS income/poverty thresholds |

**Food desert proxy note:** USDA FARA direct download was unavailable (HTTP 404 at time of collection). The proxy applied is: `food_desert_proxy = 1 WHERE poverty_rate ≥ 20% AND median_household_income ≤ $65,000`. This approximates the USDA Low-Income, Low-Access (LILA) standard. All rows are labeled to distinguish proxy-designated from directly confirmed designations.

### 3.3.3 FDI Place-Level Instrument — County Layer

| Source | Variables | Vintage |
|--------|-----------|---------|
| BLS Local Area Unemployment Statistics | County unemployment rate | 2025 |
| Census Bureau ACS 5-Year | Poverty rate, income, racial composition | 2022 |
| CDC PLACES | Health burden indicators | 2023 |
| Census Bureau ACS 5-Year | Internet access, housing vacancy | 2022 |

---

## 3.4 Validation Architecture — Stack Truth Table and Claim Triage Protocol

### The Stack Truth Table

The project maintains a canonical crosswalk document — the Stack Truth Table (`STACK_TRUTH_TABLE.md`, committed to `bdi-raw-data-vault`) — that resolves conflicts between repositories, methodology files, READMEs, and paper language. The governing rule: when any document conflicts with the Stack Truth Table, the Stack Truth Table wins and the other document is updated.

The Stack Truth Table locks the following canonical public claims:

| Claim | Locked Value | Source |
|-------|-------------|--------|
| Tracts scored (FDI v2.0) | **15,578** | `processed/farmblock_fdi_v2.csv` row count, verified |
| Cities ranked (FDI v2.0) | **50** | `processed/farmblock_city_rankings.csv` row count, verified |
| Cities in county dataset | **53** | `processed/farmblock_cities_v2.csv` row count, verified |
| Counties in Phase 2 pilot | **24** | `farmblock_fdi_phase2.csv` row count, verified |
| Counties in Phase 3 estimated scope | **~3,144** | `farmblock_phase3_manifest.json` coverage field |
| BDI empirical observations | **1,574** | Verified JSON count per BDI_QUANT_SPEC.md counting rule |
| Raw vault observations | **~14,811** | VAULT_MANIFEST.json v3.1 |
| BDI empirical window | **1991–2024** | BDI_QUANT_SPEC.md §2 |
| Historical evidence anchor | **1514** | Slave Voyages DB, first recorded voyage |
| Priority states (BDI composite) | **17** | bdi_sovereign_dataset_v1.json state_scores |

**Data point counting rule (BDI_QUANT_SPEC.md §3):** One data point equals one row in a time series or one unique observation record. JSON metadata keys (source, pillar, notes) are explicitly excluded. The earlier public claim of 1,855 data points included metadata keys as data points — this was incorrect. The corrected figure is 1,574 verified empirical observations.

### The BDI Claim Triage Matrix

All public claims in research outputs are classified against four evidentiary categories before publication:

- **source-confirmed:** claim matches primary source at the stated vintage; safe to publish as-is with footnote
- **source-conflicted:** claim appears in draft but does not match primary source value, geography, or vintage; requires rewrite per triage guidance before publication
- **internally-derived:** claim is derived from E5 Enclave methodology not yet published externally; requires methodology publication or claim replacement before external sharing
- **citation-vintage-correction:** primary source is correct but URL or institutional location has changed (e.g., EPA EJScreen removed from EPA.gov, February 5, 2025; now via Public Environmental Data Partners)

The current Claim Triage Matrix (`BDI_CLAIM_TRIAGE_MATRIX.md`, committed to both `bdi-raw-data-vault` and `farmblock-data`) documents 27 claims across all eight pillars:

| Status | Count |
|--------|-------|
| source-confirmed | 10 |
| source-conflicted | 11 |
| internally-derived | 4 |
| citation-vintage-correction | 2 |
| **Total** | **27** |

**Five highest-priority fixes required before external sharing:**

1. **Slave Voyages (HI-1):** Distinguish "12.5 million embarked" from "10.7 million disembarked in the Americas" — these are different figures. Current draft conflates them.
2. **Cancer Alley geography (H-3/CD-5):** 85% Black is a fence-line census tract figure, not a parish-level figure. Parish level ranges from 22–57% Black. Specify geography to prevent factual challenge.
3. **NAEP gap (ED-1):** Current draft cites 20-point gap. Verified NAEP 2022 figure is 24 points. Parity timeline in draft is also incorrect by a factor of approximately two.
4. **Humphreys County poverty (CD-6):** Draft uses 37% (ACS 2019 vintage). Current figure is 32.1% (ACS 2022). Child poverty figure of 55% (ACS 2022) is more powerful and current. Recommend updating to current vintage.
5. **Section 3 HUD "$4.5 billion gap" (HO-3):** No published source exists for this aggregate. Replace with HUD OIG (2013) finding: 53% of PHAs did not file required Section 3 reports.

### Dual-Source Verification Protocol

All primary claims in the BDI National Structural Record are verified against at least two independent sources before commitment to the vault. The `dual_source_log.json` file in `bdi-raw-data-vault` records the source pair, verification date, and any discrepancy notes for each verified series. Series that cannot be verified against two independent sources are flagged as single-source and labeled accordingly in the dataset.

### FDI Quality Assurance

The FDI tract pipeline applies the following validation checks before publication:
- Dimension values confirmed within 0–1 normalization bounds
- FDI composite confirmed between 0–100
- D4 health burden: confirmed using CDC PLACES direct measurement (diabetes + hypertension mean); not proxied in v2.0. Where CDC PLACES data is unavailable for a tract, D4 is imputed to zero — a conservative choice documented in LIMITATIONS.md.
- Food desert proxy: all rows labeled (`food_desert_proxy_flag`) distinguishing proxy-assigned from FARA-confirmed designations

---

## 3.5 Scoring Formulas

### 3.5.1 BDI National Composite (Product A)

```
BDI_composite = Economic×0.20 + Health×0.20 + CriminalJustice×0.20 +
                Education×0.15 + Housing×0.10 + Environmental×0.10 + Political×0.05
```

**Weighting rationale:**
- Economic (20%), Health (20%), Criminal Justice (20%) carry equal highest weight — these three pillars document the most irreversible structural outcomes: wealth deprivation, mortality, and state-imposed incarceration
- Education (15%) — a high-leverage pillar that compounds across generations
- Housing (10%) — foundational wealth-building mechanism; weighted below the top three because homeownership data carries ACS survey variance at some geographies
- Environmental (10%) — growing evidentiary base; weighted moderately given recent EPA data access disruption (February 2025)
- Political (5%) — civic participation data carries the highest measurement noise of any pillar

All pillar scores normalized 0–100. Final composite normalized 0–100 across the comparison universe.

### 3.5.2 FDI Tract Composite (Product B — Tract Layer)

```
FDI_tract = (D1_economic + D2_income_deficit + D3_food_access + D4_health + D5_vacancy + D6_digital) / 6 × 100
```

Where:
- D1: `poverty_rate` (Census ACS 2023)
- D2: `1 − normalize(median_hh_income)` (inverted; lower income = higher distress)
- D3: `food_desert_proxy × 0.60 + pct_no_internet × 0.40`
- D4: `mean(pct_diabetes, pct_high_bp)` — CDC PLACES 2023 direct measurement
- D5: `vacancy_rate` (Census ACS 2023)
- D6: `pct_no_internet` (Census ACS 2023)

All dimensions min-max normalized 0–1 across all tracts in the dataset before compositing. Equal weighting (1/6 each) is the v2.0 baseline. PCA-derived weighting is recommended for v3.0.

### 3.5.3 FDI County Composite (Product B — County Layer, Phase 2)

```
FDI_county = poverty×0.25 + health×0.25 + digital×0.20 + vacancy×0.15 + Black_pct×0.15
```

**Note on racial composition variable:** The county-level formula includes `Black_pct` at 15% weight as a structural exposure proxy — not as a demographic descriptor or outcome variable. The theoretical basis is that communities with higher Black population concentration have historically been subjected to greater disinvestment, redlining, and structural exclusion. The variable captures exposure to systemic risk, not any intrinsic characteristic of race. This choice is documented in `methodology/race_variable_note.md`. The tract-level formula does not include this variable; the tract formula uses structural dimensions only.

---

## 3.6 Cross-Dataset Reconciliation

The two products share geography but operate at different resolutions. Reconciliation rules:

**Temporal alignment:** The BDI scoring series (1991–2024) and the FDI cross-sectional snapshots (ACS 2022–2023, BLS 2025) use different temporal frames by design. The BDI answers "what happened over time." The FDI answers "where is distress concentrated now." They are complementary, not substitutable.

**Geographic alignment:** FDI tract and county scores feed city and state aggregates used for cross-referencing against BDI state-level composite scores. Where city boundaries do not align with county or tract boundaries, the larger administrative unit is used and labeled.

**Product A/B separation:** The BDI national composite score and the FDI tract/county scores are distinct instruments. They share source data (CDC PLACES, ACS) but use different formulas, different geographic units, and different purposes. They must not be cited interchangeably. The Stack Truth Table "Do NOT cite for" column governs this boundary.

---

## 3.7 Methodological Choices — Explicit Rationale

**Equal weighting (FDI tract):** FDI v2.0 uses equal dimension weights as a transparent, auditable baseline. Equal weighting makes no assumption about which structural burden matters more than another — a defensible position for a v1 public release. PCA-derived or expert-assigned weighting is recommended for v3.0 but would require public disclosure of the weight-assignment process.

**Analyst-assigned weighting (FDI county and BDI composite):** The county FDI and BDI composite use analyst-assigned weights with documented rationale. These weights are disclosed in the methodology files and are subject to sensitivity testing. Alternative weight sets produce similar rank orderings in high-distress communities, which increases confidence in the core findings.

**Proxy substitution (food desert):** The USDA FARA data download was unavailable at collection time. The ACS-based proxy is documented, labeled, and subject to validation against USDA's published LILA criteria. Tracts designated as food deserts via proxy are distinguishable from any FARA-confirmed designation in the dataset. This is consistent with accepted practice in small-area data estimation.

**Normalization approach:** Min-max normalization within each dataset's geographic universe ensures scores are interpretable as relative distress rankings within the study population. It does not support cross-study comparisons without re-normalization. This is labeled explicitly on all published outputs.

**Inclusion of racial composition in county formula:** Discussed in §3.5.3. The variable captures structural exposure, not intrinsic racial characteristics. Full methodological rationale is published in `race_variable_note.md`.

---

## 3.8 Limitations

1. **USDA FARA vintage (2019):** Food access conditions may have changed post-2019. ACS proxy substituted and labeled at the row level.
2. **CDC PLACES modeled estimates:** CDC PLACES data represents small-area model estimates, not direct clinical measurement. These are the best available tract-level health burden data but carry model uncertainty.
3. **D4 health imputed to zero:** Where CDC PLACES data is unavailable for a tract, D4 is set to zero (conservative). This may understate distress in data-sparse tracts.
4. **Equal weights (FDI tract):** Not empirically validated. No dimension is demonstrated to matter more than another at the tract level. PCA-derived weighting is the recommended path for v3.0.
5. **Geographic coverage:** The FDI tract dataset covers 50 priority cities (15,578 tracts). It is not a national random sample. National coverage with weighting adjustments is planned for v3.0.
6. **ACS 5-year rolling window:** ACS 5-year estimates represent rolling averages, not point-in-time snapshots. Temporal precision is limited compared to administrative records.
7. **Correlation only:** Both the BDI and FDI identify co-occurrence of structural conditions. Neither instrument models causation. All analytical language uses co-occurrence framing.
8. **EPA EJScreen access disruption:** EJScreen was removed from EPA.gov on February 5, 2025. Current access is via Public Environmental Data Partners (screening-tools.com/epa-ejscreen). Environmental pillar data should be reverified using this updated source before final publication.
9. **Internally-derived compound distress scores:** Compound distress scores for flagship counties (e.g., Humphreys County composite 83.5) are derived from E5 Enclave methodology. The component decomposition has not yet been published externally. Before external sharing, the full component breakdown (formula, weights, normalization method, and component scores) must be published for these flagship examples.

---

## 3.9 Data Governance and Ethics

**License:** All data products are released under CC0 1.0 Universal (Public Domain). No restriction on use, distribution, or modification. No attribution required, though attribution is appreciated.

**Intended beneficiaries:** The datasets are designed for use by community organizations, legal advocates, academic researchers, policymakers, journalists, and grant writers working in communities affected by the structural conditions the data documents. The data belongs to the communities it describes.

**Black-first framing:** Per E5 Enclave's LOGOS Doctrine, all language describing affected communities avoids deficit framing. Communities are not described primarily by what they lack. Structural critique names systems and their documented effects, not populations.

**Evidentiary standard:** The BDI Claim Triage Matrix (§3.4) enforces a pre-publication evidentiary review for all public claims. Conflicted claims are rewritten before external sharing. Internally-derived claims are either supported with published methodology or replaced with verifiable source-confirmed alternatives.

**Institutional authority:** E5 Enclave Incorporated, EIN 99-3822441, is the publishing entity. All decisions about canonical numbers, formula choices, and public language rest with the board. The Stack Truth Table is the authoritative governance document for all numerical claims.

---

## 3.10 Summary

This research produces two architecturally linked instruments built on a four-layer sovereign data stack. The BDI National Structural Record documents 1,574 verified empirical observations across eight pillars and 33 years. The FDI Place Distress Instrument scores 15,578 census tracts across 50 priority cities and 24 counties in a published pilot release.

Both instruments are correlation tools, not causal models. Both are released CC0 into the public domain. Both are governed by a Stack Truth Table and Claim Triage Matrix that enforce numerical consistency across all repositories and research outputs.

The methodology is designed to withstand peer review. The limitations are disclosed. The formula choices are documented with rationale. The canonical numbers are locked and governed.

The data is built to be used — by the communities, advocates, and researchers whose work these numbers serve.

---

**Publisher:** E5 Enclave Incorporated | EIN: 99-3822441 | iamgodiam.net
**DAG:** methodology-chapter-v2-2026-0420
**Built from:** GitHub canonical sources — verified April 20, 2026
*By Grace, perfect ways.*
