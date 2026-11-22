"""Train the Farmer Intelligence model: predicts crop production (tonnes)."""
import pandas as pd

from src.models.common import CLEAN, train_regression


def train_farmer():
    df = pd.read_csv(CLEAN / "farmer" / "crop_production_cleaned.csv")
    # Exclude 'Total' rows so each crop/season observation is counted once.
    df = df[df["season"].str.casefold() != "total"].copy()
    df["year_start"] = pd.to_numeric(df["year"].str[:4], errors="coerce")
    features = ["year_start", "state_name", "district_name", "crop_name", "season", "area"]
    return train_regression(df, "production", features, "farmer", time_col="year_start",
                            categorical=["state_name", "district_name", "crop_name", "season"])


if __name__ == "__main__":
    print(train_farmer())
