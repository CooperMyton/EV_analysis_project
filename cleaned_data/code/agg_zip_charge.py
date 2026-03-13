import pandas as pd

df = pd.read_csv('./cleaned_data/charging_station.csv')

df.fillna(0, inplace=True)

df['row_kw'] = (
    df['EV J1772 Connector Count'] * df['EV J1772 Power Output (kW)'] +
    df['EV CCS Connector Count'] * df['EV CCS Power Output (kW)'] + 
    df['EV CHAdeMO Connector Count'] * df['EV CHAdeMO Power Output (kW)'] + 
    df['EV J3400 Connector Count'] * df['EV J3400 Power Output (kW)'] + 
    df['EV J3271 Connector Count'] * df['EV J3271 Power Output (kW)']
)

zip_totals = df.groupby('ZIP')['row_kw'].sum().reset_index()

zip_totals.to_csv('./cleaned_data/charging_station.csv', index=False)