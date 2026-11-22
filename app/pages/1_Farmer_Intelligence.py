import sys
from pathlib import Path
import pandas as pd
import streamlit as st
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from app.components.ui import page_header,load_csv,load_model,log_prediction,show_last_saved
page_header("Farmer Intelligence","Estimate crop production from local agricultural and cultivation signals")
show_last_saved("farmer", "Farmer production")
modelp=ROOT/"models/farmer/farmer.joblib"; datap=ROOT/"data/cleaned/farmer/crop_production_cleaned.csv"
if not modelp.exists() or not datap.exists(): st.error("Farmer model or cleaned dataset is missing."); st.stop()
data=load_csv(str(datap),usecols=["year","state_name","district_name","crop_name","season","area"])
# The supplied cleaned CSV stores agricultural years as strings such as "2001-2002".
# The trained model expects the numeric starting year (year_start).
data["year_start"] = pd.to_numeric(data["year"].astype(str).str.extract(r"(\d{4})")[0], errors="coerce")
data = data.dropna(subset=["year_start"])
data["year_start"] = data["year_start"].astype(int)
obj=load_model(str(modelp))
st.markdown("<div class='eyebrow'>PRODUCTION ESTIMATOR</div>",unsafe_allow_html=True)
c1,c2=st.columns(2,gap="large")
states=sorted(data.state_name.dropna().unique().tolist())
state=c1.selectbox("State / Union Territory",states,key="farmer_state")
districts=sorted(data.loc[data.state_name.eq(state),"district_name"].dropna().astype(str).unique().tolist())
if not districts: st.warning("No district records are available for this state."); st.stop()
# Selectors are deliberately outside a Streamlit form so district options refresh immediately on state change.
district=c2.selectbox("District",districts,key=f"farmer_district_{state}")
crops=sorted(data.crop_name.dropna().astype(str).unique().tolist())
seasons=sorted(x for x in data.season.dropna().astype(str).unique().tolist() if x.casefold()!="total")
c3,c4=st.columns(2,gap="large")
crop=c3.selectbox("Crop",crops,key="farmer_crop")
season=c4.selectbox("Season",seasons,key="farmer_season")
c5,c6=st.columns(2,gap="large")
year=c5.number_input("Agricultural year starting",2001,2022,2022,key="farmer_year")
area=c6.number_input("Cultivated area (hectares)",min_value=0.0,value=100.0,step=10.0,key="farmer_area")
if st.button("Estimate production",type="primary",key="farmer_predict"):
    X=pd.DataFrame([{"year_start":year,"state_name":state,"district_name":district,"crop_name":crop,"season":season,"area":area}])
    try:
        pred=float(obj["pipeline"].predict(X)[0])
        st.metric("Estimated crop production",f"{pred:,.2f} tonnes")
        log_prediction("farmer",X.iloc[0].to_dict(),{"production_tonnes":pred})
    except Exception as e: st.error(f"Prediction could not be completed: {e}")
