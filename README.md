# AgriLink: Agricultural Decision Intelligence Platform

AgriLink is a machine-learning platform for agricultural decisions. It has four modules:

| Module | Predicts | Model |
|---|---|---|
| Farmer Intelligence | Crop production (tonnes) | Random Forest regressor |
| Mandi Price Intelligence | Next-month modal price (₹/quintal) | Random Forest with lag features |
| Store Demand Intelligence | Units sold | Random Forest regressor |
| Inventory Intelligence | Backorder risk (`went_on_backorder`) | Random Forest classifier |

The Integrated Intelligence page combines Farmer + Mandi (indicative gross value) and Store Demand + Inventory (stock gap and backorder risk). Predictions can be saved to MySQL, and each page shows the last saved result.

## Technology stack

- **Python**: main language for the application and pipelines
- **Pandas and NumPy**: cleaning, summaries and numerical work
- **Scikit-learn**: preprocessing pipelines, model training and evaluation
- **Joblib**: saves and loads trained model pipelines
- **Streamlit**: interactive web app and prediction forms
- **MySQL** (optional): stores prediction and model information. Connected with SQLAlchemy and PyMySQL.
- **Matplotlib / Plotly**: charts

## Large files

Git LFS is required to download the two large model files. Install it once, then clone:

```bash
git lfs install
```

## Project structure

```
AgriLink/
├── app/                      Streamlit app
│   ├── Home.py
│   ├── components/ui.py      Theme, cached loaders, prediction memory
│   └── pages/                Farmer, Mandi, Store Demand, Inventory, Integrated, Dashboard
├── config/
│   └── database_config.example.py   Copy to database_config.py and add your password
├── data/
│   ├── raw/                  Original datasets (never overwritten)
│   └── cleaned/              Output of the notebooks, one folder per module
├── database/schema.sql       MySQL schema (run in MySQL Workbench)
├── notebooks/                01–04: EDA and preprocessing per dataset
├── models/                   Trained model pipelines (see note below)
├── reports/                  Metrics (JSON), EDA and SHAP outputs
├── scripts/train_all.py      Trains all four models
├── src/
│   ├── preprocessing/        Cleaning pipeline script
│   ├── models/               Training modules (one per model)
│   ├── prediction/           Streamlit-free prediction functions
│   ├── integration/          Farmer–mandi crop and state mapping
│   ├── database/             MySQL storage (queries, records, connection)
│   └── visualization/        Chart helpers
├── tests/test_storage.py     Storage tests (no MySQL server needed)
└── requirements.txt
```

## Setup

Requires **Python 3.11 or newer**.

```bash
git clone <your-repo-url> AgriLink
cd AgriLink
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Data

| Dataset | Location | Notes |
|---|---|---|
| Crop-wise area, production and yield | `data/raw/farmer/` | In the repository |
| Retail store inventory (store demand) | `data/raw/demand/` | In the repository (synthetic) |
| Inventory backorders | `data/raw/inventory/` | In the repository |
| Daily commodity prices, mandi (2001–2023) | `data/raw/mandi/` | **Not in the repository** (about 6.5 GB). Download: <ADD YOUR DATASET LINK HERE> |
| Cleaned datasets | `data/cleaned/` | In the repository (output of the notebooks) |

Place the 23 yearly mandi CSV files (`2001.csv` to `2023.csv`) in `data/raw/mandi/` only if you want to re-run notebook 02. The app and training use the cleaned files in the repository.

## Models

Trained models are in `models/`. The two large ones (`farmer.joblib`, `demand.joblib`) are stored with Git LFS. After cloning, run `git lfs pull` if they show as small text files.

## MySQL (optional)

1. In MySQL Workbench, run `database/schema.sql`. This creates the `agrilink` database with `prediction_logs` and `model_runs`.
2. Copy the template and add your password:

   ```bash
   cp config/database_config.example.py config/database_config.py
   ```

   Edit `config/database_config.py` and set `MYSQL_PASSWORD` (and `MYSQL_USER` if you don't use `root`).

If the password is still the placeholder, the app runs normally without saving to MySQL.

## Run the app

```bash
streamlit run app/Home.py
```

Use the **Test MySQL connection** button on the Home page to check the database.

## Notebooks and training

Run the notebooks in order (`notebooks/01` to `04`). Each one cleans its dataset and saves the result to `data/cleaned/<module>/`. Then train:

```bash
python -m scripts.train_all
```

## Tests

```bash
python -m unittest tests.test_storage
```

## Important notes

- Predictions are estimates from historical data. They are not guarantees of production, prices, sales or stock.
- Farmer × price gross values are indicative, not profit.
- Store demand predictions are averages across all 100 store–product pairs in the dataset. Users do not choose a store or product.
- Store demand and inventory use different datasets with no verified product key, so they are not joined automatically.
- The retail store dataset is synthetic.
