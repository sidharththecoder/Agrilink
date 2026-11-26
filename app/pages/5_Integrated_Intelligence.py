import sys
from pathlib import Path

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.components.ui import page_header, load_csv, load_model, log_prediction, show_last_saved, year_note
from src.integration.farmer_mandi import CROP_ALIASES, STATE_ALIASES
from src.prediction.predictor import (
    predict_farmer_production, forecast_next_mandi_price, indicative_gross_value,
    predict_demand_any_store_product, store_product_pairs, predict_backorder_probability, stock_gap,
)

page_header("Integrated Intelligence",
            "Connect crop production with mandi prices, then store demand with inventory risk")
show_last_saved("integrated_farmer_mandi", "Farmer + Mandi")
show_last_saved("store_inventory_integrated", "Store + Inventory")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
FARMER_CLEAN = ROOT / "data/cleaned/farmer/crop_production_cleaned.csv"
MANDI_CLEAN = ROOT / "data/cleaned/mandi/mandi_prices_monthly_cleaned.csv"
DEMAND_CLEAN = ROOT / "data/cleaned/demand/store_demand_cleaned.csv"
INVENTORY_CLEAN = ROOT / "data/cleaned/inventory/inventory_cleaned.csv"
FARMER_MODEL = ROOT / "models/farmer/farmer.joblib"
MANDI_MODEL = ROOT / "models/mandi/mandi.joblib"
DEMAND_MODEL = ROOT / "models/demand/demand.joblib"
INVENTORY_MODEL = ROOT / "models/inventory/inventory.joblib"


# ---------------------------------------------------------------------------
# Integration 01: Farmer + Mandi  (top)
# ---------------------------------------------------------------------------
def render_farmer_mandi():
    st.markdown("<div class='eyebrow'>INTEGRATION 01 · FARMER + MANDI</div>", unsafe_allow_html=True)
    st.caption("Predicted production (tonnes) × 10 quintals/tonne × predicted mandi price (₹/quintal).")

    if not all(p.exists() for p in [FARMER_CLEAN, MANDI_CLEAN, FARMER_MODEL, MANDI_MODEL]):
        st.error("Farmer or mandi data/model files are missing.")
        return

    f = load_csv(str(FARMER_CLEAN), usecols=["year", "state_name", "district_name",
                                             "crop_name", "season", "area"])
    f["year_start"] = pd.to_numeric(f["year"].astype(str).str.extract(r"(\d{4})")[0], errors="coerce")
    f = f.dropna(subset=["year_start"])
    f["year_start"] = f["year_start"].astype(int)
    f = f[f["season"].astype(str).str.casefold() != "total"]
    m = load_csv(str(MANDI_CLEAN))

    states = sorted(f["state_name"].dropna().unique())
    c1, c2 = st.columns(2, gap="large")
    state = c1.selectbox("Farmer state", states, key="integrated_state")
    districts = sorted(f.loc[f["state_name"].eq(state), "district_name"].dropna().unique())
    district = c2.selectbox("District", districts, key=f"integrated_district_{state}")

    crops = sorted(f["crop_name"].dropna().unique())
    seasons = sorted(x for x in f["season"].dropna().unique() if str(x).casefold() != "total")
    c3, c4 = st.columns(2, gap="large")
    crop = c3.selectbox("Crop", crops, key="integrated_crop")
    season = c4.selectbox("Season", seasons, key="integrated_season")

    c5, c6 = st.columns(2, gap="large")
    year = c5.number_input("Prediction year", min_value=1900, max_value=2100, value=2027, step=1, key="integrated_year")
    note = year_note(int(year))
    if note:
        st.caption(note)
    area = c6.number_input("Cultivated area (hectares)", min_value=0.0, value=100.0,
                           step=10.0, key="integrated_area")

    st.markdown("<div class='eyebrow'>02 / MARKET FORECAST</div>", unsafe_allow_html=True)
    mandi_states = sorted(m["State"].dropna().unique())
    guessed_state = STATE_ALIASES.get(state.strip().casefold(), state)
    default_state = guessed_state if guessed_state in mandi_states else mandi_states[0]
    mc1, mc2 = st.columns(2, gap="large")
    mandi_state = mc1.selectbox("Mandi state", mandi_states,
                                index=mandi_states.index(default_state), key="integrated_mandi_state")
    commodities = sorted(m.loc[m["State"].eq(mandi_state), "Commodity"].dropna().unique())
    suggested = CROP_ALIASES.get(crop.strip().casefold(), crop)
    commodity = mc2.selectbox("Commodity", commodities,
                              index=commodities.index(suggested) if suggested in commodities else 0,
                              key=f"integrated_commodity_{mandi_state}")

    if st.button("Run farmer + mandi prediction", type="primary", key="btn_farmer_mandi"):
        try:
            production = predict_farmer_production(
                load_model(str(FARMER_MODEL)), year_start=year, state_name=state,
                district_name=district, crop_name=crop, season=season, area=area)
            forecast = forecast_next_mandi_price(load_model(str(MANDI_MODEL)), m, mandi_state, commodity)
            if forecast is None:
                st.warning("No price history for this state and commodity.")
                return
            price = forecast["price"]
            gross = indicative_gross_value(production, price)
            a, b, c = st.columns(3)
            a.metric("Predicted production", f"{production:,.1f} tonnes")
            b.metric("Next-month modal price", f"₹{price:,.2f}/quintal")
            c.metric("Indicative gross value", f"₹{gross:,.0f}")
            log_prediction("integrated_farmer_mandi",
                           {"state": state, "district": district, "crop": crop, "season": season,
                            "year": year, "area": area, "mandi_state": mandi_state, "commodity": commodity},
                           {"production_tonnes": production, "next_month_modal_price": price,
                            "indicative_gross_value": gross})
            st.caption(f"Mandi forecast period: {forecast['year']}-{forecast['month']:02d}. "
                       "Gross value is an indicative estimate, not profit or guaranteed farm-gate revenue.")
        except Exception as e:
            st.error(f"Farmer + mandi prediction failed: {e}")


# ---------------------------------------------------------------------------
# Integration 02: Store Demand + Inventory  (below)
# ---------------------------------------------------------------------------
def render_store_inventory():
    st.markdown("<div class='eyebrow'>INTEGRATION 02 · STORE DEMAND + INVENTORY</div>", unsafe_allow_html=True)
    st.caption("Forecast demand, compare it with stock already on hand or ordered, and check backorder risk.")

    if not all(p.exists() for p in [DEMAND_CLEAN, INVENTORY_CLEAN, DEMAND_MODEL, INVENTORY_MODEL]):
        st.error("Store demand or inventory data/model files are missing.")
        return

    d = load_csv(str(DEMAND_CLEAN))
    d["Date"] = pd.to_datetime(d["Date"], errors="coerce")
    dmodel = load_model(str(DEMAND_MODEL))
    imodel = load_model(str(INVENTORY_MODEL))
    feats = imodel["features"]
    inv = load_csv(str(INVENTORY_CLEAN), usecols=feats)
    med = inv[feats].median(numeric_only=True)

    st.markdown("#### 01 / Demand forecast")
    st.caption("Demand is averaged over every store and product in the dataset, so you do not choose one.")
    pairs = store_product_pairs(d)
    med_d = d.median(numeric_only=True)

    c3, c4, c5 = st.columns(3)
    latest_date = d["Date"].max()
    date = c3.date_input("Forecast date",
                         value=latest_date.date() if pd.notna(latest_date) else pd.Timestamp.today().date(),
                         key="si_date")
    price = c4.number_input("Selling price", min_value=0.0, value=float(med_d["Price"]), key="si_price")
    discount = c5.number_input("Discount (%)", 0.0, 100.0, float(med_d["Discount"]), key="si_discount")

    c6, c7, c8 = st.columns(3)
    stock = c6.number_input("Current store stock (units per store)", 0, 1000000, int(med_d["Inventory Level"]), key="si_stock")
    ordered = c7.number_input("Units already ordered", 0, 1000000, int(med_d["Units Ordered"]), key="si_ordered")
    competitor = c8.number_input("Competitor price", 0.0, 1000000.0,
                                 float(med_d["Competitor Pricing"]), key="si_competitor")

    c9, c10 = st.columns(2)
    holiday = c9.selectbox("Holiday / promotion", [0, 1], index=int(med_d["Holiday/Promotion"]), key="si_holiday")
    weather = c10.selectbox("Weather", sorted(d["Weather Condition"].dropna().unique()), key="si_weather")
    season = st.selectbox("Seasonality", sorted(d["Seasonality"].dropna().unique()), key="si_season")

    st.markdown("#### 02 / Inventory risk signals")
    st.caption("Enter the inventory/SKU signals for the item being assessed. The inventory dataset has no "
               "verified common Product ID with the store-demand dataset, so these inputs are not automatically joined.")
    values = {}
    flags = {"potential_issue", "deck_risk", "oe_constraint", "ppap_risk", "stop_auto_buy", "rev_stop"}
    with st.expander("Inventory model inputs", expanded=False):
        cols = st.columns(3)
        for n, f in enumerate(feats):
            default = float(med[f]) if f in med and pd.notna(med[f]) else 0.0
            with cols[n % 3]:
                if f in flags:
                    values[f] = st.selectbox(f, [0, 1], index=int(default >= .5), key="si_" + f)
                else:
                    values[f] = st.number_input(f, min_value=0.0, value=max(0.0, default),
                                                step=1.0, key="si_" + f)
        # Keep the inventory signal aligned with the stock quantity entered above.
        values["national_inv"] = float(stock)

    if st.button("Generate store + inventory recommendation", type="primary", key="btn_store_inventory"):
        try:
            demand, n_pairs = predict_demand_any_store_product(dmodel, {
                "date": pd.Timestamp(date), "stock": stock, "ordered": ordered,
                "price": price, "discount": discount, "competitor": competitor,
                "holiday": holiday, "weather": weather, "season": season,
            }, pairs)
            prob = predict_backorder_probability(imodel, values)
            available, gap = stock_gap(demand, stock, ordered)

            st.divider()
            a, b, c = st.columns(3)
            a.metric("Forecast demand", f"{demand:,.1f} units")
            b.metric("Backorder risk", f"{prob:.1%}")
            c.metric("Estimated stock gap", f"{gap:,.1f} units")
            if prob >= .5 or gap > 0:
                st.warning("REPLENISHMENT ATTENTION REQUIRED")
                st.markdown(f"**Suggested minimum replenishment:** {int(round(gap))} units to cover "
                            "the forecast gap, before adding any safety stock.")
            else:
                st.success("CURRENT STOCK COVERS THE FORECAST")
            st.caption("Planning estimate only. It does not account for supplier lead-time commitments, "
                       "safety-stock policy or a verified product-to-SKU join.")
            log_prediction("store_inventory_integrated",
                           {"pairs_averaged": n_pairs, "stock": stock, "ordered": ordered},
                           {"forecast_demand": demand, "backorder_probability": prob,
                            "estimated_stock_gap": gap})
        except Exception as e:
            st.error(f"Store + inventory assessment failed: {e}")


render_farmer_mandi()
st.divider()
render_store_inventory()
