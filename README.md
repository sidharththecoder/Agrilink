# 🌾 AgriLink — Agricultural Decision Intelligence Platform

**An Integrated Machine Learning Platform for Agricultural Production, Mandi Price Forecasting, Store Demand Prediction, and Inventory Risk Analysis.**

AgriLink is a Machine Learning-based decision-support platform designed to provide predictive insights across different stages of the agricultural and retail supply chain.

The platform consists of four independent Machine Learning modules that analyse historical datasets and generate predictions. It also provides an Integrated Intelligence interface to combine selected outputs where meaningful relationships are available.

The application is developed using Python and Streamlit, with Scikit-learn for Machine Learning and optional MySQL integration for storing prediction information.

---

## 1. Project Overview

Agricultural and retail supply chains involve several interconnected decision-making challenges:

- Farmers need estimates of crop production.
- Agricultural markets experience fluctuations in commodity prices.
- Retail stores need to estimate future product demand.
- Inventory managers need to identify potential backorder risks.

AgriLink addresses these challenges through four dedicated Machine Learning modules.

| Module | Prediction Objective | Model |
|---|---|---|
| Farmer Intelligence | Crop production (tonnes) | Random Forest Regressor |
| Mandi Price Intelligence | Next-month modal price (₹/quintal) | Random Forest with lag features |
| Store Demand Intelligence | Units sold | Random Forest Regressor |
| Inventory Intelligence | Backorder risk (`went_on_backorder`) | Random Forest Classifier |

### Integrated Intelligence

AgriLink also provides an integration layer:

**Farmer–Mandi Intelligence**
- Combines predicted crop production and corresponding mandi prices where matching records are available.
- Calculates an indicative gross value.
- Helps analyse the relationship between agricultural production and market prices.

**Store Demand–Inventory Intelligence**
- Brings demand predictions and inventory backorder-risk predictions into a common decision-support interface.
- Provides insights such as stock gaps and backorder risk where the available information supports them.
- Does not automatically merge the two datasets because they do not have a verified common product identifier.

Predictions can optionally be saved in MySQL, and application pages can display previously saved prediction results.

---

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Pandas | Data cleaning, manipulation and analysis |
| NumPy | Numerical operations |
| Scikit-learn | Preprocessing, model training and evaluation |
| Joblib | Saving and loading trained model pipelines |
| Streamlit | Interactive web application |
| MySQL | Optional prediction and model information storage |
| SQLAlchemy | Database connection and SQL operations |
| PyMySQL | MySQL database driver |
| Matplotlib | Data visualization |
| Plotly | Interactive charts |
| Jupyter Notebook | Exploratory Data Analysis and preprocessing |

---

## 3. Key Features

- Four independent Machine Learning prediction modules.
- Historical agricultural production analysis.
- Monthly mandi price forecasting.
- Store-level product demand prediction.
- Inventory backorder-risk classification.
- Data preprocessing and feature engineering pipelines.
- Leakage prevention during model development.
- Model persistence using Joblib.
- Farmer–Mandi integrated insights.
- Store Demand–Inventory decision-support insights.
- Interactive Streamlit dashboard.
- Optional MySQL prediction persistence.
- Exploratory Data Analysis notebooks.
- Model evaluation and reporting.

---

## 4. Project Architecture

The AgriLink workflow follows these major stages:

```text
                    RAW DATASETS
          Farmer | Mandi | Demand | Inventory
                         |
                         v
             DATA INSPECTION AND
                  PREPROCESSING
                         |
                         v
              FEATURE ENGINEERING
               + LEAKAGE CONTROLS
                         |
                         v
               TRAIN AND EVALUATE
                  FOUR ML MODELS
                         |
                         v
                  INTEGRATION
               /                 \
       Farmer–Mandi          Demand–Inventory
               \                 /
                         |
                         v
               STREAMLIT DASHBOARD
                         |
                         v
                MYSQL PERSISTENCE
                    (Optional)
```

Each module has its own preprocessing and prediction workflow. The integration layer combines selected model outputs where the required information is available.

---

## 5. Project Structure

```text
AgriLink/
│
├── .streamlit/                  Streamlit configuration
├── .venv/                       Local virtual environment (not committed)
│
├── app/                         Streamlit application
│   ├── Home.py
│   ├── components/
│   │   └── ui.py
│   └── pages/
│       ├── Farmer Intelligence
│       ├── Mandi Price Intelligence
│       ├── Store Demand Intelligence
│       ├── Inventory Intelligence
│       ├── Integrated Intelligence
│       └── Dashboard
│
├── config/
│   └── database_config.example.py
│
├── data/
│   ├── raw/
│   │   ├── farmer/
│   │   ├── mandi/
│   │   ├── demand/
│   │   └── inventory/
│   │
│   └── cleaned/
│       ├── farmer/
│       ├── mandi/
│       ├── demand/
│       └── inventory/
│
├── database/
│   └── schema.sql
│
├── models/
│   ├── farmer/
│   ├── mandi/
│   ├── demand/
│   └── inventory/
│
├── notebooks/
│   ├── 01_crop_production_eda.ipynb
│   ├── 02_mandi_prices_eda.ipynb
│   ├── 03_store_demand_eda.ipynb
│   └── 04_inventory_eda.ipynb
│
├── reports/                     Evaluation metrics and reports
│
├── scripts/
│   ├── train_all.py
│   ├── run_mac.sh
│   └── run_windows.bat
│
├── src/
│   ├── database/
│   ├── explainability/
│   ├── integration/
│   ├── models/
│   ├── prediction/
│   ├── preprocessing/
│   └── visualization/
│
├── tests/
│   └── test_storage.py
│
├── .gitignore
├── .gitattributes
├── README.md
└── requirements.txt
```

*Note: This structure describes the intended organization of the project. Refer to the actual repository for the complete list of files.*

---

## 6. Dataset Information

AgriLink uses four datasets for its Machine Learning modules.

| Dataset | Location | Description |
|---|---|---|
| Crop-wise Area, Production and Yield | `data/raw/farmer/` | Historical agricultural production data |
| Mandi Daily Commodity Prices | `data/raw/mandi/` | Historical daily mandi price observations |
| Retail Store Demand | `data/raw/demand/` | Store and product demand records |
| Inventory Backorders | `data/raw/inventory/` | Inventory and backorder information |

### 6.1 Farmer Production Dataset

- Contains historical crop production information.
- Includes crop, state, season, area, production and related attributes.
- Covers agricultural years from 2001–02 to 2022–23.
- Used for crop production prediction.

### 6.2 Mandi Price Dataset

- Contains historical daily commodity price observations.
- Covers the period 2001–2023.
- Includes commodity, state, market, date and price information.
- Daily observations are processed into monthly aggregated data.
- Used for next-month modal price forecasting.

### 6.3 Store Demand Dataset

- Contains 73,100 records.
- Includes 5 stores and 20 products.
- Covers January 2022 to January 2024.
- Used for next-day units-sold prediction.
- The retail store dataset is synthetic.

### 6.4 Inventory Dataset

- Contains 15,243 SKUs.
- Approximately 11.9% of records belong to the positive backorder class.
- Used for inventory backorder-risk classification.
- The prediction target is `went_on_backorder`.

### 6.5 Dataset Availability

The repository includes the raw Farmer, Store Demand and Inventory datasets, along with the cleaned datasets used by the application.

The original daily Mandi dataset is approximately 6.5 GB and is not included in the repository.

To reproduce the complete Mandi preprocessing workflow, obtain the original dataset separately and place the 23 yearly CSV files in:

```text
data/raw/mandi/
```

Expected filenames:

```text
2001.csv
2002.csv
2003.csv
...
2022.csv
2023.csv
```

**Mandi dataset download:** Add the original dataset source link here before publishing the repository.

The cleaned monthly Mandi dataset is included for normal application and prediction workflows, provided the required cleaned file is present.

---

## 7. Installation and Setup

### Requirements

- Python 3.11 or newer (as specified for the project environment).
- Git.
- Git LFS for downloading large model files.
- MySQL Server and MySQL Workbench (optional).

### Step 1: Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

Navigate to the project directory:

```bash
cd AgriLink
```

### Step 2: Create a virtual environment

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 3: Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

---

## 8. Git LFS — Large Model Files

AgriLink uses Git Large File Storage (Git LFS) for large trained model files.

The `farmer.joblib` and `demand.joblib` model files are stored using Git LFS.

### Install Git LFS

**macOS:**

```bash
brew install git-lfs
```

**Windows:**

Install Git LFS from:

https://git-lfs.com/

### Initialize Git LFS

```bash
git lfs install
```

### Download model files

After cloning the repository:

```bash
git lfs pull
```

This downloads the actual model files tracked by Git LFS.

If a model file appears as a small text file instead of a binary Joblib file, check that Git LFS is installed and run `git lfs pull`.

---

## 9. MySQL Database Configuration (Optional)

AgriLink supports optional MySQL integration for storing prediction and model information.

### Step 1: Start MySQL Server

Ensure that your MySQL Server is running.

### Step 2: Open MySQL Workbench

Open the following SQL file:

```text
database/schema.sql
```

Execute the SQL script in MySQL Workbench to create the project database and its configured tables.

### Step 3: Configure database credentials

Copy the example configuration:

```bash
cp config/database_config.example.py config/database_config.py
```

Open:

```text
config/database_config.py
```

Configure the appropriate MySQL credentials:

- MySQL username.
- MySQL password.
- Host.
- Database name.

Use your actual local MySQL credentials.

### Important security note

Do not commit real database passwords, API keys or other credentials to GitHub.

The actual configuration file should remain excluded through `.gitignore`.

If MySQL is not configured, the application can be used without optional database persistence, subject to the application's configured fallback behaviour.

---

## 10. Running the AgriLink Application

After completing installation and configuration, run:

```bash
streamlit run app/Home.py
```

The application should open in your default browser.

Alternatively, open:

```text
http://localhost:8501
```

### Application Modules

The Streamlit application provides the following modules:

**Farmer Intelligence**
- Crop production prediction.
- Historical agricultural data insights.

**Mandi Price Intelligence**
- Monthly modal price forecasting.
- Historical price information.

**Store Demand Intelligence**
- Next-day units-sold prediction.
- Demand-related insights.

**Inventory Intelligence**
- Backorder-risk classification.
- Inventory risk information.

**Integrated Intelligence**
- Farmer–Mandi integrated insights.
- Store Demand–Inventory decision support.

**Overall Dashboard**
- Consolidated application insights.

Use the Test MySQL Connection option on the Home page, if available, to verify database connectivity.

---

## 11. Exploratory Data Analysis and Preprocessing

The project includes four Jupyter notebooks.

| Notebook | Module |
|---|---|
| `01_crop_production_eda.ipynb` | Farmer Intelligence |
| `02_mandi_prices_eda.ipynb` | Mandi Price Intelligence |
| `03_store_demand_eda.ipynb` | Store Demand Intelligence |
| `04_inventory_eda.ipynb` | Inventory Intelligence |

Run the notebooks in the specified order.

Each notebook performs dataset inspection, exploratory analysis and preprocessing for its respective module.

The cleaned datasets are saved under:

```text
data/cleaned/
```

The original raw datasets are treated as read-only inputs and are not overwritten by preprocessing.

---

## 12. Model Training

AgriLink includes separate model training scripts for its four modules.

The training scripts are located under:

```text
src/models/
```

To train all four models using the project training script, run:

```bash
python -m scripts.train_all
```

The training workflow includes:

1. Loading the cleaned datasets.
2. Preparing features and target variables.
3. Applying preprocessing pipelines.
4. Splitting data for training and evaluation.
5. Training the Machine Learning models.
6. Evaluating model performance.
7. Saving trained pipelines using Joblib.

The trained model artifacts are stored in their respective folders under:

```text
models/
```

The Streamlit application uses the saved model pipelines for predictions.

---

## 13. Model Evaluation

AgriLink uses different evaluation metrics according to the Machine Learning task.

### Regression Modules

Used for Farmer Production, Mandi Price and Store Demand.

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)
- R-squared (R²)

### Classification Module

Used for Inventory Backorder Risk.

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC

Baseline comparisons are used to understand whether the trained models improve upon simpler prediction approaches.

The evaluation reports and related outputs are maintained in:

```text
reports/
```

Model performance should be interpreted in the context of the dataset, prediction target and evaluation method.

---

## 14. Running Tests

AgriLink includes tests for database storage functionality.

Run the available storage test using:

```bash
python -m unittest tests.test_storage
```

The storage tests are designed to run without requiring a live MySQL server.

---

## 15. Important Limitations and Assumptions

The following limitations should be considered when interpreting AgriLink predictions.

1. **Prediction uncertainty:** All predictions are estimates based on historical data. They are not guarantees of actual production, market prices, sales or inventory outcomes.

2. **Indicative gross value:** Farmer–Mandi gross value is an indicative calculation and should not be interpreted as actual farmer income, revenue received or profit.

3. **Synthetic demand dataset:** The Store Demand dataset is synthetic and may not represent all real-world retail demand patterns.

4. **Demand prediction scope:** Store demand predictions are averages across all 100 store–product pairs in the dataset. Users do not select an individual store or product.

5. **No verified common product identifier:** Store Demand and Inventory use different datasets without a verified common product ID. Therefore, they are not automatically joined at the individual product-record level.

6. **Mandi data availability:** The original large daily Mandi dataset is not included in the repository. It must be obtained separately to reproduce the complete raw-data preprocessing workflow.

7. **Model generalization:** Model performance may vary when applied to new crops, markets, stores, products or time periods.

8. **Decision support:** AgriLink is intended to support decision-making, not replace expert agricultural, market or inventory judgement.

---

## 16. Future Improvements

Potential future enhancements include:

- Incorporating additional real-world agricultural datasets.
- Expanding crop and regional coverage.
- Improving time-series forecasting approaches.
- Incorporating additional weather and environmental features.
- Improving store-specific demand forecasting.
- Establishing verified product identifiers for demand and inventory integration.
- Adding advanced model explainability.
- Improving model monitoring and retraining workflows.
- Extending the platform for larger-scale deployment.

These are potential improvements and should not be interpreted as already completed features.

---

## 17. Project Information

**Project Name:** AgriLink — Agricultural Decision Intelligence Platform

**Project Type:** Machine Learning Project

**Domain:** Agriculture, Retail Analytics and Decision Intelligence

**Developed By:**

- **Kumar Sidharth** — S25CSEU1959
- **Shikha Singh** — S25CSEU1947

**Department:** Computer Science and Engineering

**University:** Bennett University

**Academic Year:** 2026–2027

---

## Acknowledgement

This project was developed as part of the academic Machine Learning coursework at Bennett University. It demonstrates the application of Machine Learning techniques to agricultural production, commodity price forecasting, retail demand prediction and inventory risk analysis.

---

**AgriLink — Turning Agricultural Data into Actionable Decisions.**