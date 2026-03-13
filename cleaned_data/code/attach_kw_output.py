import pandas as pd

df = pd.read_csv('./cleaned_data/charging_station.csv')
of = pd.read_csv('./cleaned_data/working_sheet.csv')
zf = pd.read_csv('./raw_data/uszips.csv')

z2c = zf.set_index('zip')['county_name'].to_dict()

df['county'] = df['ZIP'].map(z2c)

county_totals = df.groupby('county')['row_kw'].sum().reset_index()
county_totals.rename(columns={'row_kw': 'total_kw'}, inplace=True)

of = of.merge(county_totals, on='county', how='left')

of.to_csv('./cleaned_data/working_sheet.csv', index=False)