import pandas as pd

working = pd.read_csv('./cleaned_data/working_ratios.csv')
fart = pd.read_csv('./cleaned_data/working_sheet.csv')

print(working[['opt_ratio','cons_ratio']].describe())
print(working['cons_ratio'].median())