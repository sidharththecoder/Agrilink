import sys
from pathlib import Path
import pandas as pd
import streamlit as st
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from app.components.ui import page_header,load_csv,load_model,log_prediction,show_last_saved
page_header("Mandi Price Intelligence","Explore monthly market history and estimate the next month's modal price")
show_last_saved("mandi", "Mandi price")
p=ROOT/"data/cleaned/mandi/mandi_prices_monthly_cleaned.csv"; mp=ROOT/"models/mandi/mandi.joblib"
if not p.exists(): st.error("Monthly mandi dataset is missing."); st.stop()
d=load_csv(str(p)); states=sorted(d.State.dropna().unique());
c1,c2=st.columns(2,gap="large")
state=c1.selectbox("State",states,key="mandi_state")
commodities=sorted(d.loc[d.State.eq(state),"Commodity"].dropna().unique())
commodity=c2.selectbox("Commodity",commodities,key=f"mandi_commodity_{state}")
if st.button("Analyse market",type="primary"):
    x=d[(d.State==state)&(d.Commodity==commodity)].sort_values(["year","month"])
    if x.empty: st.warning("No price history found for this selection.")
    else:
        latest=x.iloc[-1]
        st.metric("Latest recorded modal price",f"₹{latest.Modal_Price:,.2f} / quintal")
        chart=x.assign(period=x.year.astype(int).astype(str)+"-"+x.month.astype(int).astype(str).str.zfill(2)).set_index("period")["Modal_Price"]
        st.line_chart(chart,height=300)
        if mp.exists() and len(x)>=2:
            next_month=int(latest.month)%12+1; next_year=int(latest.year)+(1 if int(latest.month)==12 else 0)
            X=pd.DataFrame([{"State":state,"Commodity":commodity,"year":next_year,"month":next_month,"lag_1":float(latest.Modal_Price),"lag_3_mean":float(x.tail(3).Modal_Price.mean())}])
            try:
                pred=float(load_model(str(mp))["pipeline"].predict(X)[0])
                st.metric(f"Estimated modal price · {next_year}-{next_month:02d}",f"₹{pred:,.2f} / quintal")
                log_prediction("mandi",X.iloc[0].to_dict(),{"modal_price_rupees_per_quintal":pred})
            except Exception as e: st.error(f"Price prediction failed: {e}")
        st.dataframe(x.tail(24),use_container_width=True,hide_index=True)
