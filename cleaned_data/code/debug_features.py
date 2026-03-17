"""
debug_features.py

Investigates which counties get dropped during feature engineering and why.
"""

import pandas as pd
import numpy as np
from pathlib import Path

ROOT    = Path(__file__).resolve().parent.parent
DATA_IN = ROOT / "data_with_labels"

print("=" * 60)
print("PATH CHECK")
print("=" * 60)
print(f"Project root:  {ROOT}")
print(f"Data in:       {DATA_IN}")
print(f"Data exists:   {DATA_IN.exists()}")


# Load and clean
df = pd.read_csv(DATA_IN)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

def clean_numeric(series):
    return series.astype(str).str.replace(",", "").str.strip().astype(float)

df["pop_estimate"] = clean_numeric(df["pop_estimate"])
df["daily_miles"]  = clean_numeric(df["daily_miles"])
df["grand_total"]  = clean_numeric(df["grand_total"])
df["total_kw"]     = clean_numeric(df["total_kw"])

print(f"\nTotal counties loaded: {len(df)}")


# Check for zeros
print("\n" + "=" * 60)
print("ZERO VALUE COUNTS (before ratio calc)")
print("=" * 60)
for col in ["grand_total", "total_kw", "pop_estimate", "daily_miles"]:
    zeros = (df[col] == 0).sum()
    nulls = df[col].isna().sum()
    print(f"  {col:<20} zeros={zeros}  nulls={nulls}")


# Compute ratios
df["kw_per_ev"]     = df["total_kw"]    / df["grand_total"].replace(0, np.nan)
df["ev_per_capita"] = df["grand_total"] / df["pop_estimate"].replace(0, np.nan)
df["kw_per_capita"] = df["total_kw"]    / df["pop_estimate"].replace(0, np.nan)
df["miles_per_ev"]  = df["daily_miles"] / df["grand_total"].replace(0, np.nan)
df["miles_per_kw"]  = df["daily_miles"] / df["total_kw"].replace(0, np.nan)

RATIO_COLS = ["kw_per_ev", "ev_per_capita", "kw_per_capita", "miles_per_ev", "miles_per_kw"]


# Find dropped counties
dropped_mask = df[RATIO_COLS].isna().any(axis=1)
dropped      = df[dropped_mask].copy()
kept         = df[~dropped_mask].copy()

print(f"\n" + "=" * 60)
print(f"DROPPED COUNTIES: {len(dropped)} of {len(df)}")
print("=" * 60)

# For each dropped county, show which column caused it
def drop_reason(row):
    reasons = []
    if row["grand_total"] == 0 or pd.isna(row["grand_total"]):
        reasons.append("grand_total=0 or null")
    if row["total_kw"] == 0 or pd.isna(row["total_kw"]):
        reasons.append("total_kw=0 or null")
    if row["pop_estimate"] == 0 or pd.isna(row["pop_estimate"]):
        reasons.append("pop_estimate=0 or null")
    if row["daily_miles"] == 0 or pd.isna(row["daily_miles"]):
        reasons.append("daily_miles=0 or null")
    return ", ".join(reasons) if reasons else "unknown"

dropped["drop_reason"] = dropped.apply(drop_reason, axis=1)

print(dropped[["county", "grand_total", "total_kw", "pop_estimate",
            "daily_miles", "drop_reason"]].to_string(index=False))


# Breakdown by reason
print("\n" + "=" * 60)
print("DROP REASON BREAKDOWN")
print("=" * 60)
print(dropped["drop_reason"].value_counts().to_string())


# Are dropped counties salvageable?
# A county with total_kw=0 but valid EV registrations is genuinely underserved
# and could be labeled directly rather than dropped
zero_kw = dropped[dropped["total_kw"] == 0]
print(f"\nCounties dropped purely because total_kw=0: {len(zero_kw)}")
print("These counties have EV registrations but no recorded charger power.")
print("They are likely genuinely underserved and could be relabeled directly.")
if len(zero_kw) > 0:
    print(zero_kw[["county", "grand_total", "total_kw", "cons_label"]].to_string(index=False))

print(f"\nKept counties: {len(kept)}")
print("\nDone.")