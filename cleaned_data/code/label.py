import pandas as pd
import numpy as np

df = pd.read_csv("./cleaned_data/working_ratios.csv")

opt_med = df['opt_ratio'].median()
cons_med = df['cons_ratio'].median()

df['opt_label'] = np.where(df['opt_ratio'] > opt_med, 'over', 'under')
df['cons_label'] = np.where(df['cons_ratio'] > cons_med, 'over', 'under')

df.to_csv('./cleaned_data/labeled.csv')