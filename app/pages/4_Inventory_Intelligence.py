import sys
from pathlib import Path
import pandas as pd
import streamlit as st
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from app.components.ui import page_header,load_csv,load_model,log_prediction,show_last_saved
page_header("Inventory Intelligence","Estimate SKU-level supply-chain backorder risk")
show_last_saved("inventory", "Inventory risk")
mp=ROOT/"models/inventory/inventory.joblib"; dp=ROOT/"data/cleaned/inventory/inventory_cleaned.csv"
if not mp.exists() or not dp.exists(): st.error("Inventory model or cleaned dataset is missing."); st.stop()
obj=load_model(str(mp)); features=obj["features"]; d=load_csv(str(dp),usecols=features); med=d[features].median(numeric_only=True)
flags={"potential_issue","deck_risk","oe_constraint","ppap_risk","stop_auto_buy","rev_stop"}
values={}; st.markdown("<div class='eyebrow'>CURRENT SKU SIGNALS</div>",unsafe_allow_html=True)
cols=st.columns(3,gap="large")
for i,col in enumerate(features):
    default=float(med[col]) if col in med and pd.notna(med[col]) else 0.0
    with cols[i%3]:
        if col in flags: values[col]=st.selectbox(col,[0,1],index=int(default>=.5),key=f"inv_{col}")
        else: values[col]=st.number_input(col,value=default,step=1.0,format="%.3f",key=f"inv_{col}")
if st.button("Assess backorder risk",type="primary"):
    X=pd.DataFrame([values],columns=features)
    try:
        model=obj["pipeline"]; prob=float(model.predict_proba(X)[0,1]); pred=int(prob>=.5)
        a,b=st.columns(2); a.metric("Backorder probability",f"{prob:.1%}"); b.metric("Risk assessment","HIGH RISK" if pred else "LOWER RISK")
        st.progress(min(max(prob,0.0),1.0))
        log_prediction("inventory",X.iloc[0].to_dict(),{"backorder_probability":prob,"predicted_class":pred})
    except Exception as e: st.error(f"Risk prediction failed: {e}")
