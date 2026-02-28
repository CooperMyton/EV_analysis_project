import sys
import pandas as pd

for i in range(1,13):

    input_path = f"cleaned_data/EvReg/2024{i if i >= 10 else f"0{i}"}01.csv"
    output_path = f"cleaned_data/EvReg/2024{i if i >= 10 else f"0{i}"}01_collapsed.csv"

    df = pd.read_csv(input_path)

    # Assume first column is County
    county_col = df.columns[0]

    # Sum all other columns row-wise
    df["Total_Registrations"] = df.iloc[:, 1:].sum(axis=1)

    # Keep only county and total
    result = df[[county_col, "Total_Registrations"]]

    result.to_csv(output_path, index=False)



