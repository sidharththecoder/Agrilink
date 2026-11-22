
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
C=ROOT/"data"/"cleaned"

CROP_ALIASES = {
    "arhar/tur":"Arhar (Tur/Red Gram)(Whole)", "bajra":"Bajra (Pearl Millet/Cumbu)",
    "barley":"Barley (Jau)", "beet root":"Beetroot", "ber":"Ber (Zizyphus/Borehannu)",
    "bhindi":"Bhindi (Ladies Finger)", "cardamom":"Cardamoms", "cotton(lint)":"Cotton",
    "cowpea(lobia)":"Cowpea (Lobia/Karamani)", "cucumber":"Cucumbar (Kheera)",
    "dry ginger":"Ginger (Dry)", "gram":"Bengal Gram (Gram)(Whole)",
    "guar seed":"Guar Seed (Cluster Beans Seed)", "horse-gram":"Kulthi (Horse Gram)",
    "jowar":"Jowar (Sorghum)", "masoor":"Lentil (Masur)(Whole)",
    "moong(green gram)":"Green Gram (Moong)(Whole)", "ragi":"Ragi (Finger Millet)",
    "rapeseed &mustard":"Mustard", "sesamum":"Sesamum (Sesame,Gingelly,Til)",
    "urad":"Black Gram (Urd Beans)(Whole)", "arecanut":"Arecanut (Betelnut/Supari)",
    "arcanut (processed)":"Arecanut (Betelnut/Supari)", "atcanut (raw)":"Arecanut (Betelnut/Supari)",
    "cashewnut":"Cashewnuts", "cashewnut processed":"Cashewnuts", "cashewnut raw":"Cashewnuts",
    "ginger":"Ginger (Green)", "coriander":"Corriander seed", "sapota":"Chikoos (Sapota)",
    "redish":"Radish", "snak guard":"Snakeguard", "ribed guard":"Ridgeguard (Tori)",
    "ash gourd":"Ashgourd", "colocosia":"Colacasia", "citrus fruit":"Orange"
}
STATE_ALIASES = {
    "andaman and nicobar islands":"Andaman and Nicobar",
    "chhattisgarh":"Chattisgarh", "puducherry":"Pondicherry",
    "uttarakhand":"Uttrakhand"
}
def build():
    farmer=pd.read_csv(C/"farmer"/"crop_production_cleaned.csv")
    farmer=farmer[farmer["season"].str.casefold()!="total"].copy()
    farmer["agri_start"]=pd.to_numeric(farmer["year"].str[:4],errors="coerce")
    farmer=farmer[(farmer.agri_start>=2001)&(farmer.agri_start<=2022)]
    farmer["Commodity_mapped"]=farmer["crop_name"].astype(str).str.strip().str.casefold().map(CROP_ALIASES).fillna(farmer["crop_name"].astype(str).str.strip())
    farmer["State_mapped"]=farmer["state_name"].astype(str).str.strip().str.casefold().map(STATE_ALIASES).fillna(farmer["state_name"].astype(str).str.strip())
    farmer["Commodity_key"]=farmer["Commodity_mapped"].astype(str).str.strip().str.casefold()
    farmer["State_key"]=farmer["State_mapped"].astype(str).str.strip().str.casefold()
    farmer["agri_end"]=farmer.agri_start+1
    farmer["agri_year"]=farmer.agri_start.astype("Int64").astype(str)+"-"+farmer.agri_end.astype("Int64").astype(str)
    monthly=pd.read_csv(C/"mandi"/"mandi_prices_monthly_cleaned.csv")
    # July-Dec belong to agricultural year starting in calendar year; Jan-Jun belong to previous July.
    monthly["agri_start"]=monthly["year"].where(monthly["month"]>=7,monthly["year"]-1)
    monthly["Commodity_key"]=monthly["Commodity"].astype(str).str.strip().str.casefold()
    monthly["State_key"]=monthly["State"].astype(str).str.strip().str.casefold()
    monthly=monthly[(monthly.agri_start>=2001)&(monthly.agri_start<=2022)]
    # Weight monthly means by daily observations when forming agricultural-year mean.
    monthly["weighted_price"]=monthly["Modal_Price"]*monthly["records"]
    annual=monthly.groupby(["State_key","Commodity_key","agri_start"],as_index=False).agg(
        weighted_price=("weighted_price","sum"),mandi_records=("records","sum"))
    annual["mandi_modal_price_mean"]=annual["weighted_price"]/annual["mandi_records"]
    annual=annual.drop(columns="weighted_price")
    merged=farmer.merge(annual,on=["State_key","Commodity_key","agri_start"],how="inner")
    # ₹/quintal × 10 quintals/tonne × tonnes gives indicative gross value in ₹.
    merged["indicative_gross_value_inr"]=merged["production"]*10*merged["mandi_modal_price_mean"]
    out=C/"integration"/"farmer_mandi_integrated.csv"
    out.parent.mkdir(parents=True,exist_ok=True); merged.to_csv(out,index=False)
    unmatched_crop=sorted(set(farmer["Commodity_key"])-set(annual["Commodity_key"]))
    print("Farmer rows:",len(farmer),"matched rows:",len(merged),"match rate:",round(len(merged)/max(len(farmer),1),4))
    
    print("Unmatched crop names (first 30):",unmatched_crop[:30])
    pd.DataFrame({"farmer_crop":sorted(farmer.crop_name.dropna().unique())}).assign(
        mandi_candidate=lambda x:x.farmer_crop.astype(str).str.strip().str.casefold().map(CROP_ALIASES)
    ).to_csv(C/"integration"/"crop_name_mapping_review.csv",index=False)
    pd.DataFrame({"farmer_state":sorted(farmer.state_name.dropna().unique())}).assign(
        mandi_candidate=lambda x:x.farmer_state.astype(str).str.strip().str.casefold().map(STATE_ALIASES)
    ).to_csv(C/"integration"/"state_name_mapping_review.csv",index=False)

    print("Saved:",out)
    return merged
if __name__=="__main__": build()
