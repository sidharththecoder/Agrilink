"""SQL used by AgriLink. Kept as plain strings so they can be read and tested without MySQL."""

SAVE_PREDICTION = """
INSERT INTO prediction_logs (module_name, input_json, prediction_json)
VALUES (:module_name, :input_json, :prediction_json)
"""

SAVE_MODEL_RUN = """
INSERT INTO model_runs (module_name, model_name, metrics_json)
VALUES (:module_name, :model_name, :metrics_json)
"""

# Most recent predictions for one module, newest first.
# prediction_id breaks ties when two rows share the same timestamp.
LATEST_PREDICTIONS = """
SELECT prediction_id, module_name, input_json, prediction_json, created_at
FROM prediction_logs
WHERE module_name = :module_name
ORDER BY created_at DESC, prediction_id DESC
LIMIT :limit
"""
