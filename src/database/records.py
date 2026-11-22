"""Turns database rows into plain dictionaries for the app. No database driver is needed here."""
import json


def as_dict(value):
    """MySQL JSON columns may come back as a string or as a parsed dict, depending on the driver."""
    if isinstance(value, (bytes, bytearray)):
        value = value.decode("utf-8")
    if isinstance(value, str):
        return json.loads(value)
    return value or {}


def rows_to_predictions(rows):
    """Convert saved prediction rows (newest first) into dicts the pages can display."""
    return [{
        "prediction_id": row["prediction_id"],
        "module_name": row["module_name"],
        "inputs": as_dict(row["input_json"]),
        "outputs": as_dict(row["prediction_json"]),
        "created_at": str(row["created_at"]),
    } for row in rows]
