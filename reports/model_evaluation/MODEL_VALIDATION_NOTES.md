# Model validation methodology

| Module | Target | Validation | Baseline / imbalance handling |
|---|---|---|---|
| Farmer | `production` (tonnes) | Chronological split by agricultural start year | Mean DummyRegressor baseline |
| Mandi | Monthly `Modal_Price` | Chronological split by calendar year after a reproducible 180k-row sample | Mean DummyRegressor baseline; lagged-price features |
| Store Demand | `Units Sold` | Chronological split by Date | Mean DummyRegressor baseline |
| Inventory | `went_on_backorder` | Stratified holdout split | Majority DummyClassifier baseline; class-weighted Random Forest |

Model scores are holdout estimates, not guarantees. Demand data covers only two years and its Random Forest performance should be interpreted cautiously. The farmer target has a strongly skewed distribution, so RMSE is sensitive to very large production records. The inventory F1/recall and ROC-AUC are more informative than accuracy alone under class imbalance.
