import pandas as pd
import numpy as np
county_stats = pd.read_csv('./cleaned_data/county-statistics-cleanedCols.csv')
working = pd.read_csv('./cleaned_data/working_sheet.csv')
working['total_kw'] = working['total_kw'].fillna(0)

county_stats['Per Capita Daily Vehicle Miles*'] = pd.to_numeric(
    county_stats['Per Capita Daily Vehicle Miles*'],
    errors='coerce'
)

county_stats["daily_km_per_capita"] = (
    county_stats['Per Capita Daily Vehicle Miles*'] * 1.60934
)

county_km = dict(zip(county_stats['county'], county_stats["daily_km_per_capita"]))
working["daily_km_per_capita"] = working["county"].map(county_km)

working["kWh_use_per_day"] = (
    working["daily_km_per_capita"]
    * working["grand total"]
    * working["avg_Wh"]
) / 1000

working["opt_kWh_charge_per_day"] = working['total_kw'] * 24 * 0.5
working["cons_kWh_charge_per_day"] = working['total_kw'] * 24 * 0.3

working['opt_ratio'] = working['opt_kWh_charge_per_day'] / working["kWh_use_per_day"]
working['cons_ratio'] = working['cons_kWh_charge_per_day'] / working["kWh_use_per_day"]

working['opt_ratio'] = working['opt_ratio'].fillna(0)
working['cons_ratio'] = working['cons_ratio'].fillna(0)

working.to_csv('./cleaned_data/working_ratios.csv', index=False)