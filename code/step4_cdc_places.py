"""
FarmBlock v2.0 — Step 4: CDC PLACES Health Outcomes
=====================================================
CDC PLACES 2024 — tract-level health outcomes.
Using CDC's open data API (Socrata) — no key required.

Variables:
  DIABETES       — % adults with diabetes
  HIGHCHOL       — % adults with high cholesterol
  BPHIGH         — % adults with high blood pressure
  OBESITY        — % adults with obesity
  CSMOKING       — % adults who smoke
  CHECKUP        — % adults with annual checkup (access proxy)
"""
import requests, json, hashlib, time
import pandas as pd
import numpy as np

# CDC PLACES API — Socrata open data
CDC_URL = "https://data.cdc.gov/resource/cwsq-ngmh.json"
params_base = {
    "$limit": 50000,
    "$offset": 0,
    "$select": "locationid,stateabbr,countyfips,tractfips,measure,data_value,category",
    "$where": "year='2023' AND geographiclevel='Census Tract' AND measure IN ('Current asthma among adults aged >=18 years','Diagnosed diabetes among adults aged >=18 years','High blood pressure among adults aged >=18 years','Obesity among adults aged >=18 years','Current smoking among adults aged >=18 years','Visits to doctor for routine checkup within the past year among adults aged >=18 years')"
}

print("Pulling CDC PLACES 2023 tract-level data...")

all_rows = []
offset   = 0

for page in range(8):  # max 400K rows
    params = params_base.copy()
    params["$offset"] = offset
    try:
        r = requests.get(CDC_URL, params=params, timeout=60)
        if r.status_code == 200:
            data = r.json()
            if not data:
                break
            all_rows.extend(data)
            print(f"  Page {page+1}: {len(data):,} rows (total: {len(all_rows):,})")
            if len(data) < 50000:
                break
            offset += 50000
            time.sleep(0.3)
        else:
            print(f"  HTTP {r.status_code} — stopping")
            break
    except Exception as e:
        print(f"  Error: {e}")
        break

if all_rows:
    df_cdc = pd.DataFrame(all_rows)
    print(f"\n✅ CDC PLACES raw: {len(df_cdc):,} rows")
    print(f"   Measures: {df_cdc['measure'].unique()[:5] if 'measure' in df_cdc.columns else 'N/A'}")
    
    # Save raw
    df_cdc.to_csv("/app/farmblock_v2/raw/cdc_places_raw.csv", index=False)
    sha = hashlib.sha256(open("/app/farmblock_v2/raw/cdc_places_raw.csv","rb").read()).hexdigest()
    
    # Pivot: one row per tract, columns per measure
    if "tractfips" in df_cdc.columns and "measure" in df_cdc.columns:
        df_cdc["data_value"] = pd.to_numeric(df_cdc["data_value"], errors="coerce")
        
        # Simplify measure names
        measure_map = {
            "Diagnosed diabetes among adults aged >=18 years": "pct_diabetes",
            "High blood pressure among adults aged >=18 years": "pct_high_bp",
            "Obesity among adults aged >=18 years": "pct_obesity",
            "Current smoking among adults aged >=18 years": "pct_smoking",
            "Visits to doctor for routine checkup within the past year among adults aged >=18 years": "pct_annual_checkup",
            "Current asthma among adults aged >=18 years": "pct_asthma",
        }
        df_cdc["measure_short"] = df_cdc["measure"].map(measure_map).fillna(df_cdc["measure"])
        
        df_pivot = df_cdc.pivot_table(
            index="tractfips", 
            columns="measure_short", 
            values="data_value", 
            aggfunc="mean"
        ).reset_index()
        df_pivot.columns.name = None
        df_pivot = df_pivot.rename(columns={"tractfips": "fips_tract"})
        
        # Ensure 11-digit FIPS
        df_pivot["fips_tract"] = df_pivot["fips_tract"].astype(str).str.zfill(11)
        
        # Load main dataset
        df_main = pd.read_csv("/app/farmblock_v2/processed/acs_with_fooddesert.csv", dtype={"fips_tract": str})
        df_main["fips_tract"] = df_main["fips_tract"].astype(str).str.zfill(11)
        
        before = len(df_main)
        df_merged = df_main.merge(df_pivot, on="fips_tract", how="left")
        
        health_cols = [c for c in df_pivot.columns if c != "fips_tract"]
        match_rate  = df_merged[health_cols[0]].notna().sum() / len(df_merged) * 100 if health_cols else 0
        
        print(f"   Pivot: {len(df_pivot):,} tracts × {len(health_cols)} measures")
        print(f"   Join match rate: {match_rate:.1f}%")
        
        df_merged.to_csv("/app/farmblock_v2/processed/acs_cdc_merged.csv", index=False)
        
        manifest = {
            "file": "cdc_places_raw.csv",
            "source": "CDC PLACES 2023 via Socrata API",
            "sha256": sha,
            "rows_raw": len(df_cdc),
            "tracts_pivoted": len(df_pivot),
            "measures": health_cols,
            "match_rate_pct": round(match_rate, 1)
        }
        json.dump(manifest, open("/app/farmblock_v2/raw/cdc_manifest.json","w"), indent=2)
        print(f"✅ CDC PLACES joined — {len(df_merged):,} tracts with health overlay")
    else:
        print("⚠️  Unexpected CDC data format — saving raw only")
        df_main = pd.read_csv("/app/farmblock_v2/processed/acs_with_fooddesert.csv")
        df_main.to_csv("/app/farmblock_v2/processed/acs_cdc_merged.csv", index=False)
else:
    print("⚠️  No CDC data — copying forward without health layer")
    import shutil
    shutil.copy("/app/farmblock_v2/processed/acs_with_fooddesert.csv",
                "/app/farmblock_v2/processed/acs_cdc_merged.csv")
