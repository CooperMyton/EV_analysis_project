import sys
import pandas as pd

''' This file loops through the month by month ev registration .xlsx files.
    It extracts the proper county cheet and saves that as a .csv '''

for i in range(1,13):
    path = f"2024{i if i >= 10 else f"0{i}"}01"
    open_path = f"raw_data/evReg/{path}.xlsx"
    try: 
        df = pd.read_excel(open_path, sheet_name="County")
        print(f"Read county sheet from {path}.xlsx")
    except Exception as e:
        print(f"Error opening county sheet of {path}.xlsx")

    save_path = f"cleaned_data/EvReg/{path}.csv"

    try:
        df.to_csv(save_path, index=False)
        print(f"Isolated CSV saved to: /cleaned_data/EvReg/{path}.csv")
    except Exception as e:
        print(f"Error writing output CSV: {e}")