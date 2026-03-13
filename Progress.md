# Saturday 2/28

## Data Manipulation

From raw_data I manipulated two useful sets of info. Cleaned raw_data/fy2025-district-and-county-statistics.csv to county-statistics-cleanedCols.csv.

I also cleaned raw_data/evReg into files in cleaned_data/EvReg. They are by month,
but I realized the counts are cummulative per month, so december represents total counts. 

Added a new dataset, raw_data/electric_vehicles_spec_2025.csv because it includes a wH/km metric for each model, which represents power consumption per km for a given EV. We could pair this with our per-model counts from the county_statistics and get some sort of average power consumption among the EV's of a given county for calculating a more accurate ratio.

# Wednesday 3/4

## Data Manipulation
Stripped extrenuous columns from raw_data/electric_vehicles_spec_2025.csv.csv and created cleaned_data/vehicle_specs.csv
Realized that the EvReg information contains a grand-total count so I removed my summed versions since they undoubtedly counted that as well, effectively doubling the number.

Normalized headrers of the december ev reg counts for Wh/km averaging. Combined first two columns of vehicle_specs.csv for the same reason. 

# Thursday 3/12

I did it! We now have a datasheet in the root directory, data_with_labels, which contains a set of reliable county data and labeling. I computed the available power/power use metric, and set the decision boundry at the median value. So above the median ratio = over served and under is under served. I chose a relatively small set of county features for prediction, maybe we could add more. But the ones I have are total ev registration numbers (grand total), total kw output across all chargers in the county according to my data (total_kw), a population estimate from my data (pop_estimate), and finally daily driven miles (daily_miles). The labels are under opt_label and cons_label. There are two because I made my ratio calculation two ways. one with an OPTimistic guess at charger utilisation, and one with a CONServative estimate at charger utilisation.