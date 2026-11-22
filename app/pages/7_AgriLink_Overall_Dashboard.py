import json,sys
from pathlib import Path
import streamlit as st
ROOT=Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path: sys.path.insert(0,str(ROOT))
from app.components.ui import page_header
page_header('AgriLink Overall Decision Dashboard','A single command centre for field production, market prices, retail demand and inventory risk')
metrics_file=ROOT/'reports/model_evaluation/all_metrics.json'
try: metrics=json.loads(metrics_file.read_text())
except Exception: metrics={}
labels=[('farmer','Farmer production'),('mandi','Mandi price'),('demand','Store demand'),('inventory','Inventory risk')]
cols=st.columns(4)
for col,(key,label) in zip(cols,labels):
    m=metrics.get(key,{})
    with col:
        if key=='inventory': val=f"AUC {m.get('roc_auc',0):.3f}" if m else 'Model ready'
        else: val=f"R² {m.get('R2', m.get('r2', 0)):.3f}" if m else 'Model ready'
        st.metric(label,val)
st.markdown('### Seven intelligence workspaces')
sections=[('01','Farmer Intelligence','Crop production prediction','pages/1_Farmer_Intelligence.py'),('02','Mandi Price Intelligence','Monthly modal-price forecast','pages/2_Mandi_Price_Intelligence.py'),('03','Farmer–Mandi Integrated Intelligence','Production and price combined into indicative gross value (top of Integrated Intelligence page)','pages/5_Integrated_Intelligence.py'),('04','Store Demand Intelligence','Retail units-sold forecast','pages/3_Store_Demand_Intelligence.py'),('05','Inventory Intelligence','SKU backorder-risk classification','pages/4_Inventory_Intelligence.py'),('06','Store–Inventory Integrated Intelligence','Demand, stock gap and backorder-risk decision support','pages/5_Integrated_Intelligence.py')]
for i in range(0,len(sections),2):
    a,b=st.columns(2)
    for c,(num,title,desc,path) in zip((a,b),sections[i:i+2]):
        with c:
            with st.container(border=True):
                st.caption('WORKSPACE '+num); st.subheader(title); st.write(desc); st.page_link(path,label='Open workspace',icon='↗')
st.info('Integrated outputs are decision-support estimates. Farmer–Mandi uses the existing crop/state mapping. Store–Inventory uses two model outputs but does not claim a verified product/SKU join.')
st.markdown('### Decision workflow')
st.markdown('**Field:** estimate production → **Market:** forecast mandi price → **Retail:** forecast demand → **Supply:** assess backorder risk → **Action:** review stock-gap recommendations.')
