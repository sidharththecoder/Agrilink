"""Optional MySQL storage for AgriLink.

The app works without MySQL. Connection settings come from config/database_config.py.
"""
import json
import os

from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from src.database.queries import LATEST_PREDICTIONS, SAVE_MODEL_RUN, SAVE_PREDICTION
from src.database.records import rows_to_predictions



PLACEHOLDER_PASSWORD = "your_password_here"


def get_settings():
    """Read connection settings from config/database_config.py.
    Falls back to environment variables (.env) only if that file is missing."""
    try:
        from config import database_config as cfg
    except ImportError:
        cfg = None

    def pick(name, default):
        if cfg is not None and hasattr(cfg, name):
            return getattr(cfg, name)
        return os.getenv(name, default)

    return {
        "host": str(pick("MYSQL_HOST", "localhost")),
        "port": int(pick("MYSQL_PORT", 3306)),
        "user": str(pick("MYSQL_USER", "root")),
        "password": str(pick("MYSQL_PASSWORD", "")),
        "database": str(pick("MYSQL_DATABASE", "agrilink")),
    }


def is_configured():
    """True when settings are filled in and the password is not still the placeholder."""
    s = get_settings()
    return bool(s["host"] and s["user"] and s["database"]) and s["password"] != PLACEHOLDER_PASSWORD


def get_engine():
    s = get_settings()
    url = URL.create(
        "mysql+pymysql",
        username=s["user"],
        password=s["password"],
        host=s["host"],
        port=s["port"],
        database=s["database"],
    )
    return create_engine(url, pool_pre_ping=True, connect_args={"connect_timeout": 3})


def save_prediction(module_name, inputs, prediction):
    with get_engine().begin() as conn:
        conn.execute(text(SAVE_PREDICTION), {
            "module_name": module_name,
            "input_json": json.dumps(inputs, default=str),
            "prediction_json": json.dumps(prediction, default=str),
        })


def save_model_run(module_name, model_name, metrics):
    with get_engine().begin() as conn:
        conn.execute(text(SAVE_MODEL_RUN), {
            "module_name": module_name,
            "model_name": model_name,
            "metrics_json": json.dumps(metrics, default=str),
        })


def get_latest_predictions(module_name, limit=1):
    """Most recent saved predictions for a module. Returns [] if MySQL is off or unreachable."""
    if not is_configured():
        return []
    try:
        with get_engine().connect() as conn:
            result = conn.execute(text(LATEST_PREDICTIONS), {"module_name": module_name, "limit": int(limit)})
            return rows_to_predictions(result.mappings().all())
    except Exception:
        return []


def test_connection():
    with get_engine().connect() as conn:
        return conn.execute(text("SELECT 1")).scalar() == 1
