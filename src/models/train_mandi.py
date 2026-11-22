"""Train the Mandi Price model: predicts next-month modal price from lag features."""
import pandas as pd

from src.models.common import CLEAN, train_regression


def train_mandi():
    monthly = pd.read_csv(CLEAN / "mandi" / "mandi_prices_monthly_cleaned.csv")
    monthly = monthly.sort_values(["State", "Commodity", "year", "month"]).copy()
    # Lag features use only past months. shift(1) makes sure the current month is never used.
    monthly["lag_1"] = monthly.groupby(["State", "Commodity"])["Modal_Price"].shift(1)
    monthly["lag_3_mean"] = monthly.groupby(["State", "Commodity"])["Modal_Price"].transform(
        lambda s: s.shift(1).rolling(3, min_periods=1).mean())
    monthly = monthly.dropna(subset=["lag_1"])
    # Reproducible sample for practical training time. Sampling happens before the split,
    # and the split is still chronological by year.
    if len(monthly) > 180_000:
        monthly = monthly.sample(n=180_000, random_state=42)
    features = ["State", "Commodity", "year", "month", "lag_1", "lag_3_mean"]
    return train_regression(monthly, "Modal_Price", features, "mandi", time_col="year",
                            categorical=["State", "Commodity"], trees=45, depth=16)


if __name__ == "__main__":
    print(train_mandi())
