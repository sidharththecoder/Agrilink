-- AgriLink MySQL schema
-- Run this whole file in MySQL Workbench (File > Open SQL Script > Execute).
-- Creates the `agrilink` schema with two tables:
--   prediction_logs : every prediction made in the app, with the time it was made
--   model_runs      : evaluation metrics for each trained model

CREATE DATABASE IF NOT EXISTS agrilink
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE agrilink;

CREATE TABLE IF NOT EXISTS model_runs (
  run_id       BIGINT AUTO_INCREMENT PRIMARY KEY,
  module_name  VARCHAR(80)  NOT NULL,
  model_name   VARCHAR(120) NOT NULL,
  metrics_json JSON         NOT NULL,
  created_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY idx_model_module_time (module_name, created_at)
);

CREATE TABLE IF NOT EXISTS prediction_logs (
  prediction_id   BIGINT AUTO_INCREMENT PRIMARY KEY,
  module_name     VARCHAR(80) NOT NULL,      -- farmer, mandi, demand, inventory, integrated_farmer_mandi, store_inventory_integrated
  input_json      JSON        NOT NULL,      -- the inputs the user entered
  prediction_json JSON        NOT NULL,      -- the model outputs
  created_at      TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
  KEY idx_prediction_module_time (module_name, created_at)
);

-- Quick checks to run in Workbench after using the app:
-- SELECT * FROM prediction_logs ORDER BY created_at DESC LIMIT 20;
-- SELECT module_name, COUNT(*) AS predictions FROM prediction_logs GROUP BY module_name;
