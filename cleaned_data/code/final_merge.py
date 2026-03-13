import pandas as pd
import numpy as np

stats = pd.read_csv('./cleaned_data/county-statistics-cleanedCols.csv')
labeled = pd.read_csv('./cleaned_data/labeled.csv')

newData = labeled[['county','grand total','total_kw']]

county_pop = dict(zip(stats['county'], stats["Population Estimate**"]))
county_miles = dict(zip(stats['county'], stats["Daily Vehicle Miles*"]))

newData['pop_estimate'] = newData['county'].map(county_pop)
newData['daily_miles'] = newData['county'].map(county_miles)
newData['opt_label'] = labeled['opt_label']
newData['cons_label'] = labeled['cons_label']
newData.dropna(inplace=True)

newData.to_csv('./data_with_labels', index=False)