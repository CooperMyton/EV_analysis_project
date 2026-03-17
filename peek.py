import pandas as pd
import os

files = {
    "data_with_labels": "data_with_labels",
    "county_stats": "cleaned_data/county-statistics-cleanedCols.csv",
    "ev_reg_dec": "cleaned_data/EvReg/20241201.csv",
    "reg_year_total": "cleaned_data/reg_year_total.csv",
}

for name, path in files.items():
    print(f"\n{'='*50}")
    print(f"FILE: {name}")
    print(f"{'='*50}")
    try:
        df = pd.read_csv(path)
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print(df.head(3).to_string())
    except Exception as e:
        print(f"Error: {e}")

# Also print Progress.md
print("\n" + "="*50 + "\nProgress.md\n" + "="*50)
with open("Progress.md") as f:
    print(f.read())