import sys
import pandas as pd
import glob
import os

def main():
    if len(sys.argv) != 3:
        print("Usage: python yearly_county_totals.py <input_folder> <output_csv>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_path = sys.argv[2]

    # Get all CSV files in folder
    files = glob.glob(os.path.join(input_folder, "*.csv"))

    if not files:
        print("No CSV files found in folder.")
        sys.exit(1)

    all_data = []

    for file in files:
        df = pd.read_csv(file)

        # Standardize column names just in case
        df.columns = df.columns.str.strip()

        # Ensure expected columns exist
        if len(df.columns) < 2:
            print(f"Skipping malformed file: {file}")
            continue

        county_col = df.columns[0]
        total_col = df.columns[1]

        # Force numeric just in case
        df[total_col] = pd.to_numeric(df[total_col], errors="coerce")

        all_data.append(df[[county_col, total_col]])

    # Combine all months
    combined = pd.concat(all_data, ignore_index=True)

    # Group by county and sum
    yearly = combined.groupby(county_col, as_index=False)[total_col].sum()

    yearly = yearly.rename(columns={total_col: "Year_Total_Registrations"})

    yearly.to_csv(output_path, index=False)

    print("\nYearly totals created successfully.")
    print(yearly.head())

if __name__ == "__main__":
    main()