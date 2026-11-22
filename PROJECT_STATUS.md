# AgriLink — final delivery status

## Completed and generated

- [x] Inspected the four supplied datasets and all 23 mandi yearly files (2001–2023).
- [x] Created the agreed AgriLink folder structure.
- [x] Cleaned Farmer, Mandi, Store Demand and Inventory data.
- [x] Saved cleaned datasets under `data/cleaned/`.
- [x] Processed 64,026,496 valid daily mandi price observations into 427,242 monthly state–commodity aggregates.
- [x] Created Farmer–Mandi agricultural-year integration output with explicit crop/state aliases: 240,581 matched rows (67.05% of eligible non-Total farmer rows).
- [x] Trained and saved all four model pipelines: Farmer, Mandi, Store Demand and Inventory.
- [x] Saved holdout metrics and model scorecard.
- [x] Generated EDA summaries and charts for all four modules.
- [x] Generated SHAP summary plots and feature contribution CSVs for all four modules.
- [x] Built the AgriLink Streamlit multipage UI with model prediction forms and integrated Farmer–Mandi value estimation.
- [x] Added MySQL schema, SQLAlchemy helper, optional prediction logging and connection test.
- [x] Python syntax compilation passed; model artifact inference smoke tests passed.

## Model holdout metrics

- Farmer: MAE 337,620.22 tonnes; RMSE 10,438,189.78 tonnes; R² 0.7906.
- Mandi: MAE ₹931.07/quintal; RMSE ₹7,188.69/quintal; R² 0.7438.
- Store Demand: MAE 69.42 units; RMSE 88.98 units; R² 0.3243.
- Inventory: accuracy 0.9275; precision 0.6898; recall 0.7107; F1 0.7001; ROC-AUC 0.9513.

Full results are in `reports/model_evaluation/MODEL_RESULTS.md` and JSON files.

## Honest environment notes

- The Streamlit app source is complete and syntax-checked. Streamlit itself was not installed in this build environment, and package installation was blocked by unavailable network access. Install the included requirements locally, then run `streamlit run app/Home.py`.
- MySQL schema and application integration are included. A live database connection cannot be verified without the user's MySQL server and credentials; prediction logging activates after `.env` is configured.
- The 5.4 GB raw mandi source files are supplied in five companion ZIP archives. Extract each into the project root so its `AgriLink/data/raw/mandi/` paths merge into the same folder.
- Demand model performance is moderate; see model validation notes. No performance guarantee is implied.
