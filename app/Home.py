import json, sys
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.components.ui import theme

st.set_page_config(
    page_title="AgriLink",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={},
)
theme()

# Homepage-only visual treatment: cinematic black with a deep green palette, inspired by
# the supplied product video. The seven workspaces are presented as a long,
# scrollable editorial dashboard rather than a grid of click-to-open tiles.
st.markdown("""<style>
:root{--primary:#054D3A;--black:#050807;--cream:#EAE6DF;--lime:#A7F432;--teal:#3B8F7B;--gold:#C6A66B}
.stApp{background:
 radial-gradient(ellipse at 4% 4%,rgba(5,77,58,.58),transparent 34%),
 radial-gradient(ellipse at 92% 18%,rgba(59,143,123,.16),transparent 28%),
 radial-gradient(ellipse at 52% 65%,rgba(5,77,58,.23),transparent 38%),
 linear-gradient(145deg,#030605 0%,#06120e 48%,#020403 100%)!important;background-attachment:fixed!important}
[data-testid="stMainBlockContainer"]{max-width:1380px;padding-top:2.2rem;padding-bottom:5rem}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#030806,#061B16)!important;border-right:1px solid rgba(59,143,123,.25)!important}
.brandbar{display:flex;align-items:center;justify-content:space-between;gap:18px;padding:12px 0 22px;border-bottom:1px solid rgba(234,230,223,.14);margin-bottom:42px}
.brandname{font-family:'Manrope',sans-serif;font-size:.86rem;letter-spacing:.32em;font-weight:800;color:#EAE6DF;text-transform:uppercase}
.brandname span{color:#A7F432}
.brandmeta{font-size:.68rem;letter-spacing:.18em;color:#7F9B8F;text-transform:uppercase}
.hero-shell{position:relative;overflow:hidden;border:1px solid rgba(59,143,123,.34);border-radius:30px;padding:clamp(28px,5vw,68px);background:linear-gradient(118deg,rgba(5,77,58,.62),rgba(5,12,9,.96) 64%,rgba(3,7,5,.98));box-shadow:0 30px 100px rgba(0,0,0,.4),inset 0 1px rgba(234,230,223,.08)}
.hero-shell:after{content:'';position:absolute;width:430px;height:430px;border-radius:50%;right:-90px;top:-150px;background:radial-gradient(circle,rgba(59,143,123,.28),rgba(5,77,58,.05) 52%,transparent 70%);pointer-events:none}
.hero-kicker,.section-kicker{font-size:.68rem;letter-spacing:.27em;text-transform:uppercase;font-weight:800;color:#A7F432}
.hero-heading{font-family:'Playfair Display',Georgia,serif;font-size:clamp(3.4rem,8vw,7.4rem);line-height:.91;letter-spacing:-.055em;color:#EAE6DF;margin:24px 0 22px;position:relative;z-index:1}
.hero-heading em{font-style:normal;color:#A7F432}
.hero-text{max-width:720px;font-size:1.02rem;line-height:1.85;color:#B9C9C1;position:relative;z-index:1}
.hero-stats{display:flex;gap:12px;flex-wrap:wrap;margin-top:34px;position:relative;z-index:1}
.stat-pill{border:1px solid rgba(234,230,223,.17);background:rgba(0,0,0,.28);padding:10px 15px;border-radius:999px;color:#DCE5DF;font-size:.78rem}
.stat-pill b{color:#A7F432;margin-right:6px}
.section-intro{display:flex;align-items:end;justify-content:space-between;gap:24px;margin:62px 0 22px}
.section-title{font-family:'Playfair Display',Georgia,serif;color:#EAE6DF;font-size:clamp(2rem,4vw,3.4rem);line-height:1.05;margin-top:10px}
.section-note{max-width:440px;color:#8FA79B;font-size:.84rem;line-height:1.7}
.workspace{position:relative;overflow:hidden;border:1px solid rgba(234,230,223,.13);border-radius:24px;padding:26px 28px;background:linear-gradient(120deg,rgba(5,77,58,.48),rgba(9,14,12,.91) 72%);box-shadow:0 18px 55px rgba(0,0,0,.22);min-height:190px;margin-bottom:14px}
.workspace:before{content:'';position:absolute;inset:0 auto 0 0;width:3px;background:linear-gradient(180deg,#A7F432,#3B8F7B,transparent)}
.workspace-no{font-size:.67rem;letter-spacing:.22em;color:#A7F432;font-weight:800}
.workspace-title{font-family:'Playfair Display',Georgia,serif;font-size:1.75rem;color:#EAE6DF;margin:9px 0 8px}
.workspace-desc{color:#AFC1B7;font-size:.9rem;line-height:1.7;max-width:850px}
.workspace-tag{display:inline-block;margin-top:16px;padding:6px 10px;border:1px solid rgba(59,143,123,.4);border-radius:99px;color:#9DC5B4;font-size:.66rem;letter-spacing:.12em;text-transform:uppercase}
.dual-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.dual-grid .workspace{min-height:218px}
.feature-band{border:1px solid rgba(167,244,50,.25);border-radius:26px;padding:30px;background:linear-gradient(110deg,rgba(5,77,58,.78),rgba(4,10,7,.94));margin-top:18px}
.feature-band h3{font-family:'Playfair Display',Georgia,serif;color:#EAE6DF;font-size:2rem;margin:8px 0}
.feature-band p{color:#B6C8BE;line-height:1.75}
.footer-brand{padding:34px 0 12px;text-align:center;color:#7F978B;font-size:.68rem;letter-spacing:.22em;text-transform:uppercase}
.footer-brand strong{color:#A7F432;font-weight:800}
@media(max-width:760px){.dual-grid{grid-template-columns:1fr}.section-intro{display:block}.brandmeta{display:none}.workspace{padding:22px}}
</style>""", unsafe_allow_html=True)

st.markdown("""<div class='brandbar'>
  <div class='brandname'>AGRI<span>LINK</span></div>
  <div class='brandmeta'>FIELD TO MARKET &nbsp;·&nbsp; DECISION INTELLIGENCE</div>
</div>
<div class='hero-shell'>
  <div class='hero-kicker'>A connected agricultural intelligence platform</div>
  <div class='hero-heading'>From field<br>to <em>market.</em></div>
  <div class='hero-text'>AgriLink brings crop production, mandi prices, retail demand and inventory signals into one connected decision experience. Explore the platform by scrolling through its intelligence workspaces — insights first, without a dashboard full of buttons.</div>
  <div class='hero-stats'><span class='stat-pill'><b>04</b> trained ML models</span><span class='stat-pill'><b>07</b> intelligence workspaces</span><span class='stat-pill'><b>01</b> connected platform</span></div>
</div>""", unsafe_allow_html=True)

st.markdown("""<div class='section-intro'><div><div class='section-kicker'>THE PLATFORM</div><div class='section-title'>Seven ways to see<br>the bigger picture.</div></div><div class='section-note'>A continuous overview of every AgriLink capability. Scroll down to explore how field-level estimates, market forecasts and store operations fit together.</div></div>""", unsafe_allow_html=True)

sections = [
    ("01", "Farmer Intelligence", "Estimate crop production from state, district, crop, season, agricultural year and cultivated area. Turn historical agricultural patterns into a production estimate.", "CROP PRODUCTION · RANDOM FOREST REGRESSION"),
    ("02", "Mandi Price Intelligence", "Explore historical monthly modal prices and forecast market prices by state and commodity to support market-aware planning.", "MARKET PRICES · TIME-AWARE REGRESSION"),
]
for no, title, desc, tag in sections:
    st.markdown(f"<div class='workspace'><div class='workspace-no'>{no} / WORKSPACE</div><div class='workspace-title'>{title}</div><div class='workspace-desc'>{desc}</div><span class='workspace-tag'>{tag}</span></div>", unsafe_allow_html=True)

st.markdown("""<div class='feature-band'><div class='section-kicker'>INTEGRATED WORKFLOW 01</div><h3>Farmer + Mandi Intelligence</h3><p>Connect estimated crop production with mandi price forecasts. The combined view calculates an indicative gross value using production and market price signals — not profit or guaranteed farm-gate revenue.</p><span class='workspace-tag'>PRODUCTION × MARKET CONTEXT</span></div>""", unsafe_allow_html=True)

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
for no, title, desc, tag in [
    ("04", "Store Demand Intelligence", "Forecast expected retail units sold from store, product, pricing, promotion and market context. Use the forecast to anticipate demand changes.", "RETAIL DEMAND · RANDOM FOREST REGRESSION"),
    ("05", "Inventory Intelligence", "Estimate backorder risk from inventory and supply-chain signals. Identify records that may need closer attention.", "BACKORDER RISK · RANDOM FOREST CLASSIFICATION"),
]:
    st.markdown(f"<div class='workspace'><div class='workspace-no'>{no} / WORKSPACE</div><div class='workspace-title'>{title}</div><div class='workspace-desc'>{desc}</div><span class='workspace-tag'>{tag}</span></div>", unsafe_allow_html=True)

st.markdown("""<div class='feature-band'><div class='section-kicker'>INTEGRATED WORKFLOW 02</div><h3>Store + Inventory Intelligence</h3><p>Bring demand forecasts together with available stock and backorder-risk signals to highlight potential stock gaps and replenishment priorities. Product-level joins are only made where a verified product/SKU mapping exists.</p><span class='workspace-tag'>DEMAND × STOCK × RISK</span></div>""", unsafe_allow_html=True)

st.markdown("""<div class='section-intro'><div><div class='section-kicker'>THE COMPLETE VIEW</div><div class='section-title'>One decision<br>dashboard.</div></div><div class='section-note'>A high-level view of the four model systems and two integrated workflows, with clear separation between model predictions and decision logic.</div></div>
<div class='workspace' style='border-color:rgba(167,244,50,.34);background:linear-gradient(120deg,rgba(5,77,58,.68),rgba(2,7,5,.96))'>
 <div class='workspace-no'>07 / OVERALL DECISION DASHBOARD</div><div class='workspace-title'>AgriLink Overall Decision Dashboard</div>
 <div class='workspace-desc'>Review farmer production, mandi price, store demand and inventory risk signals in one place. Compare model performance, understand the two integrated workflows and identify where decisions need attention.</div>
 <span class='workspace-tag'>FOUR ML MODELS · TWO INTEGRATED WORKFLOWS · ONE PLATFORM</span>
</div>
<div class='footer-brand'><strong>AGRILINK</strong> &nbsp;·&nbsp; FIELD TO MARKET</div>""", unsafe_allow_html=True)

with st.expander("Database connection · MySQL"):
    st.write("Connect the existing AgriLink database to save prediction records. Set your credentials in config/database_config.py.")
    if st.button("Test MySQL connection", key="home_mysql_test"):
        try:
            from src.database.mysql import test_connection
            if test_connection():
                st.success("MySQL connected successfully.")
        except Exception as exc:
            st.error(f"Connection failed: {exc}")

st.caption("Predictions are estimates based on historical datasets. They are not guarantees of production, prices, sales or supply availability.")
