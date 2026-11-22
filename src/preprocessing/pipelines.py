from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "cleaned"
CLEAN.mkdir(parents=True, exist_ok=True)

def farmer_clean():
    p = RAW/"farmer"/"crop-wise-area-production-yield.csv"
    df = pd.read_csv(p, low_memory=False)
    # Include agricultural years beginning 2001 through 2022 (2001-02 ... 2022-23).
    start = pd.to_numeric(df["year"].astype(str).str[:4], errors="coerce")
    df = df[(start >= 2001) & (start <= 2022)].copy()
    for c in ["area","production","yield"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    for c in ["state_name","district_name","crop_name","season","year"]:
        df[c] = df[c].astype("string").str.strip()
    df = df.drop_duplicates()
    # Retain original Total rows; aggregation script explicitly excludes them to avoid double counting.
    df.to_csv(CLEAN/"farmer"/"crop_production_cleaned.csv", index=False)
    return df


def mandi_clean_chunks(chunksize=400_000):
    # Build compact monthly cleaned data rather than duplicating >5 GB of daily CSV.
    out = CLEAN/"mandi"/"mandi_prices_monthly_cleaned.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    partials=[]
    for year in range(2001,2024):
        p=RAW/"mandi"/f"{year}.csv"
        if not p.exists(): raise FileNotFoundError(p)
        print(f"Processing mandi {year} ...", flush=True)
        for chunk in pd.read_csv(p, chunksize=chunksize, low_memory=False,
                                 usecols=["State","District","Market","Commodity","Variety","Grade","Arrival_Date","Min_Price","Max_Price","Modal_Price","Commodity_Code"]):
            chunk["Arrival_Date"]=pd.to_datetime(chunk["Arrival_Date"], errors="coerce", dayfirst=True)
            for c in ["Min_Price","Max_Price","Modal_Price"]:
                chunk[c]=pd.to_numeric(chunk[c],errors="coerce")
            for c in ["State","District","Market","Commodity","Variety","Grade"]:
                chunk[c]=chunk[c].astype("string").str.strip()
            chunk=chunk.dropna(subset=["Arrival_Date","Modal_Price","State","Commodity"])
            chunk=chunk[(chunk["Arrival_Date"].dt.year>=2001)&(chunk["Arrival_Date"].dt.year<=2023)&(chunk["Modal_Price"]>0)]
            if chunk.empty: continue
            chunk["year"]=chunk["Arrival_Date"].dt.year
            chunk["month"]=chunk["Arrival_Date"].dt.month
            g=chunk.groupby(["State","Commodity","year","month"],dropna=False)["Modal_Price"].agg(["sum","count","mean"]).reset_index()
            partials.append(g)
        print(f"Finished {year}; partial groups: {len(partials):,}", flush=True)
    if not partials: raise ValueError("No valid mandi records found")
    combined=pd.concat(partials,ignore_index=True)
    monthly=combined.groupby(["State","Commodity","year","month"],as_index=False).agg(
        price_sum=("sum","sum"), records=("count","sum"))
    monthly["Modal_Price"]=monthly["price_sum"]/monthly["records"]
    monthly=monthly.drop(columns=["price_sum"]).sort_values(["State","Commodity","year","month"])
    monthly.to_csv(out,index=False)
    print(f"Saved monthly mandi data: {len(monthly):,} rows -> {out}", flush=True)
    return out

def demand_clean():
    df=pd.read_csv(RAW/"demand"/"retail_store_inventory.csv")
    df["Date"]=pd.to_datetime(df["Date"],errors="coerce")
    for c in ["Inventory Level","Units Sold","Units Ordered","Price","Discount","Competitor Pricing"]:
        df[c]=pd.to_numeric(df[c],errors="coerce")
    df=df.dropna(subset=["Date","Units Sold"])
    df=df.drop_duplicates()
    # Demand Forecast intentionally excluded from model inputs due to possible target leakage.
    df.to_csv(CLEAN/"demand"/"store_demand_cleaned.csv",index=False)
    return df

def inventory_clean():
    df=pd.read_csv(RAW/"inventory"/"train.csv")
    df=df.drop(columns=["Validation"],errors="ignore")
    df=df.drop_duplicates()
    df.to_csv(CLEAN/"inventory"/"inventory_cleaned.csv",index=False)
    return df

def run_all():
    f=farmer_clean()
    d=demand_clean()
    i=inventory_clean()
    m=mandi_clean_chunks()
    return {"farmer_rows":len(f),"demand_rows":len(d),"inventory_rows":len(i),"mandi_file":str(m)}
if __name__=="__main__":
    print(run_all())
