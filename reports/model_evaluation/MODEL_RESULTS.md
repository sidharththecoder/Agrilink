# AgriLink trained model results

All values below are from the saved holdout evaluation JSON files.

## Farmer Intelligence — production regression
- Train rows: 283,425; test rows: 70,857.
- MAE: 337,620.22 tonnes.
- RMSE: 10,438,189.78 tonnes.
- R²: 0.7906.
- Mean baseline MAE: 1,819,276.59 tonnes.

## Mandi Price Intelligence — monthly modal-price regression
- Train rows: 144,000; test rows: 36,000.
- MAE: ₹931.07/quintal.
- RMSE: ₹7,188.69/quintal.
- R²: 0.7438.
- Mean baseline MAE: ₹3,447.95/quintal.
- The model uses a reproducible 180,000-row sample of monthly aggregates, with a chronological split.

## Store Demand Intelligence — units-sold regression
- Train rows: 58,480; test rows: 14,620.
- MAE: 69.42 units.
- RMSE: 88.98 units.
- R²: 0.3243.
- Mean baseline MAE: 88.81 units.
- Performance is moderate; stronger lagged sales features and longer historical coverage are recommended.

## Inventory Intelligence — backorder classification
- Train rows: 12,194; test rows: 3,049.
- Accuracy: 0.9275.
- Precision: 0.6898.
- Recall: 0.7107.
- F1: 0.7001.
- ROC-AUC: 0.9513.
- Majority baseline accuracy: 0.8809.

These are held-out results for this dataset split and configuration. They should not be presented as guaranteed real-world performance.
