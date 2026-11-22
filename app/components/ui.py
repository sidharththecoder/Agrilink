import streamlit as st

PRIMARY_GREEN = "#054D3A"
CREAM = "#EAE6DF"


def theme():
    st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Manrope:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap');
    :root{--primary:#054D3A;--deep:#061B16;--cream:#EAE6DF;--muted:#A9BDB4;--lime:#A7F432;--teal:#3B8F7B;--gold:#C6A66B}
    html,body,[class*="css"]{font-family:'Manrope','DM Sans',sans-serif}
    .stApp{color:var(--cream);background:
      radial-gradient(ellipse at 12% 0%,rgba(59,143,123,.25),transparent 36%),
      radial-gradient(ellipse at 88% 22%,rgba(167,244,50,.075),transparent 27%),
      repeating-linear-gradient(118deg,rgba(255,255,255,.012) 0 1px,transparent 1px 10px),
      linear-gradient(135deg,#061B16 0%,#054D3A 48%,#031A14 100%);background-attachment:fixed}
    [data-testid="stHeader"]{background:rgba(4,30,23,.72)}
    [data-testid="stToolbar"],[data-testid="stMainMenu"],[data-testid="stDecoration"]{display:none!important}
    [data-testid="stSidebar"]{background:linear-gradient(180deg,#061B16,#03140F);border-right:1px solid rgba(234,230,223,.1)}
    [data-testid="stSidebar"] *{color:var(--cream)!important}
    [data-testid="stSidebar"] [aria-current="page"]{background:rgba(167,244,50,.13)!important;border-radius:12px}
    h1,h2,h3{color:var(--cream)!important;font-family:'Playfair Display',Georgia,serif!important;letter-spacing:-.035em}
    h1{font-size:clamp(2.6rem,5vw,4.5rem)!important;line-height:1.02!important}
    p,label,span,div{font-family:'Manrope','DM Sans',sans-serif}
    .stMarkdown p,[data-testid="stCaptionContainer"]{color:#C3D1CA}
    [data-testid="stMetric"]{background:linear-gradient(145deg,rgba(234,230,223,.13),rgba(234,230,223,.045));border:1px solid rgba(234,230,223,.15);border-radius:18px;padding:18px 20px;box-shadow:0 15px 40px rgba(0,0,0,.14)}
    [data-testid="stMetricLabel"]{color:#B8C9C0!important}[data-testid="stMetricValue"]{color:#EAE6DF!important;font-weight:800}
    [data-testid="stForm"], [data-testid="stExpander"],div[data-testid="stVerticalBlockBorderWrapper"]{background:rgba(3,27,21,.43);border:1px solid rgba(234,230,223,.15);border-radius:20px}
    .stTextInput input,.stNumberInput input,.stDateInput input,[data-baseweb="select"]>div{background:#EAE6DF!important;color:#103D30!important;border-radius:11px!important;border:1px solid rgba(5,77,58,.2)!important}
    [data-baseweb="popover"] [role="option"]{color:#103D30!important}
    .stButton>button,.stFormSubmitButton>button{background:linear-gradient(100deg,#A7F432,#C5F66C)!important;color:#10281E!important;border:0!important;border-radius:999px!important;font-weight:800!important;padding:.62rem 1.35rem!important;box-shadow:0 8px 24px rgba(167,244,50,.13);transition:transform .18s ease,box-shadow .18s ease}
    .stButton>button:hover,.stFormSubmitButton>button:hover{transform:translateY(-2px);box-shadow:0 12px 28px rgba(167,244,50,.22)}
    [data-testid="stDataFrame"]{border:1px solid rgba(234,230,223,.16);border-radius:14px;overflow:hidden}
    hr{border-color:rgba(234,230,223,.16)!important}
    [data-testid="stAlert"]{border-radius:14px}
    .eyebrow{font-size:.7rem;font-weight:800;letter-spacing:.24em;text-transform:uppercase;color:#A7F432;margin-bottom:.8rem}
    .hero-title{font-family:'Playfair Display',Georgia,serif;font-size:clamp(3.4rem,7vw,6.6rem);font-weight:800;line-height:.91;letter-spacing:-.06em;color:#EAE6DF}
    .hero-title em{font-style:normal;color:#A7F432}
    .hero-copy{font-size:1.04rem;line-height:1.8;color:#B8C9C0;max-width:640px}
    .glass-card{height:100%;padding:24px;border:1px solid rgba(234,230,223,.15);border-radius:22px;background:linear-gradient(145deg,rgba(234,230,223,.12),rgba(234,230,223,.035));box-shadow:0 18px 44px rgba(0,0,0,.12)}
    .module-kicker{font-size:.68rem;letter-spacing:.18em;font-weight:800;color:#A7F432}
    .module-title{font-family:'Playfair Display',Georgia,serif;color:#EAE6DF;font-size:1.5rem;font-weight:700;margin:.5rem 0}
    .module-copy{color:#B8C9C0;font-size:.88rem;line-height:1.65}
    .result-panel{padding:22px 24px;border-radius:18px;border:1px solid rgba(167,244,50,.25);background:linear-gradient(120deg,rgba(5,77,58,.82),rgba(59,143,123,.18))}
    </style>""", unsafe_allow_html=True)


def page_header(title, subtitle):
    theme()
    st.markdown("<div class='eyebrow'>AGRILINK &nbsp;·&nbsp; FIELD TO MARKET</div>", unsafe_allow_html=True)
    st.title(title)
    st.markdown(f"<p style='color:#B8C9C0;margin-top:-.35rem'>{subtitle}</p>", unsafe_allow_html=True)
    st.divider()


@st.cache_data(show_spinner=False)
def load_csv(path, **kwargs):
    import pandas as pd
    return pd.read_csv(path, **kwargs)


@st.cache_resource(show_spinner="Loading trained model…")
def load_model(path):
    import joblib
    return joblib.load(path)


def log_prediction(module, inputs, outputs):
    """Remember a prediction for this browser session and, if configured, save it to MySQL.

    The session copy lets other pages show the result while the app keeps running.
    The MySQL copy keeps it after a refresh or restart. The UI never fails because of the database.
    """
    import time
    st.session_state[f"last_{module}"] = {
        "module_name": module, "inputs": inputs, "outputs": outputs,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    try:
        from src.database.mysql import is_configured, save_prediction
        if is_configured():
            save_prediction(module, inputs, outputs)
    except Exception:
        # Prediction must remain available even if the optional database is offline.
        pass


def show_last_saved(module, title):
    """Show the most recent saved result for a module, so it survives page changes and refreshes."""
    record = None
    try:
        from src.database.mysql import get_latest_predictions
        rows = get_latest_predictions(module, 1)
        record = rows[0] if rows else None
    except Exception:
        record = None
    if record is None:
        record = st.session_state.get(f"last_{module}")
    if not record:
        return
    outputs = ", ".join(f"{k.replace('_', ' ')}: {v:,.2f}" if isinstance(v, (int, float)) else f"{k}: {v}"
                        for k, v in record["outputs"].items())
    st.caption(f"Last saved {title} · {record['created_at']} · {outputs}")
