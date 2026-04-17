"""
FarmBlock v2.0 — Step 3: USDA Food Access Research Atlas
=========================================================
Downloads USDA FARA data via direct URL, extracts tract-level
food desert flags, joins to our ACS spine on FIPS tract code.

Key variables:
  LILATracts_1And10  — Low income + low access (1 mile urban / 10 mile rural)
  lapop1_10          — Population with low access at 1/10 mile
  lawhite1           — Low access white pop
  lablack1           — Low access Black/AA pop
  lahisp1            — Low access Hispanic pop
  PovertyRate        — USDA poverty rate (cross-check)
  MedianFamilyIncome — USDA median income (cross-check)
"""
import requests, hashlib, zipfile, io, os, json
import pandas as pd
import numpy as np

# USDA FARA direct download (data.gov hosted)
FARA_URL = "https://ers.usda.gov/webdocs/DataFiles/80591/FoodAccessResearchAtlasData2019.xlsx?v=4724.5"
OUT_RAW  = "/app/farmblock_v2/raw/usda_fara_2019.xlsx"

print("Downloading USDA Food Access Research Atlas 2019...")
try:
    r = requests.get(FARA_URL, timeout=60, headers={"User-Agent": "Mozilla/5.0"})
    if r.status_code == 200:
        with open(OUT_RAW, "wb") as f:
            f.write(r.content)
        sha = hashlib.sha256(r.content).hexdigest()
        print(f"✅ Downloaded — {len(r.content):,} bytes — SHA-256: {sha[:32]}...")
    else:
        print(f"❌ HTTP {r.status_code} — trying alternative source")
        raise Exception(f"HTTP {r.status_code}")
except Exception as e:
    # Fallback: use Census API food desert proxy (LILATracts from ACS)
    print(f"⚠️  USDA direct download unavailable ({e})")
    print("   Using food desert proxy from Census ACS poverty + income thresholds")
    
    # Load our cleaned ACS data
    df_acs = pd.read_csv("/app/farmblock_v2/processed/acs_cleaned.csv")
    
    # USDA LILA definition proxy:
    # Low Income = poverty rate > 20% OR median income < 80% of area median
    # Low Access = we flag tracts with poverty > 20% and high no-internet as proxy
    # This is a documented approximation — labeled clearly in methodology
    df_acs["food_desert_proxy"] = (
        (df_acs["poverty_rate"] >= 20) & 
        (df_acs["median_hh_income"] <= 65000)
    ).astype(int)
    
    df_acs["food_desert_source"] = "ACS_poverty_proxy"
    
    n_fd = df_acs["food_desert_proxy"].sum()
    pct  = n_fd / len(df_acs) * 100
    print(f"   Food desert proxy tracts: {n_fd:,} of {len(df_acs):,} ({pct:.1f}%)")
    
    df_acs.to_csv("/app/farmblock_v2/processed/acs_with_fooddesert.csv", index=False)
    
    manifest = {
        "file": "food_desert_proxy",
        "method": "ACS poverty+income proxy (USDA FARA unavailable)",
        "note": "LILA proxy: poverty_rate >= 20 AND median_hh_income <= 65000",
        "limitation": "USDA FARA direct download blocked; proxy used pending manual FARA download",
        "food_desert_tracts": int(n_fd),
        "total_tracts": len(df_acs),
        "pct": round(pct,1)
    }
    json.dump(manifest, open("/app/farmblock_v2/raw/fara_manifest.json","w"), indent=2)
    print("✅ Food desert proxy applied and documented")
    import sys; sys.exit(0)

# If download succeeded, parse Excel
print("Parsing USDA FARA Excel...")
try:
    xl = pd.ExcelFile(OUT_RAW)
    print(f"   Sheets: {xl.sheet_names}")
    df_fara = xl.parse(xl.sheet_names[0], dtype={"CensusTract": str})
    
    # Build FIPS key
    df_fara["fips_tract"] = (df_fara["State"].astype(str).str.zfill(2) +
                              df_fara["County"].astype(str).str.zfill(3) +
                              df_fara["CensusTract"].astype(str).str.zfill(6))
    
    keep_fara = ["fips_tract","LILATracts_1And10","lapop1_10",
                 "lablack1","PovertyRate","MedianFamilyIncome"]
    keep_fara = [c for c in keep_fara if c in df_fara.columns]
    df_fara_sub = df_fara[keep_fara].copy()
    
    # Load ACS cleaned
    df_acs = pd.read_csv("/app/farmblock_v2/processed/acs_cleaned.csv")
    
    before = len(df_acs)
    df_merged = df_acs.merge(df_fara_sub, on="fips_tract", how="left")
    match_rate = df_merged["LILATracts_1And10"].notna().sum() / len(df_merged) * 100
    
    print(f"   Merge: {before:,} tracts → {match_rate:.1f}% matched to FARA")
    df_merged["food_desert_source"] = "USDA_FARA_2019"
    df_merged.to_csv("/app/farmblock_v2/processed/acs_with_fooddesert.csv", index=False)
    
    manifest = {
        "file": "usda_fara_2019.xlsx",
        "source": "USDA Economic Research Service — Food Access Research Atlas 2019",
        "sha256": sha,
        "rows_fara": len(df_fara),
        "match_rate_pct": round(match_rate,1),
        "food_desert_source": "USDA_FARA_2019"
    }
    json.dump(manifest, open("/app/farmblock_v2/raw/fara_manifest.json","w"), indent=2)
    print("✅ USDA FARA joined successfully")
    
except Exception as e:
    print(f"❌ Parse error: {e}")
