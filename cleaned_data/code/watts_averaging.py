import pandas as pd
import numpy as np

reg_df = pd.read_csv("./cleaned_data/reg_year_total.csv")
spec_df = pd.read_csv("./cleaned_data/vehicle_specs.csv")
out_df = reg_df[['county', 'grand total']]

mean_wh = spec_df['efficiency_wh_per_km'].mean()

results = np.zeros(reg_df.shape[0])


def findWh(model_name):

    words = model_name.split() # split model name for fuzzy match search

    while words:
        search = " ".join(words) # join remaining words

        matches = spec_df[spec_df['model'].str.contains(search, regex = False)] #extract rows with model name

        if not matches.empty:
            # if matches are found, average across and return
            return matches['efficiency_wh_per_km'].mean()

        words.pop() # if no matches found, remove a word for more generalized search

    # If there's no matches, return the global average
    return mean_wh

for i, row in reg_df.iterrows():

    total_reg = row['grand total']

    for vehicle in reg_df.columns[1:-1]:
        count = row[vehicle]
        if pd.isna(count):
            continue
        else:
            out = findWh(vehicle)
            results[i] += ((out * count)/total_reg)

out_df['avg_Wh'] = results;

out_df.to_csv('./cleaned_data/working_sheet.csv', index=False)
