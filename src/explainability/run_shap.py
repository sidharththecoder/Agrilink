from pathlib import Path
import joblib,pandas as pd,numpy as np,shap,matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2]
def explain(module, sample_path=None, max_rows=80):
    obj=joblib.load(ROOT/"models"/module/f"{module}.joblib")
    if sample_path: df=pd.read_csv(sample_path)
    elif module=="farmer": df=pd.read_csv(ROOT/"data/cleaned/farmer/crop_production_cleaned.csv").query("season != 'Total'").sample(max_rows,random_state=42)
    elif module=="demand": df=pd.read_csv(ROOT/"data/cleaned/demand/store_demand_cleaned.csv").sample(max_rows,random_state=42)
    elif module=="mandi": df=pd.read_csv(ROOT/"data/cleaned/mandi/mandi_prices_monthly_cleaned.csv").sort_values(["State","Commodity","year","month"]).copy()
    else: df=pd.read_csv(ROOT/"data/cleaned/inventory/inventory_cleaned.csv").sample(max_rows,random_state=42)
    if module=="farmer": df["year_start"]=pd.to_numeric(df["year"].astype(str).str[:4],errors="coerce")
    if module=="demand":
        df["Date"]=pd.to_datetime(df["Date"]); df["year"]=df.Date.dt.year; df["month"]=df.Date.dt.month; df["dayofweek"]=df.Date.dt.dayofweek
    if module=="mandi":
        df["lag_1"]=df.groupby(["State","Commodity"])["Modal_Price"].shift(1)
        df["lag_3_mean"]=df.groupby(["State","Commodity"])["Modal_Price"].transform(lambda s:s.shift(1).rolling(3,min_periods=1).mean())
    df=df.dropna(subset=obj["features"])
    df=df.sample(min(max_rows,len(df)),random_state=42)
    X=df[obj["features"]]
    pipe=obj["pipeline"]; Xt=pipe.named_steps["prep"].transform(X)
    if hasattr(Xt,"toarray"): Xt=Xt.toarray()
    names=pipe.named_steps["prep"].get_feature_names_out()
    tree=pipe.named_steps["rf"]; explainer=shap.TreeExplainer(tree)
    vals=explainer.shap_values(Xt, approximate=True)
    if module=="inventory" and isinstance(vals,list): vals=vals[1]
    elif module=="inventory" and getattr(vals,"ndim",0)==3: vals=vals[:,:,1]
    out=ROOT/"reports"/"shap"; out.mkdir(parents=True,exist_ok=True)
    shap.summary_plot(vals,Xt,feature_names=names,show=False,max_display=20)
    plt.tight_layout(); plt.savefig(out/f"{module}_summary.png",dpi=160,bbox_inches="tight"); plt.close()
    imp=np.abs(vals).mean(axis=0)
    pd.DataFrame({"feature":names,"mean_abs_shap":imp}).sort_values("mean_abs_shap",ascending=False).to_csv(out/f"{module}_feature_importance.csv",index=False)
    print("SHAP complete:",module)
if __name__=="__main__":
    import sys
    for name in (sys.argv[1:] or ["farmer","mandi","demand","inventory"]): explain(name)
