"""Prediction helpers for AgriLink.

These functions contain no Streamlit code, so they can be tested from a plain
Python session. Each function takes an already-loaded model bundle, i.e. the
dict saved by src/models/*.py with keys "pipeline" and "features".
"""
from __future__ import annotations

import numpy as np
import pandas as pd

QUINTALS_PER_TONNE = 10  # 1 tonne = 10 quintals


def predict_farmer_production(model_bundle: dict, *, year_start: int, state_name: str,
                            district_name: str, crop_name: str, season: str,
                            area: float) -> float:
    """Predicted production in tonnes for one state/district/crop/season/year/area."""
    X = pd.DataFrame([{
        "year_start": int(year_start), "state_name": state_name,
        "district_name": district_name, "crop_name": crop_name,
        "season": season, "area": float(area),
    }])
    return float(model_bundle["pipeline"].predict(X)[0])


def forecast_next_mandi_price(model_bundle: dict, history: pd.DataFrame,
                              state: str, commodity: str) -> dict | None:
    """Forecast the modal price (Rs/quintal) for the month after the latest observed month.

    `history` is the cleaned monthly mandi table (State, Commodity, year, month, Modal_Price).
    Returns None when the state/commodity pair has no history.
    """
    hist = history[(history["State"] == state) & (history["Commodity"] == commodity)]
    hist = hist.sort_values(["year", "month"])
    if hist.empty:
        return None
    latest = hist.iloc[-1]
    last_month, last_year = int(latest["month"]), int(latest["year"])
    next_month = last_month % 12 + 1
    next_year = last_year + (1 if last_month == 12 else 0)
    X = pd.DataFrame([{
        "State": state, "Commodity": commodity,
        "year": next_year, "month": next_month,
        "lag_1": float(latest["Modal_Price"]),
        "lag_3_mean": float(hist.tail(3)["Modal_Price"].mean()),
    }])
    price = float(model_bundle["pipeline"].predict(X)[0])
    return {"price": price, "year": next_year, "month": next_month}


def indicative_gross_value(production_tonnes: float, price_per_quintal: float) -> float:
    """Indicative gross value in Rs = tonnes x 10 quintals/tonne x Rs/quintal.

    This is a gross estimate, not farmer income or profit.
    """
    return max(0.0, production_tonnes) * QUINTALS_PER_TONNE * max(0.0, price_per_quintal)


def predict_store_demand(model_bundle: dict, record: dict) -> float:
    """Predicted units sold. `record` must contain the raw demand inputs, including 'date'."""
    dt = pd.Timestamp(record["date"])
    row = {
        "year": dt.year, "month": dt.month, "dayofweek": dt.dayofweek,
        "Store ID": record["store"], "Product ID": record["product"],
        "Category": record["category"], "Region": record["region"],
        "Inventory Level": record["stock"], "Units Ordered": record["ordered"],
        "Price": record["price"], "Discount": record["discount"],
        "Competitor Pricing": record["competitor"],
        "Holiday/Promotion": record["holiday"], "Weather Condition": record["weather"],
        "Seasonality": record["season"],
    }
    X = pd.DataFrame([row], columns=model_bundle["features"])
    return max(0.0, float(model_bundle["pipeline"].predict(X)[0]))


def store_product_pairs(demand_df: pd.DataFrame) -> pd.DataFrame:
    """One row per Store ID x Product ID pair, with the Category and Region used by the model."""
    return demand_df[["Store ID", "Product ID", "Category", "Region"]].drop_duplicates(["Store ID", "Product ID"]).reset_index(drop=True)


def predict_demand_any_store_product(model_bundle: dict, base: dict, pairs: pd.DataFrame):
    """Average predicted units sold across every store-product pair.

    `base` holds the date and the store-wide inputs (stock, ordered, price, discount,
    competitor, holiday, weather, season). Returns (average units, number of pairs averaged).
    """
    dt = pd.Timestamp(base["date"])
    X = pd.DataFrame({
        "year": dt.year, "month": dt.month, "dayofweek": dt.dayofweek,
        "Store ID": pairs["Store ID"].values, "Product ID": pairs["Product ID"].values,
        "Category": pairs["Category"].values, "Region": pairs["Region"].values,
        "Inventory Level": base["stock"], "Units Ordered": base["ordered"],
        "Price": base["price"], "Discount": base["discount"],
        "Competitor Pricing": base["competitor"],
        "Holiday/Promotion": base["holiday"], "Weather Condition": base["weather"],
        "Seasonality": base["season"],
    })[model_bundle["features"]]
    preds = np.maximum(0.0, model_bundle["pipeline"].predict(X))
    return float(preds.mean()), int(len(preds))


def predict_backorder_probability(model_bundle: dict, values: dict) -> float:
    """Probability that an item goes on backorder, from the inventory classifier."""
    X = pd.DataFrame([values], columns=model_bundle["features"])
    return float(model_bundle["pipeline"].predict_proba(X)[0, 1])


def stock_gap(demand: float, stock: int, ordered: int) -> tuple[int, float]:
    """Return (available units, gap). Gap = max(0, demand - (stock + already ordered)).

    A planning estimate only: it ignores safety stock and supplier lead-time policy.
    """
    available = max(0, int(stock) + int(ordered))
    return available, max(0.0, demand - available)
