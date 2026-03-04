# Saturday 2/28

## Data Manipulation

From raw_data I manipulated two useful sets of info. Cleaned raw_data/fy2025-district-and-county-statistics.csv to county-statistics-cleanedCols.csv.

I also cleaned raw_data/evReg into files in cleaned_data/EvReg. They are by month,
but I realized the counts are cummulative per month, so december represents total counts. 



Added a new dataset, raw_data/electric_vehicles_spec_2025.csv because it includes a wH/km metric for each model, which represents power consumption per km for a given EV. We could pair this with our per-model counts from the county_statistics and get some sort of average power consumption among the EV's of a given county for calculating a more accurate ratio.