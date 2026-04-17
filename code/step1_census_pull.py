"""
FarmBlock Distress Index v2.0 — Step 1: Census ACS Pull
========================================================
Source:  US Census Bureau ACS 5-Year Estimates (2023)
API:     api.census.gov/data/2023/acs/acs5
License: CC0 1.0 Universal
Author:  Atlas / E5 Enclave Incorporated
Date:    2026-04-17

Variables pulled per census tract:
  B17001_002E  = persons below poverty level
  B17001_001E  = total persons (poverty universe)
  B19013_001E  = median household income
  B02001_003E  = Black/AA population alone
  B02001_001E  = total population
  B28002_013E  = no internet access (households)
  B28002_001E  = total households (internet universe)
  B25002_003E  = vacant housing units
  B25002_001E  = total housing units

Derived:
  poverty_rate     = B17001_002E / B17001_001E * 100
  pct_black        = B02001_003E / B02001_001E * 100
  pct_no_internet  = B28002_013E / B28002_001E * 100
  vacancy_rate     = B25002_003E / B25002_001E * 100
"""

import requests, json, hashlib, os, time
import pandas as pd
from datetime import datetime

API_KEY = os.environ.get("CENSUS_API_KEY", "")
BASE    = "https://api.census.gov/data/2023/acs/acs5"
VARS    = "B17001_002E,B17001_001E,B19013_001E,B02001_003E,B02001_001E,B28002_013E,B28002_001E,B25002_003E,B25002_001E"

# Our 50 target cities — (state_fips, county_fips, city_name, state_abbr)
# Using county-level pulls then filtering — more reliable than place-level
TARGETS = [
    ("28","049","Jackson","MS"),
    ("26","163","Detroit","MI"),
    ("01","073","Birmingham","AL"),
    ("47","157","Memphis","TN"),
    ("13","095","Albany","GA"),
    ("18","089","Gary","IN"),
    ("26","049","Flint","MI"),
    ("24","510","Baltimore","MD"),
    ("22","071","New Orleans","LA"),
    ("22","033","Baton Rouge","LA"),
    ("22","017","Shreveport","LA"),
    ("01","101","Montgomery","AL"),
    ("13","051","Savannah","GA"),
    ("13","245","Augusta","GA"),
    ("13","021","Macon","GA"),
    ("13","215","Columbus","GA"),
    ("01","125","Tuscaloosa","AL"),
    ("01","101","Selma","AL"),  # Dallas County
    ("34","007","Camden","NJ"),
    ("42","045","Chester","PA"),
    ("17","163","East St. Louis","IL"),
    ("12","011","Jacksonville","FL"),  # Duval
    ("12","031","Miami","FL"),         # Miami-Dade (Liberty City)
    ("12","057","Lakeland","FL"),
    ("45","079","Columbia","SC"),
    ("37","119","Charlotte","NC"),
    ("37","081","Greensboro","NC"),
    ("37","067","Durham","NC"),
    ("51","760","Richmond","VA"),
    ("51","800","Suffolk","VA"),
    ("54","039","Kanawha","WV"),       # Charleston WV
    ("40","143","Tulsa","OK"),
    ("40","109","Oklahoma City","OK"),
    ("48","201","Houston","TX"),
    ("48","453","Dallas","TX"),
    ("48","141","El Paso","TX"),
    ("48","029","San Antonio","TX"),
    ("06","037","Los Angeles","CA"),
    ("06","001","Oakland","CA"),
    ("06","073","San Diego","CA"),
    ("53","033","Seattle","WA"),
    ("17","031","Chicago","IL"),
    ("36","005","Bronx","NY"),
    ("36","047","Brooklyn","NY"),
    ("39","035","Cleveland","OH"),
    ("39","061","Cincinnati","OH"),
    ("39","113","Columbus","OH"),
    ("21","111","Louisville","KY"),
    ("29","510","St. Louis","MO"),
    ("04","013","Phoenix","AZ"),
]

results = []
errors  = []

print(f"[{datetime.now().strftime('%H:%M:%S')}] Starting Census ACS pull — {len(TARGETS)} counties")
print(f"API key loaded: {API_KEY[:8]}...")

for i, (state, county, city, abbr) in enumerate(TARGETS):
    url = (f"{BASE}?get=NAME,{VARS}"
           f"&for=tract:*&in=state:{state}%20county:{county}"
           f"&key={API_KEY}")
    try:
        r = requests.get(url, timeout=30)
        if r.status_code == 200:
            data = r.json()
            cols = data[0]
            rows = data[1:]
            df   = pd.DataFrame(rows, columns=cols)
            df["city"]        = city
            df["state_abbr"]  = abbr
            df["source"]      = "Census ACS 5-Year 2023"
            df["pull_date"]   = "2026-04-17"
            results.append(df)
            print(f"  ✅ {city}, {abbr} — {len(rows)} tracts")
        else:
            errors.append({"city": city, "status": r.status_code, "text": r.text[:200]})
            print(f"  ❌ {city}, {abbr} — HTTP {r.status_code}")
    except Exception as e:
        errors.append({"city": city, "error": str(e)})
        print(f"  ❌ {city}, {abbr} — {e}")
    time.sleep(0.15)  # polite rate limiting

if results:
    combined = pd.concat(results, ignore_index=True)
    out_path  = "/app/farmblock_v2/raw/census_acs_tracts_raw.csv"
    combined.to_csv(out_path, index=False)
    
    # SHA-256 hash
    sha = hashlib.sha256(open(out_path,"rb").read()).hexdigest()
    
    manifest = {
        "file":        "census_acs_tracts_raw.csv",
        "source":      "US Census Bureau ACS 5-Year Estimates 2023",
        "api":         "api.census.gov/data/2023/acs/acs5",
        "pull_date":   "2026-04-17",
        "rows":        len(combined),
        "cities":      len(results),
        "errors":      len(errors),
        "sha256":      sha,
        "variables":   VARS.split(","),
    }
    json.dump(manifest, open("/app/farmblock_v2/raw/census_manifest.json","w"), indent=2)
    json.dump(errors,   open("/app/farmblock_v2/validation/census_errors.json","w"), indent=2)
    
    print(f"\n✅ INGEST COMPLETE")
    print(f"   Rows:    {len(combined):,}")
    print(f"   Cities:  {len(results)}/{len(TARGETS)}")
    print(f"   Errors:  {len(errors)}")
    print(f"   SHA-256: {sha[:32]}...")
else:
    print("❌ No data retrieved — check API key and connectivity")

