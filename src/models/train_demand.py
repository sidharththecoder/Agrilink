"""Train the Store Demand model: predicts units sold."""
import pandas as pd

from src.models.common import CLEAN, train_regression


def train_demand():
    df = pd.read_csv(CLEAN / "demand" / "store_demand_cleaned.csv")
    dates = pd.to_datetime(df["Date"])
    df["year"] = dates.dt.year
    df["month"] = dates.dt.month
    df["dayofweek"] = dates.dt.dayofweek
    features = ["year", "month", "dayofweek", "Store ID", "Product ID", "Category", "Region",
                "Inventory Level", "Units Ordered", "Price", "Discount", "Competitor Pricing",
                "Holiday/Promotion", "Weather Condition", "Seasonality"]
    return train_regression(
        df, "Units Sold", features, "demand", time_col="Date",
        categorical=["Store ID", "Product ID", "Category", "Region", "Weather Condition", "Seasonality"])


if __name__ == "__main__":
    print(train_demand())
