"""Shared helpers for AgriLink training modules: paths, saving, and regression training."""
from __future__ import annotations

import json
from pathlib import Path

import joblib
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.dummy import DummyRegressor

ROOT = Path(__file__).resolve().parents[2]
CLEAN = ROOT / "data" / "cleaned"
MODELS = ROOT / "models"
REPORTS = ROOT / "reports" / "model_evaluation"
REPORTS.mkdir(parents=True, exist_ok=True)


def save_json(name: str, obj) -> None:
    (REPORTS / name).write_text(json.dumps(obj, indent=2, default=float), encoding="utf-8")


def save_bundle(name: str, bundle: dict) -> Path:
    path = MODELS / name / f"{name}.joblib"
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(bundle, path)
    return path


def train_regression(df, target, features, name, time_col=None, categorical=None,
                     trees=80, depth=24):
    """Train a Random Forest regressor with a chronological split when time_col is given.

    Imputers and one-hot encoders are fitted inside the pipeline on training rows only,
    so no test information leaks into preprocessing.
    """
    cols = list(dict.fromkeys(features + [target] + ([time_col] if time_col else [])))
    data = df[cols].dropna(subset=[target]).copy()
    if time_col:
        data = data.sort_values(time_col)
        split = int(len(data) * .8)
        train, test = data.iloc[:split], data.iloc[split:]
    else:
        train, test = train_test_split(data, test_size=.2, random_state=42)

    X_tr, y_tr = train[features], train[target]
    X_te, y_te = test[features], test[target]
    categorical = categorical or [c for c in features if X_tr[c].dtype == "object"]
    numeric = [c for c in features if c not in categorical]

    prep = ColumnTransformer([
        ("num", SimpleImputer(strategy="median"), numeric),
        ("cat", Pipeline([("imputer", SimpleImputer(strategy="most_frequent")),
                          ("onehot", OneHotEncoder(handle_unknown="ignore", min_frequency=2))]), categorical),
    ])
    model = Pipeline([("prep", prep), ("rf", RandomForestRegressor(
        n_estimators=trees, min_samples_leaf=2, max_depth=depth, n_jobs=-1, random_state=42))])
    baseline = DummyRegressor(strategy="mean").fit(X_tr, y_tr)
    model.fit(X_tr, y_tr)
    pred = model.predict(X_te)

    metrics = {
        "model": name, "rows_train": len(train), "rows_test": len(test),
        "MAE": mean_absolute_error(y_te, pred),
        "RMSE": mean_squared_error(y_te, pred) ** .5,
        "R2": r2_score(y_te, pred),
        "baseline_MAE": mean_absolute_error(y_te, baseline.predict(X_te)),
    }
    save_bundle(name, {"pipeline": model, "features": features, "target": target})
    save_json(f"{name}_metrics.json", metrics)
    return metrics
