@echo off
cd /d %~dp0\..
py -m venv .venv
call .venv\Scripts\activate
py -m pip install --upgrade pip
pip install -r requirements.txt
py -m src.preprocessing.pipelines
py -m scripts.train_all
py -m src.integration.farmer_mandi
streamlit run app/Home.py
