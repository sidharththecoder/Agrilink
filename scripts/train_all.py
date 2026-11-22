"""Train all four AgriLink models and write one combined metrics file.

Run from the project root:  python -m scripts.train_all
"""
import json
import sys
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.models.common import save_json  # noqa: E402
from src.models.train_demand import train_demand  # noqa: E402
from src.models.train_farmer import train_farmer  # noqa: E402
from src.models.train_inventory import train_inventory  # noqa: E402
from src.models.train_mandi import train_mandi  # noqa: E402

TRAINERS = {"farmer": train_farmer, "mandi": train_mandi,
            "demand": train_demand, "inventory": train_inventory}

if __name__ == "__main__":
    results = {}
    for name, fn in TRAINERS.items():
        print("Training", name, flush=True)
        try:
            results[name] = fn()
        except Exception as exc:
            results[name] = {"error": str(exc), "traceback": traceback.format_exc()}
        print(json.dumps(results[name], indent=2, default=float), flush=True)
    save_json("all_metrics.json", results)
    print("Saved combined metrics.", flush=True)
