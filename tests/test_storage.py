"""Tests for the MySQL storage layer.

These run the same SQL as the app against an in-memory SQLite database, so they do not
need a MySQL server. MySQL-only syntax in schema.sql (JSON, CHARACTER SET) is converted
to SQLite equivalents before the tables are created.
"""
import importlib.util
import os
import re
import sqlite3
import unittest
from pathlib import Path

from src.database.queries import LATEST_PREDICTIONS, SAVE_MODEL_RUN, SAVE_PREDICTION
from src.database.records import rows_to_predictions

SCHEMA = Path(__file__).resolve().parents[1] / "database" / "schema.sql"


def sqlite_schema():
    """Convert the MySQL schema to SQLite for testing."""
    sql = SCHEMA.read_text()
    sql = re.sub(r"CREATE DATABASE.*?;|USE agrilink;", "", sql, flags=re.S)
    sql = re.sub(r"CHARACTER SET.*?;", ";", sql, flags=re.S)
    sql = sql.replace("BIGINT AUTO_INCREMENT PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
    sql = sql.replace("JSON", "TEXT")
    sql = sql.replace("TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP", "TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP")
    sql = sql.replace("TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP", "TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP")
    # SQLite cannot declare indexes inside CREATE TABLE, so move them out.
    indexes = re.findall(r",\s*KEY (\w+) \(([^)]*)\)", sql)
    sql = re.sub(r",\s*KEY \w+ \([^)]*\)", "", sql)
    sql = re.sub(r"--[^\n]*", "", sql)
    extra = "\n".join(f"CREATE INDEX {n} ON {t} ({c});"
                      for t in ("model_runs", "prediction_logs") for n, c in indexes if n.startswith(
                          "idx_model" if t == "model_runs" else "idx_prediction"))
    return sql + "\n" + extra


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.db.row_factory = sqlite3.Row
        self.db.executescript(sqlite_schema())

    def tearDown(self):
        self.db.close()

    def save(self, module, inputs, outputs, created_at=None):
        params = {"module_name": module, "input_json": str(inputs).replace("'", '"'),
                  "prediction_json": str(outputs).replace("'", '"')}
        self.db.execute(SAVE_PREDICTION, params)
        if created_at:
            self.db.execute("UPDATE prediction_logs SET created_at = ? WHERE prediction_id = last_insert_rowid()", (created_at,))
        self.db.commit()

    def latest(self, module, limit=1):
        rows = self.db.execute(LATEST_PREDICTIONS, {"module_name": module, "limit": limit}).fetchall()
        return rows_to_predictions(rows)

    def test_schema_creates_both_tables(self):
        names = {r[0] for r in self.db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertTrue({"prediction_logs", "model_runs"} <= names)

    def test_prediction_is_saved_with_a_timestamp(self):
        self.save("farmer", {"state": "Assam"}, {"production_tonnes": 12.5})
        row = self.latest("farmer")[0]
        self.assertEqual(row["module_name"], "farmer")
        self.assertEqual(row["outputs"], {"production_tonnes": 12.5})
        self.assertTrue(row["created_at"])

    def test_latest_returns_newest_first(self):
        self.save("mandi", {"n": 1}, {"price": 1.0}, "2026-01-01 10:00:00")
        self.save("mandi", {"n": 2}, {"price": 2.0}, "2026-01-02 10:00:00")
        self.save("mandi", {"n": 3}, {"price": 3.0}, "2026-01-01 09:00:00")
        rows = self.latest("mandi", limit=3)
        self.assertEqual([r["outputs"]["price"] for r in rows], [2.0, 1.0, 3.0])

    def test_modules_do_not_mix(self):
        self.save("farmer", {}, {"production_tonnes": 1.0})
        self.save("demand", {}, {"units_sold": 9.0})
        self.assertEqual(self.latest("farmer")[0]["outputs"], {"production_tonnes": 1.0})
        self.assertEqual(self.latest("demand")[0]["outputs"], {"units_sold": 9.0})

    def test_no_row_returns_empty_list(self):
        self.assertEqual(self.latest("inventory"), [])

    def test_model_run_is_saved(self):
        self.db.execute(SAVE_MODEL_RUN, {"module_name": "farmer", "model_name": "RandomForest",
                                         "metrics_json": '{"R2": 0.79}'})
        count = self.db.execute("SELECT COUNT(*) FROM model_runs").fetchone()[0]
        self.assertEqual(count, 1)

    @unittest.skipUnless(importlib.util.find_spec("sqlalchemy"), "needs SQLAlchemy (in requirements.txt)")
    def test_storage_is_off_without_credentials(self):
        from src.database import mysql
        for key in ("MYSQL_HOST", "MYSQL_USER", "MYSQL_DATABASE"):
            os.environ.pop(key, None)
        self.assertFalse(mysql.is_configured())
        self.assertEqual(mysql.get_latest_predictions("farmer"), [])


if __name__ == "__main__":
    unittest.main()
