''' Using this file to print the combined brand-model name from vehicle_specs.csv for comparison to registration data.'''
import sys
import pandas as pd

try:
    df = pd.read_csv("./cleaned_data/vehicle_specs.csv")
except Exception as e:
    print(f"Error reading input CSV: {e}")
    sys.exit(1)

combined = df.iloc[:, 0].astype(str) + " " + df.iloc[:, 1].astype(str)

for value in combined:
    print(value)