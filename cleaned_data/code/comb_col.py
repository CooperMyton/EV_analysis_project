import pandas as pd


"""
Concatenating the first two cols of vehicle specs to combine brand and model. 
Normalizing to help with model matching from reg_year_total.csv.
"""
df = pd.read_csv("./cleaned_data/vehicle_specs.csv")

# Create new combined column
combined = df.iloc[:, 0].astype(str) + " " + df.iloc[:, 1].astype(str)

# Drop the original first two columns
df = df.drop(df.columns[[0, 1]], axis=1)

# Insert the combined column at position 0
df.insert(0, "model", combined)

df["model"] = df["model"].str.strip()
df["model"] = df["model"].str.lower()

# Save to new CSV
df.to_csv("./cleaned_data/vehicle_specs.csv", index=False)