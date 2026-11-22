# AgriLink — Exploratory Data Analysis Report

## Farmer Intelligence
- 402,102 rows after filtering agricultural years 2001–02 through 2022–23.
- 16 source columns; 34 states, 735 district names and 114 crop names.
- 358,800 rows remain after excluding `Total` season rows for modelling/integration to avoid double-counting seasonal subtotals.
- Production, area and yield are numeric; missing values are preserved for audit and handled by the model pipeline where appropriate.

## Mandi Price Intelligence
- 23 source files (2001–2023), each with 11 common columns.
- 64,026,496 valid positive modal-price observations represented after parsing dates and filtering invalid dates/non-positive modal prices.
- 427,242 state–commodity–calendar-month aggregates were generated.
- Monthly price means are weighted by the number of daily observations when aggregating to agricultural years.
- Raw daily files remain unchanged under `data/raw/mandi/`.

## Store Demand Intelligence
- 73,100 observations from 2022-01-01 through 2024-01-01.
- Five stores and twenty products.
- Mean `Units Sold` is approximately 136.46.
- `Units Sold` is the supervised target. `Demand Forecast` is excluded from model inputs to reduce risk of leakage from an existing forecast field.

## Inventory Intelligence
- 15,243 SKU observations.
- Target `went_on_backorder`: 13,430 negatives and 1,813 positives (11.89% positive class).
- `Validation` and `sku` are excluded from model features.
- Class imbalance is handled using `class_weight="balanced"`.

See `eda_summary.json` and the PNG charts in this folder for generated summaries and plots.
