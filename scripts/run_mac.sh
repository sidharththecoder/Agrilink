#!/bin/bash
set -e
cd "$(dirname "$0")/.."
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m src.preprocessing.pipelines
python -m scripts.train_all
python -m src.integration.farmer_mandi
streamlit run app/Home.py
