# Saturday 2/28

## Data Manipulation
From raw_data I manipulated two useful sets of info. Cleaned raw_data/fy2025-district-and-county-statistics.csv to cleaned_data/county-statistics-cleandCols.csv. I removed a number of useful data headers regarding road length and upkeep stats and kept things regarding commute distance / frequency.

I also took the month by month registration data in raw_data/evReg, isolated the desired 'county' datasheet, and then created a summed version for each month. For some reason they include registration numbers for each make and model, so I condensed it into a single total for each county.

I have also realized that the month-by-month totals are cummulative, so the December sheet offers the year total.

In raw data theres a sheet: electric_vehicles_spec_2025.csv that has info on EV models available in 2025. I think this could be useful because it includes a wH/km metric for each model, which represents power consumption per km for a given EV. We could pair this with our per-model counts and we could get some sort of average power consumption among the EV's of a given county or something similar.