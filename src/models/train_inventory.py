"""Train the Inventory Intelligence model: classifies backorder risk (went_on_backorder)."""
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (accuracy_score, precision_recall_fscore_support, roc_auc_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.models.common import CLEAN, save_bundle, save_json


def train_inventory():
    df = pd.read_csv(CLEAN / "inventory" / "inventory_cleaned.csv")
    y = df["went_on_backorder"].astype(int)
    # sku is an identifier and the target must never be a feature.
    X = df.drop(columns=["went_on_backorder", "sku"], errors="ignore")
    cat = [c for c in X if X[c].dtype == "object"]
    num = [c for c in X if c not in cat]

    prep = ColumnTransformer([
        ("num", Pipeline([("imp", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), num),
        ("cat", Pipeline([("imp", SimpleImputer(strategy="most_frequent")),
                          ("oh", OneHotEncoder(handle_unknown="ignore"))]), cat),
    ])
    # Stratified split preserves the backorder rate in train and test. Splitting happens
    # before any class weighting, so the test set is untouched.
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=.2, random_state=42, stratify=y)
    model = Pipeline([("prep", prep), ("rf", RandomForestClassifier(
        n_estimators=100, class_weight="balanced", min_samples_leaf=2, max_depth=24,
        n_jobs=-1, random_state=42))])
    baseline = DummyClassifier(strategy="most_frequent").fit(X_tr, y_tr)
    model.fit(X_tr, y_tr)
    pred = model.predict(X_te)
    proba = model.predict_proba(X_te)[:, 1]
    precision, recall, f1, _ = precision_recall_fscore_support(y_te, pred, average="binary", zero_division=0)

    metrics = {
        "model": "inventory", "rows_train": len(X_tr), "rows_test": len(X_te),
        "accuracy": accuracy_score(y_te, pred), "precision": precision,
        "recall": recall, "f1": f1, "roc_auc": roc_auc_score(y_te, proba),
        "baseline_accuracy": accuracy_score(y_te, baseline.predict(X_te)),
    }
    save_bundle("inventory", {"pipeline": model, "features": list(X.columns),
                              "target": "went_on_backorder"})
    save_json("inventory_metrics.json", metrics)
    return metrics


if __name__ == "__main__":
    print(train_inventory())
