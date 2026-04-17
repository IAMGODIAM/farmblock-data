"""
FarmBlock v2.0 — Step 2: Validate + Clean
==========================================
PROOF-gated. Every decision documented. No silent drops.
"""
import pandas as pd
import numpy as np
import json
from datetime import datetime

df = pd.read_csv("/app/farmblock_v2/raw/census_acs_tracts_raw.csv", dtype=str)
report = {"timestamp": "2026-04-17", "agent": "PROOF", "steps": []}

# ── STEP 1: Type conversion ──────────────────────────────────────────────────
numeric_cols = ["B17001_002E","B17001_001E","B19013_001E",
                "B02001_003E","B02001_001E","B28002_013E",
                "B28002_001E","B25002_003E","B25002_001E"]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ── STEP 2: FIPS key ─────────────────────────────────────────────────────────
df["fips_tract"] = df["state"].str.zfill(2) + df["county"].str.zfill(3) + df["tract"].str.zfill(6)
dupes = df["fips_tract"].duplicated().sum()
report["steps"].append({"step": "FIPS key", "duplicate_tracts": int(dupes)})
print(f"✅ FIPS key built — {dupes} duplicate tracts (expect 0)")

# ── STEP 3: Derive variables ─────────────────────────────────────────────────
# Poverty rate
df["poverty_rate"] = np.where(df["B17001_001E"] > 0,
    df["B17001_002E"] / df["B17001_001E"] * 100, np.nan)

# Median household income (already direct)
df["median_hh_income"] = df["B19013_001E"]

# % Black/AA
df["pct_black"] = np.where(df["B02001_001E"] > 0,
    df["B02001_003E"] / df["B02001_001E"] * 100, np.nan)

# % No internet
df["pct_no_internet"] = np.where(df["B28002_001E"] > 0,
    df["B28002_013E"] / df["B28002_001E"] * 100, np.nan)

# Vacancy rate
df["vacancy_rate"] = np.where(df["B25002_001E"] > 0,
    df["B25002_003E"] / df["B25002_001E"] * 100, np.nan)

# Total population
df["total_population"] = df["B02001_001E"]

# ── STEP 4: Range validation ─────────────────────────────────────────────────
checks = {
    "poverty_rate":    (0, 100),
    "pct_black":       (0, 100),
    "pct_no_internet": (0, 100),
    "vacancy_rate":    (0, 100),
}
for col, (lo, hi) in checks.items():
    out_of_range = ((df[col] < lo) | (df[col] > hi)).sum()
    if out_of_range > 0:
        df.loc[(df[col] < lo) | (df[col] > hi), col] = np.nan
    report["steps"].append({"step": f"range_check_{col}", "out_of_range_set_null": int(out_of_range)})

# Negative income → null
neg_income = (df["median_hh_income"] < 0).sum()
df.loc[df["median_hh_income"] < 0, "median_hh_income"] = np.nan
report["steps"].append({"step": "negative_income_nulled", "count": int(neg_income)})

# ── STEP 5: Missing value audit ──────────────────────────────────────────────
key_vars = ["poverty_rate","median_hh_income","pct_black","pct_no_internet","vacancy_rate"]
missing = {}
for v in key_vars:
    pct = df[v].isna().sum() / len(df) * 100
    missing[v] = round(pct, 2)
    print(f"   {v}: {pct:.1f}% missing")

report["steps"].append({"step": "missing_audit", "missing_pct": missing})

# ── STEP 6: Exclude zero-population tracts (uninhabited — prisons, parks, etc.)
zero_pop = (df["total_population"] <= 0) | df["total_population"].isna()
n_excluded = zero_pop.sum()
df_clean = df[~zero_pop].copy()
report["steps"].append({"step": "exclude_zero_pop", "excluded": int(n_excluded), "remaining": len(df_clean)})
print(f"\n✅ Excluded {n_excluded} zero-population tracts → {len(df_clean):,} tracts remaining")

# ── STEP 7: Imputation (median, only where <10% missing) ────────────────────
imputed_flags = []
for v in key_vars:
    miss_pct = df_clean[v].isna().sum() / len(df_clean) * 100
    if 0 < miss_pct <= 10:
        med = df_clean[v].median()
        n_imputed = df_clean[v].isna().sum()
        df_clean[f"{v}_imputed"] = df_clean[v].isna()
        df_clean[v] = df_clean[v].fillna(med)
        imputed_flags.append({"variable": v, "pct_missing": round(miss_pct,2), "imputed_with": round(med,2), "n_rows": int(n_imputed)})
        print(f"   Imputed {n_imputed} rows of {v} with median {med:.1f}")
    elif miss_pct > 10:
        print(f"   ⚠️  {v}: {miss_pct:.1f}% missing — flagged, NOT imputed")

report["steps"].append({"step": "imputation", "imputed": imputed_flags})

# ── STEP 8: Select final columns ─────────────────────────────────────────────
keep = ["fips_tract","city","state_abbr","NAME",
        "total_population",
        "poverty_rate","median_hh_income","pct_black",
        "pct_no_internet","vacancy_rate",
        "pull_date","source"]
# Add imputed flag columns if present
for v in key_vars:
    if f"{v}_imputed" in df_clean.columns:
        keep.append(f"{v}_imputed")

df_out = df_clean[keep].copy()

# ── STEP 9: Summary stats by city ────────────────────────────────────────────
city_summary = df_out.groupby("city").agg(
    tracts=("fips_tract","count"),
    median_poverty=("poverty_rate","median"),
    median_income=("median_hh_income","median"),
    median_pct_black=("pct_black","median"),
    median_no_internet=("pct_no_internet","median"),
    total_pop=("total_population","sum"),
).round(1).reset_index()
city_summary.to_csv("/app/farmblock_v2/validation/city_summary_acs.csv", index=False)

# Save
df_out.to_csv("/app/farmblock_v2/processed/acs_cleaned.csv", index=False)
json.dump(report, open("/app/farmblock_v2/validation/clean_report.json","w"), indent=2)

print(f"\n✅ VALIDATION + CLEAN COMPLETE")
print(f"   Final tracts:  {len(df_out):,}")
print(f"   Cities:        {df_out['city'].nunique()}")
print(f"   Columns:       {len(df_out.columns)}")
print(f"\n── City summary (top 10 by median poverty rate) ──")
print(city_summary.sort_values("median_poverty", ascending=False).head(10).to_string(index=False))
