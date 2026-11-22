import sys
from pathlib import Path
import pandas as pd
import streamlit as st
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from app.components.ui import page_header,load_csv,load_model,log_prediction,show_last_saved
from src.prediction.predictor import store_product_pairs, predict_demand_any_store_product
page_header("Store Demand Intelligence","Estimate average retail units sold across all stores and products, from market conditions")
show_last_saved("demand", "Store demand")
mp=ROOT/"models/demand/demand.joblib"; dp=ROOT/"data/cleaned/demand/store_demand_cleaned.csv"
if not mp.exists() or not dp.exists(): st.error("Demand model or cleaned dataset is missing."); st.stop()
d=load_csv(str(dp)); d["Date"]=pd.to_datetime(d.Date,errors="coerce")
obj=load_model(str(mp))
pairs=store_product_pairs(d)
med=d.median(numeric_only=True)
st.caption(f"The prediction is the average over {len(pairs)} store–product pairs in the dataset. "
           "Enter the market conditions below; you do not need to choose a store or product.")
c3,c4=st.columns(2,gap="large")
date=c3.date_input("Forecast date",value=d.Date.max().date())
inventory=c4.number_input("Inventory level (units per store)",0,100000,int(med["Inventory Level"]))
c5,c6=st.columns(2,gap="large")
ordered=c5.number_input("Units ordered",0,100000,int(med["Units Ordered"]))
price=c6.number_input("Selling price",0.0,100000.0,float(med["Price"]))
c7,c8=st.columns(2,gap="large")
discount=c7.number_input("Discount (%)",0.0,100.0,float(med["Discount"]))
competitor=c8.number_input("Competitor price",0.0,100000.0,float(med["Competitor Pricing"]))
c9,c10=st.columns(2,gap="large")
holiday=c9.selectbox("Holiday / promotion",[0,1],index=int(med["Holiday/Promotion"]))
weather=c10.selectbox("Weather",sorted(d["Weather Condition"].dropna().unique()))
season=st.selectbox("Seasonality",sorted(d.Seasonality.dropna().unique()))
if st.button("Predict units sold",type="primary"):
    base={"date":pd.Timestamp(date),"stock":inventory,"ordered":ordered,"price":price,"discount":discount,
          "competitor":competitor,"holiday":holiday,"weather":weather,"season":season}
    try:
        pred,n=predict_demand_any_store_product(obj,base,pairs)
        st.metric("Estimated units sold (average per store and product)",f"{pred:,.1f} units")
        st.caption(f"Averaged over {n} store–product pairs.")
        log_prediction("demand",{**{k:str(v) for k,v in base.items()},"pairs":n},{"units_sold":pred})
    except Exception as e: st.error(f"Demand prediction failed: {e}")
