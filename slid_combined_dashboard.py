"""
SLID — Combined Immigration Services Dashboard
Digitalization and Process Optimization of Immigration Services in Sierra Leone
Author: Millicent Iye Koiwa | MSc Business Analytics | AUB | 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import joblib
import json
import statsmodels.api as sm
from math import factorial
import warnings
warnings.filterwarnings("ignore")

# ═══════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SLID — Immigration Analytics",
    page_icon="🛂",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ═══════════════════════════════════════════════════════════
# COLOUR PALETTE — Professional, non-AI
# ═══════════════════════════════════════════════════════════
C = {
    "primary"      : "#1D3557",   # deep navy
    "secondary"    : "#457B9D",   # steel blue
    "accent"       : "#A8DADC",   # soft teal
    "highlight"    : "#E63946",   # clear red
    "success"      : "#2A9D8F",   # teal green
    "warning"      : "#E9C46A",   # warm gold
    "dark"         : "#0D1B2A",   # near black
    "light"        : "#F1FAEE",   # off white
    "mid"          : "#457B9D",
    "bg"           : "#0D1B2A",
    "card"         : "#1A2B3C",
    "border"       : "#2C3E50",
    "text"         : "#F1FAEE",
    "subtext"      : "#A8C5D8",
}

# ═══════════════════════════════════════════════════════════
# GLOBAL CSS
# ═══════════════════════════════════════════════════════════
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] {{
      font-family: 'Inter', sans-serif;
      background-color: {C['bg']};
      color: {C['text']};
  }}

  /* ── Login ── */
  .login-wrap {{
      max-width: 420px; margin: 6rem auto;
      background: {C['card']}; border-radius: 16px;
      padding: 2.5rem; border: 1px solid {C['border']};
      box-shadow: 0 8px 32px rgba(0,0,0,0.4);
  }}
  .login-logo {{ text-align:center; font-size:2.8rem; margin-bottom:0.5rem; }}
  .login-title {{ text-align:center; font-size:1.3rem; font-weight:700;
                  color:{C['text']}; margin-bottom:0.25rem; }}
  .login-sub {{ text-align:center; font-size:0.82rem; color:{C['subtext']};
                margin-bottom:1.8rem; }}

  /* ── Header ── */
  .dash-header {{
      background: linear-gradient(135deg, {C['dark']} 0%, {C['primary']} 100%);
      border-bottom: 2px solid {C['secondary']};
      padding: 1.1rem 2rem; border-radius: 12px;
      margin-bottom: 1.4rem;
      display: flex; align-items: center; gap: 1rem;
  }}
  .dash-header h1 {{ color:{C['text']}; font-size:1.45rem;
                     font-weight:700; margin:0; }}
  .dash-header p  {{ color:{C['subtext']}; font-size:0.82rem;
                     margin:0.2rem 0 0 0; }}

  /* ── Tabs ── */
  .stTabs [data-baseweb="tab-list"] {{
      gap: 4px; background: {C['card']};
      padding: 6px; border-radius: 10px;
      border: 1px solid {C['border']};
  }}
  .stTabs [data-baseweb="tab"] {{
      background: transparent; border-radius: 8px;
      color: {C['subtext']}; font-weight: 500;
      font-size: 0.85rem; padding: 0.5rem 1rem;
      border: none;
  }}
  .stTabs [aria-selected="true"] {{
      background: {C['primary']} !important;
      color: {C['text']} !important;
  }}

  /* ── KPI cards ── */
  .kpi {{
      background: {C['card']}; border-radius: 12px;
      padding: 1.1rem 1.2rem;
      border: 1px solid {C['border']};
      border-top: 3px solid {C['secondary']};
      margin-bottom: 0.8rem;
  }}
  .kpi.green  {{ border-top-color: {C['success']}; }}
  .kpi.red    {{ border-top-color: {C['highlight']}; }}
  .kpi.gold   {{ border-top-color: {C['warning']}; }}
  .kpi.teal   {{ border-top-color: {C['accent']}; }}
  .kpi-val  {{ font-size: 1.75rem; font-weight: 700;
               color: {C['text']}; margin: 0; line-height:1; }}
  .kpi-lbl  {{ font-size: 0.78rem; color: {C['subtext']};
               margin: 0.3rem 0 0 0; font-weight: 500;
               text-transform: uppercase; letter-spacing: 0.05em; }}
  .kpi-delta {{ font-size: 0.75rem; margin: 0.2rem 0 0 0; }}

  /* ── Filter bar ── */
  .filter-bar {{
      background: {C['card']}; border-radius: 10px;
      padding: 0.8rem 1rem; margin-bottom: 1.2rem;
      border: 1px solid {C['border']};
      display: flex; align-items: center; gap: 0.5rem;
  }}
  .filter-label {{ font-size:0.78rem; color:{C['subtext']};
                   font-weight:600; text-transform:uppercase;
                   letter-spacing:0.05em; white-space:nowrap; }}

  /* ── Section headers ── */
  .sec {{ font-size:0.9rem; font-weight:600; color:{C['subtext']};
          text-transform:uppercase; letter-spacing:0.07em;
          border-bottom:1px solid {C['border']}; padding-bottom:0.4rem;
          margin-bottom:0.9rem; }}

  /* ── Insight / warning boxes ── */
  .insight {{
      background: rgba(42,157,143,0.12); border-left:3px solid {C['success']};
      border-radius:6px; padding:0.7rem 1rem;
      font-size:0.82rem; color:{C['accent']};
      margin: 0.5rem 0;
  }}
  .warn {{
      background: rgba(230,57,70,0.12); border-left:3px solid {C['highlight']};
      border-radius:6px; padding:0.7rem 1rem;
      font-size:0.82rem; color:#FF8A80;
      margin: 0.5rem 0;
  }}
  .finding {{
      background: rgba(233,196,106,0.12); border-left:3px solid {C['warning']};
      border-radius:6px; padding:0.7rem 1rem;
      font-size:0.82rem; color:{C['warning']};
      margin: 0.5rem 0;
  }}

  /* ── Prediction boxes ── */
  .pred-green {{
      background:rgba(42,157,143,0.15); border:1.5px solid {C['success']};
      border-radius:12px; padding:1.2rem; text-align:center;
  }}
  .pred-gold {{
      background:rgba(233,196,106,0.15); border:1.5px solid {C['warning']};
      border-radius:12px; padding:1.2rem; text-align:center;
  }}
  .pred-red {{
      background:rgba(230,57,70,0.15); border:1.5px solid {C['highlight']};
      border-radius:12px; padding:1.2rem; text-align:center;
  }}

  /* ── Streamlit overrides ── */
  .stSelectbox>div>div, .stMultiSelect>div>div,
  .stNumberInput>div>div, .stSlider>div {{
      background: {C['card']} !important;
      border-color: {C['border']} !important;
      color: {C['text']} !important;
  }}
  .stButton>button {{
      background: {C['primary']}; color: {C['text']};
      border: 1px solid {C['secondary']}; border-radius: 8px;
      font-weight: 600; font-size: 0.88rem;
      padding: 0.55rem 1.4rem;
  }}
  .stButton>button:hover {{
      background: {C['secondary']}; border-color: {C['accent']};
  }}
  [data-testid="stSidebar"] {{ display: none !important; }}
  .block-container {{ padding: 1.5rem 2rem; max-width: 100%; }}
  div[data-testid="stMetricValue"] {{ color: {C['text']}; }}
  .stDataFrame {{ background: {C['card']}; }}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# AUTH
# ═══════════════════════════════════════════════════════════
CREDENTIALS = {"SLID": "SLID2026"}

def login():
    st.markdown(f"""
    <div class="login-wrap">
      <div class="login-logo">🛂</div>
      <div class="login-title">SLID Analytics Dashboard</div>
      <div class="login-sub">Sierra Leone Immigration Department<br>
           Authorized Access Only</div>
    </div>""", unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1,2,1])
    with col_c:
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password",
                                     placeholder="Enter password")
            submitted = st.form_submit_button("Sign In",
                                              use_container_width=True)
            if submitted:
                if username in CREDENTIALS and \
                   CREDENTIALS[username] == password:
                    st.session_state["auth"] = True
                    st.session_state["user"] = username
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
        st.markdown(
            f'<p style="text-align:center;font-size:0.75rem;'
            f'color:{C["subtext"]};margin-top:1rem;">'
            f'Digitalization & Process Optimization Initiative<br>'
            f'MSc Business Analytics — AUB 2026</p>',
            unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    login()
    st.stop()

# ═══════════════════════════════════════════════════════════
# PLOTLY THEME
# ═══════════════════════════════════════════════════════════
LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor ="rgba(0,0,0,0)",
    font=dict(family="Inter", color=C["subtext"], size=12),
    margin=dict(l=0, r=0, t=30, b=0),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=C["subtext"])),
)

def ax(fig):
    """Apply consistent axis styling."""
    fig.update_xaxes(gridcolor=C["border"], linecolor=C["border"],
                     tickfont=dict(color=C["subtext"]))
    fig.update_yaxes(gridcolor=C["border"], linecolor=C["border"],
                     tickfont=dict(color=C["subtext"]))
    return fig
PALETTE = [C["secondary"], C["success"], C["warning"],
           C["highlight"], C["accent"], "#8ECAE6",
           "#FB8500", "#023047", "#219EBC"]

def apply_theme(fig, h=400):
    fig.update_layout(**LAYOUT, height=h)
    return fig

# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════
def kpi(label, value, color="", delta=None):
    delta_html = ""
    if delta:
        clr = C["success"] if "▲" in str(delta) else C["highlight"]
        delta_html = f'<p class="kpi-delta" style="color:{clr}">{delta}</p>'
    st.markdown(f"""
    <div class="kpi {color}">
      <p class="kpi-val">{value}</p>
      <p class="kpi-lbl">{label}</p>
      {delta_html}
    </div>""", unsafe_allow_html=True)

def sec(title):
    st.markdown(f'<p class="sec">{title}</p>', unsafe_allow_html=True)

def insight(txt):
    st.markdown(f'<div class="insight">💡 {txt}</div>',
                unsafe_allow_html=True)

def warn(txt):
    st.markdown(f'<div class="warn">⚠ {txt}</div>',
                unsafe_allow_html=True)

def finding(txt):
    st.markdown(f'<div class="finding">📌 {txt}</div>',
                unsafe_allow_html=True)

def mms(lam, mu, s):
    rho = lam / (s * mu)
    if rho >= 1:
        return {"rho":rho,"stable":False,"W":None,"Lq":None}
    terms = sum([(s*rho)**n/factorial(n) for n in range(s)])
    last  = (s*rho)**s/(factorial(s)*(1-rho))
    P0    = 1/(terms+last)
    Lq    = (P0*(lam/mu)**s*rho)/(factorial(s)*(1-rho)**2)
    Wq    = Lq/lam
    W     = Wq+1/mu
    return {"rho":round(rho,4),"stable":True,
            "W":round(W,4),"Lq":round(Lq,4)}

# ═══════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════
@st.cache_data
def load_rp():
    df = pd.read_excel("SLID_Residency_Final_Cleaned.xlsx",
                       engine="openpyxl")
    df["Date of Creation"] = pd.to_datetime(
        df["Date of Creation"], errors="coerce")
    df["Card Expiry Date"] = pd.to_datetime(
        df["Card Expiry Date"], errors="coerce")
    for col, expr in [
        ("Month",    lambda d: d["Date of Creation"].dt.to_period("M").astype(str)),
        ("Month_Num",lambda d: d["Date of Creation"].dt.month),
        ("Day_of_Week",lambda d: d["Date of Creation"].dt.day_name()),
        ("DOW_Num",  lambda d: d["Date of Creation"].dt.dayofweek),
        ("Days_to_Expiry", lambda d:(d["Card Expiry Date"]-d["Date of Creation"]).dt.days),
        ("Card_Issued",    lambda d: d["Card Number"].notna().astype(int)),
    ]:
        if col not in df.columns:
            df[col] = expr(df)
    if "Completion" not in df.columns:
        df["Completion"] = np.where(df["Status"]==7,"Delivered","Not Delivered")
    if "Completion_Binary" not in df.columns:
        df["Completion_Binary"] = (df["Completion"]=="Delivered").astype(int)
    if "Status_Name" not in df.columns:
        smap = {1:"Draft",2:"New",3:"Appointment Needed",
                5:"Printed",6:"Ready To Pickup",7:"Delivered",
                8:"Expired",11:"Rejected",15:"Need Extra Document",
                19:"Needs Edit"}
        df["Status_Name"] = df["Status"].map(smap).fillna("Other")
    return df

@st.cache_resource
def load_models():
    try:
        lr  = joblib.load("slid_logistic_model.joblib")
        sc  = joblib.load("slid_scaler.joblib")
        lec = joblib.load("slid_le_category.joblib")
        lep = joblib.load("slid_le_process.joblib")
        km  = joblib.load("slid_kmeans_model.joblib")
        ks  = joblib.load("slid_kscaler.joblib")
        with open("slid_feature_meta.json") as f:
            meta = json.load(f)
        with open("slid_ols_params.json") as f:
            ols_p = json.load(f)
        return lr,sc,lec,lep,km,ks,meta,ols_p,True
    except:
        return None,None,None,None,None,None,{},{},False

@st.cache_data
def load_pp():
    pp = pd.DataFrame({
        "Month":["Jan","Feb","Mar","Apr","May","Jun","Jul"],
        "MF":["2026-01","2026-02","2026-03","2026-04",
              "2026-05","2026-06","2026-07"],
        "Mn":[1,2,3,4,5,6,7],
        "Ordinary":[5894,6370,5094,5468,4102,4754,6685],
        "Service" :[55,103,108,10,7,8,83],
        "Diplomatic":[15,25,30,27,16,32,17],
        "Total":[5964,6498,5232,5505,4125,4794,6785],
        "WD":[26,25,27,26,27,26,27],
    })
    pp["Revenue"]   = pp["Ordinary"]*100+pp["Service"]*100
    pp["DailyRate"] = (pp["Total"]/pp["WD"]).round(1)
    pp["MoM"]       = pp["Total"].diff()
    office = pd.DataFrame({
        "Office":["Freetown","Makeni","Kenema","Online","Bo"],
        "Total" :[38195,279,170,130,129],
        "Pct"   :[98.18,0.72,0.44,0.33,0.33],
        "Lat"   :[8.484,8.879,7.876,8.484,7.965],
        "Lon"   :[-13.234,-12.059,-11.190,-13.234,-11.738],
    })
    return pp, office

df = load_rp()
pp, office = load_pp()
lr_model,scaler,le_cat,le_proc,km_model,kscaler,meta,ols_p,models_ok = load_models()

# ═══════════════════════════════════════════════════════════
# HEADER + LOGOUT
# ═══════════════════════════════════════════════════════════
hc1, hc2 = st.columns([9,1])
with hc1:
    st.markdown(f"""
    <div class="dash-header">
      <div>
        <h1>🛂 Sierra Leone Immigration Department — Analytics Dashboard</h1>
        <p>Passport Production (Jan–Jul 2026) &nbsp;·&nbsp;
           Residency Permit Applications (Jan–Aug 2026) &nbsp;·&nbsp;
           Digitalization & Process Optimization Initiative</p>
      </div>
    </div>""", unsafe_allow_html=True)
with hc2:
    if st.button("Sign Out"):
        st.session_state["auth"] = False
        st.rerun()

# ═══════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════
tabs = st.tabs([
    "📊  Overview",
    "🛂  Passport",
    "📋  Residency Permit",
    "⚙️  Process Performance",
    "💰  Revenue Forecast",
    "🔮  Predictive Analytics",
])

# ──────────────────────────────────────────────────────────
# TAB 1 — OVERVIEW
# ──────────────────────────────────────────────────────────
with tabs[0]:
    # Filters
    with st.expander("🔽  Filters", expanded=False):
        fc1,fc2 = st.columns(2)
        with fc1:
            all_months = sorted(df["Month"].dropna().unique())
            sel_months = st.multiselect("Residency Permit Month",
                all_months, default=all_months, key="ov_m")
        with fc2:
            pp_months = pp["Month"].tolist()
            sel_pp = st.multiselect("Passport Month",
                pp_months, default=pp_months, key="ov_pp")

    fdf = df[df["Month"].isin(sel_months)]
    fpp = pp[pp["Month"].isin(sel_pp)]

    # KPIs
    k1,k2,k3,k4,k5,k6 = st.columns(6)
    with k1: kpi("Passports Produced", f"{fpp['Total'].sum():,}", "teal")
    with k2: kpi("Permit Applications", f"{len(fdf):,}", "")
    with k3:
        dr = (fdf["Completion"]=="Delivered").mean()*100
        kpi("Permit Delivery Rate", f"{dr:.1f}%",
            "green" if dr>70 else "red")
    with k4: kpi("Passport Revenue (Est.)",
                 f"${fpp['Revenue'].sum()/1e6:.2f}M", "gold")
    with k5: kpi("Permit Revenue",
                 f"${fdf['Amount ($)'].sum()/1e6:.2f}M", "gold")
    with k6:
        tot = fpp["Revenue"].sum()+fdf["Amount ($)"].sum()
        kpi("Combined Revenue", f"${tot/1e6:.2f}M", "green")

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)

    with c1:
        sec("Monthly Volume — Passport vs Residency Permit")
        rp_m = fdf.groupby("Month").size().reset_index(name="Apps")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=fpp["MF"], y=fpp["Total"], name="Passport",
            mode="lines+markers",
            line=dict(color=C["secondary"],width=2.5),
            marker=dict(size=7),
            fill="tozeroy",fillcolor="rgba(69,123,157,0.12)"))
        fig.add_trace(go.Scatter(
            x=rp_m["Month"], y=rp_m["Apps"], name="Residency Permit",
            mode="lines+markers",
            line=dict(color=C["success"],width=2.5),
            marker=dict(size=7),
            fill="tozeroy",fillcolor="rgba(42,157,143,0.12)"))
        fig.update_layout(**LAYOUT, height=360,
            legend=dict(orientation="h",y=1.12,
                        bgcolor="rgba(0,0,0,0)",
                        font=dict(color=C["subtext"])))
        fig.update_xaxes(title_text="Month",
                         title_font=dict(color=C["subtext"]))
        fig.update_yaxes(title_text="Volume",
                         title_font=dict(color=C["subtext"]))
        ax(fig)
        st.plotly_chart(fig, use_container_width=True)
        insight("Passport volumes are 5–10× higher than permit applications, reflecting Sierra Leone's broader citizen travel demand versus foreign national residency.")

    with c2:
        sec("Monthly Revenue — Passport vs Residency Permit")
        rp_rev = fdf.groupby("Month")["Amount ($)"].sum().reset_index()
        rp_rev.columns = ["Month","Revenue"]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=fpp["MF"], y=fpp["Revenue"], name="Passport (Est.)",
            marker_color=C["secondary"], opacity=0.85,
            text=fpp["Revenue"].apply(lambda x:f"${x/1e6:.2f}M"),
            textposition="inside",
            textfont=dict(color="white",size=10)))
        fig2.add_trace(go.Bar(
            x=rp_rev["Month"], y=rp_rev["Revenue"],
            name="Residency Permit",
            marker_color=C["success"], opacity=0.85,
            text=rp_rev["Revenue"].apply(lambda x:f"${x/1e6:.2f}M"),
            textposition="inside",
            textfont=dict(color="white",size=10)))
        fig2.update_layout(**LAYOUT, height=360, barmode="group",
            legend=dict(orientation="h",y=1.12,
                        bgcolor="rgba(0,0,0,0)",
                        font=dict(color=C["subtext"])))
        fig2.update_yaxes(tickformat="$,.0f",
                          title_text="Revenue (USD)",
                          title_font=dict(color=C["subtext"]))
        fig2.update_xaxes(title_text="Month",
                          title_font=dict(color=C["subtext"]))
        ax(fig2)
        st.plotly_chart(fig2, use_container_width=True)
        insight("Passport revenue dominates month-on-month due to volume. Residency permit revenue shows a stronger growth trajectory through June 2026.")

    st.markdown("<br>", unsafe_allow_html=True)
    c3,c4 = st.columns(2)

    with c3:
        sec("Revenue Split — Passport vs Residency Permit")
        fig3 = go.Figure(go.Pie(
            labels=["Passport (Est.)","Residency Permit"],
            values=[fpp["Revenue"].sum(), fdf["Amount ($)"].sum()],
            hole=0.55,
            marker_colors=[C["secondary"],C["success"]],
            textinfo="label+percent",
            textfont=dict(color="white",size=12),
        ))
        fig3.update_layout(**LAYOUT,height=320,showlegend=False)
        ax(fig3)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        sec("Service Delivery Scorecard")
        scorecard = pd.DataFrame({
            "Metric":["Passport Production Rate","Permit Delivery Rate",
                      "Online Channel Adoption","Freetown Concentration",
                      "Processing Time vs Target"],
            "Current":["212/day","74.7%","0.33%","98.18%","~14 days"],
            "Target" :["Sustained","≥95%","≥20%","≤70%","3 days"],
            "Status" :["✅","⚠️","❌","❌","❌"]
        })
        st.dataframe(scorecard, use_container_width=True,
                     hide_index=True)
        warn("Three of five service delivery metrics are off-target. Online adoption and geographic decentralisation are the most urgent gaps.")

# ──────────────────────────────────────────────────────────
# TAB 2 — PASSPORT
# ──────────────────────────────────────────────────────────
with tabs[1]:
    with st.expander("🔽  Filters", expanded=False):
        pp_months_all = pp["Month"].tolist()
        sel_pp2 = st.multiselect("Passport Month", pp_months_all,
                                 default=pp_months_all, key="pp_m2")
    fpp2 = pp[pp["Month"].isin(sel_pp2)]

    k1,k2,k3,k4,k5 = st.columns(5)
    with k1: kpi("Total Produced",f"{fpp2['Total'].sum():,}","teal")
    with k2: kpi("Ordinary",f"{fpp2['Ordinary'].sum():,}","")
    with k3: kpi("Service",f"{fpp2['Service'].sum():,}","gold")
    with k4: kpi("Diplomatic (Exempt)",f"{fpp2['Diplomatic'].sum():,}","")
    with k5: kpi("Est. Revenue",f"${fpp2['Revenue'].sum():,.0f}","green")

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)

    with c1:
        sec("Monthly Production Trend by Passport Type")
        fig = go.Figure()
        for ptype,col in [("Ordinary",C["secondary"]),
                          ("Service",C["success"]),
                          ("Diplomatic",C["warning"])]:
            fig.add_trace(go.Scatter(
                x=fpp2["MF"], y=fpp2[ptype],
                name=ptype, mode="lines+markers",
                line=dict(color=col,width=2.5),
                marker=dict(size=8)))
        fig.update_layout(**LAYOUT,height=380,
            legend=dict(orientation="h",y=1.12,
                        bgcolor="rgba(0,0,0,0)",
                        font=dict(color=C["subtext"])))
        fig.update_yaxes(title_text="Passports Produced",
                         title_font=dict(color=C["subtext"]))
        ax(fig)
        st.plotly_chart(fig, use_container_width=True)
        warn("Service passport production collapsed 96% between March (108) and May (7). This anomaly is unexplained and requires investigation with SLID.")

    with c2:
        sec("Passport Type — Volume & Revenue Share")
        td = pd.DataFrame({
            "Type":["Ordinary","Service","Diplomatic"],
            "Vol" :[fpp2["Ordinary"].sum(),fpp2["Service"].sum(),
                    fpp2["Diplomatic"].sum()],
            "Rev" :[fpp2["Ordinary"].sum()*100,
                    fpp2["Service"].sum()*100, 0]
        })
        fig2 = make_subplots(1,2,
            subplot_titles=["Volume Share","Revenue Share"],
            specs=[[{"type":"pie"},{"type":"pie"}]])
        for i,(col_name,colors) in enumerate([
            ("Vol",[C["secondary"],C["success"],C["warning"]]),
            ("Rev",[C["secondary"],C["success"],C["warning"]])
        ]):
            fig2.add_trace(go.Pie(
                labels=td["Type"],values=td[col_name],
                hole=0.5,textinfo="label+percent",
                marker_colors=colors,
                textfont=dict(color="white",size=11)),
                row=1,col=i+1)
        fig2.update_layout(**LAYOUT,height=380,showlegend=False)
        for ann in fig2.layout.annotations:
            ann.font.color = C["subtext"]
        ax(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c3,c4 = st.columns(2)

    with c3:
        sec("Month-over-Month Production Change")
        mom = fpp2.dropna(subset=["MoM"]).copy()
        fig3 = go.Figure(go.Bar(
            x=mom["MF"],
            y=mom["MoM"],
            text=mom["MoM"].apply(lambda x:f"{x:+,.0f}"),
            textposition="outside",
            textfont=dict(color=C["subtext"]),
            marker_color=[C["success"] if v>=0 else C["highlight"]
                          for v in mom["MoM"]]))
        fig3.add_hline(y=0,line_color=C["border"],line_width=1)
        fig3.update_layout(**LAYOUT,height=340,showlegend=False)
        fig3.update_yaxes(title_text="Change in Volume",
                          title_font=dict(color=C["subtext"]))
        ax(fig3)
        st.plotly_chart(fig3, use_container_width=True)
        insight(f"Highest single-month gain: July (+{int(pp['MoM'].max()):,}). Steepest decline: May ({int(pp['MoM'].min()):,}). No consistent trend — demand is highly variable.")

    with c4:
        sec("Daily Production Rate by Month")
        fig4 = go.Figure(go.Scatter(
            x=fpp2["MF"], y=fpp2["DailyRate"],
            mode="lines+markers+text",
            line=dict(color=C["secondary"],width=2.5),
            marker=dict(size=10,color=C["secondary"]),
            text=fpp2["DailyRate"].apply(lambda x:f"{x:.0f}/day"),
            textposition="top center",
            textfont=dict(color=C["subtext"],size=11)))
        fig4.add_hline(
            y=fpp2["DailyRate"].mean(),
            line_dash="dash",line_color=C["warning"],
            annotation_text=f"Avg {fpp2['DailyRate'].mean():.0f}/day",
            annotation_font_color=C["warning"])
        fig4.update_layout(**LAYOUT,height=340)
        fig4.update_yaxes(title_text="Passports per Working Day",
                          title_font=dict(color=C["subtext"]))
        ax(fig4)
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    sec("Geographic Distribution of Passport Production — Sierra Leone")
    cm1,cm2 = st.columns([3,2])

    with cm1:
        fig5 = px.scatter_geo(
            office, lat="Lat", lon="Lon",
            size="Total", color="Office",
            hover_name="Office",
            hover_data={"Total":True,"Pct":True,
                        "Lat":False,"Lon":False},
            size_max=55,
            color_discrete_sequence=PALETTE,
            projection="natural earth")
        fig5.update_geos(
            visible=True,
            resolution=50,
            showcountries=True, countrycolor=C["border"],
            showcoastlines=True, coastlinecolor=C["border"],
            showland=True, landcolor="#1A2B3C",
            showocean=True, oceancolor="#0D1B2A",
            showlakes=False,
            center={"lat":8.5,"lon":-11.8},
            lataxis_range=[6.5,10.5],
            lonaxis_range=[-14.5,-10.0],
        )
        fig5.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color=C["subtext"], size=12),
            margin=dict(l=0, r=0, t=30, b=0),
            legend=dict(bgcolor="rgba(0,0,0,0)",
                        font=dict(color=C["subtext"])),
            height=420,
            geo_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig5, use_container_width=True)

    with cm2:
        sec("Production by Office")
        fig6 = go.Figure(go.Bar(
            x=office.sort_values("Total")["Total"],
            y=office.sort_values("Total")["Office"],
            orientation="h",
            text=office.sort_values("Total")["Pct"].apply(
                lambda x:f"{x:.2f}%"),
            textposition="outside",
            textfont=dict(color=C["subtext"]),
            marker_color=PALETTE[:5]))
        fig6.update_layout(**LAYOUT,height=320,showlegend=False)
        fig6.update_xaxes(title_text="Passports Produced",
                          title_font=dict(color=C["subtext"]))
        ax(fig6)
        st.plotly_chart(fig6, use_container_width=True)
        warn("Freetown handles 98.18% of all production — a critical single point of failure. Any disruption in Freetown halts the entire national passport system.")
        finding("Online channel: only 130 passports (0.33%) despite the digitalization mandate — indicating negligible digital adoption.")

# ──────────────────────────────────────────────────────────
# TAB 3 — RESIDENCY PERMIT
# ──────────────────────────────────────────────────────────
with tabs[2]:
    with st.expander("🔽  Filters", expanded=False):
        rc1,rc2 = st.columns(2)
        with rc1:
            all_m3 = sorted(df["Month"].dropna().unique())
            sel_m3 = st.multiselect("Month", all_m3,
                                    default=all_m3, key="rp_m3")
        with rc2:
            all_c3 = ["All"]+sorted(df["Category"].dropna().unique())
            sel_c3 = st.selectbox("Category", all_c3, key="rp_c3")

    fdf3 = df[df["Month"].isin(sel_m3)]
    if sel_c3 != "All":
        fdf3 = fdf3[fdf3["Category"]==sel_c3]

    k1,k2,k3,k4,k5 = st.columns(5)
    with k1: kpi("Total Applications",f"{len(fdf3):,}","")
    with k2:
        dr3 = (fdf3["Completion"]=="Delivered").mean()*100
        kpi("Delivery Rate",f"{dr3:.1f}%",
            "green" if dr3>70 else "red")
    with k3:
        nd3 = (fdf3["Completion"]=="Not Delivered").sum()
        kpi("Not Delivered",f"{nd3:,}","red")
    with k4: kpi("Total Revenue",
                 f"${fdf3['Amount ($)'].sum():,.0f}","gold")
    with k5: kpi("Average Fee",
                 f"${fdf3['Amount ($)'].mean():,.0f}","")

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)

    with c1:
        sec("Monthly Volume & Revenue (Dual Axis)")
        m3 = fdf3.groupby("Month").agg(
            Apps=("Receipt Code","count"),
            Rev=("Amount ($)","sum")).reset_index()
        fig = make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(
            x=m3["Month"],y=m3["Apps"],name="Applications",
            marker_color=C["secondary"],opacity=0.85,
            text=m3["Apps"],textposition="outside",
            textfont=dict(color=C["subtext"],size=10)),
            secondary_y=False)
        fig.add_trace(go.Scatter(
            x=m3["Month"],y=m3["Rev"],name="Revenue ($)",
            mode="lines+markers",
            line=dict(color=C["warning"],width=2.5),
            marker=dict(size=8,color=C["warning"])),
            secondary_y=True)
        fig.update_layout(**LAYOUT,height=380,
            legend=dict(orientation="h",y=1.12,
                        bgcolor="rgba(0,0,0,0)",
                        font=dict(color=C["subtext"])))
        fig.update_yaxes(title_text="Applications",
            title_font=dict(color=C["subtext"]),secondary_y=False,
            gridcolor=C["border"])
        fig.update_yaxes(title_text="Revenue ($)",
            tickformat="$,.0f",
            title_font=dict(color=C["subtext"]),secondary_y=True,
            gridcolor="rgba(0,0,0,0)")
        ax(fig)
        st.plotly_chart(fig, use_container_width=True)
        insight("June 2026 was peak month for both volume (2,634 applications) and revenue ($1.49M) — driven by annual permit renewals concentrated in Q2.")

    with c2:
        sec("Application Status Distribution")
        sd = fdf3["Status_Name"].value_counts().reset_index()
        sd.columns = ["Status","Count"]
        colors_sd = [C["success"] if s=="Delivered"
                     else C["highlight"] if s in ["Rejected","Expired"]
                     else C["secondary"] for s in sd["Status"]]
        fig2 = go.Figure(go.Bar(
            x=sd["Count"],y=sd["Status"],orientation="h",
            text=sd["Count"],textposition="outside",
            textfont=dict(color=C["subtext"],size=10),
            marker_color=colors_sd))
        fig2.update_layout(**LAYOUT,height=380,showlegend=False)
        fig2.update_xaxes(title_text="Count",
                          title_font=dict(color=C["subtext"]))
        ax(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c3,c4 = st.columns(2)

    with c3:
        sec("Applications & Revenue by Category")
        cs = fdf3.groupby("Category",dropna=False).agg(
            Count=("Receipt Code","count"),
            Revenue=("Amount ($)","sum"),
            AvgFee=("Amount ($)","mean"),
            DR=("Completion_Binary","mean")).reset_index()
        cs["Category"] = cs["Category"].fillna("Unknown")
        cs["DR"] = (cs["DR"]*100).round(1)

        fig3 = make_subplots(2,1,
            subplot_titles=["Applications by Category",
                            "Revenue by Category ($)"],
            vertical_spacing=0.18)
        fig3.add_trace(go.Bar(
            x=cs["Category"],y=cs["Count"],
            marker_color=C["secondary"],
            text=cs["Count"],textposition="outside",
            textfont=dict(color=C["subtext"],size=10),
            name="Applications"),row=1,col=1)
        fig3.add_trace(go.Bar(
            x=cs["Category"],y=cs["Revenue"],
            marker_color=C["success"],
            text=cs["Revenue"].apply(lambda x:f"${x:,.0f}"),
            textposition="outside",
            textfont=dict(color=C["subtext"],size=10),
            name="Revenue"),row=2,col=1)
        fig3.update_layout(**LAYOUT,height=560,showlegend=False)
        for ann in fig3.layout.annotations:
            ann.font.color = C["subtext"]
        ax(fig3)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        sec("Delivery Rate & Average Fee by Category")
        fig4 = make_subplots(2,1,
            subplot_titles=["Delivery Rate (%)",
                            "Average Fee ($)"],
            vertical_spacing=0.18)
        bar_colors = [C["success"] if v>80
                      else C["warning"] if v>50
                      else C["highlight"] for v in cs["DR"]]
        fig4.add_trace(go.Bar(
            x=cs["Category"],y=cs["DR"],
            marker_color=bar_colors,
            text=cs["DR"].apply(lambda x:f"{x:.1f}%"),
            textposition="outside",
            textfont=dict(color=C["subtext"],size=10),
            name="Delivery Rate"),row=1,col=1)
        fig4.add_hline(y=74.7,line_dash="dash",
                       line_color=C["warning"],row=1,col=1,
                       annotation_text="Overall 74.7%",
                       annotation_font_color=C["warning"])
        fig4.add_trace(go.Bar(
            x=cs["Category"],y=cs["AvgFee"],
            marker_color=C["warning"],
            text=cs["AvgFee"].apply(lambda x:f"${x:,.0f}"),
            textposition="outside",
            textfont=dict(color=C["subtext"],size=10),
            name="Avg Fee"),row=2,col=1)
        fig4.update_layout(**LAYOUT,height=560,showlegend=False)
        for ann in fig4.layout.annotations:
            ann.font.color = C["subtext"]
        ax(fig4)
        st.plotly_chart(fig4, use_container_width=True)
        insight("Category B (General Merchandise) generates the highest total revenue and has the highest average fee at $709. Category D (Dependants) has the lowest at $213.")

    st.markdown("<br>", unsafe_allow_html=True)
    c5,c6 = st.columns(2)

    with c5:
        sec("Applications by Day of Week")
        day_order=["Monday","Tuesday","Wednesday",
                   "Thursday","Friday","Saturday"]
        dow = fdf3["Day_of_Week"].value_counts()\
              .reindex(day_order).dropna().reset_index()
        dow.columns=["Day","Count"]
        fig5 = go.Figure(go.Bar(
            x=dow["Day"],y=dow["Count"],
            text=dow["Count"],textposition="outside",
            textfont=dict(color=C["subtext"],size=10),
            marker_color=[C["secondary"] if d!="Tuesday"
                          else C["highlight"] for d in dow["Day"]]))
        fig5.update_layout(**LAYOUT,height=340,showlegend=False)
        fig5.update_yaxes(title_text="Applications",
                          title_font=dict(color=C["subtext"]))
        st.plotly_chart(fig5, use_container_width=True)
        insight("Monday is the busiest day. Tuesday shows an unexpectedly low volume — a potential data anomaly worth raising with SLID.")

    with c6:
        sec("Applicant Segments — K-Means Cluster Analysis")
        cl = pd.DataFrame({
            "Cluster":["Cluster 0","Cluster 1","Cluster 2","Cluster 3"],
            "Size"   :[2934,6104,1649,373],
            "AvgFee" :[225,709,744,0],
            "DR"     :[67,100,0,47],
        })
        fig6 = go.Figure()
        for i,row in cl.iterrows():
            fig6.add_trace(go.Scatter(
                x=[row["AvgFee"]],y=[row["DR"]],
                mode="markers+text",
                marker=dict(size=row["Size"]/60,
                            color=PALETTE[i],opacity=0.85,
                            line=dict(color="white",width=1.5)),
                text=[row["Cluster"]],
                textposition="top center",
                textfont=dict(color=C["subtext"],size=11),
                name=row["Cluster"],
                hovertemplate=(
                    f"<b>{row['Cluster']}</b><br>"
                    f"Size: {row['Size']:,}<br>"
                    f"Avg Fee: ${row['AvgFee']}<br>"
                    f"Delivery Rate: {row['DR']}%"
                    "<extra></extra>")))
        fig6.update_layout(**LAYOUT,height=340,showlegend=False)
        fig6.update_xaxes(title_text="Average Fee ($)",
                          title_font=dict(color=C["subtext"]))
        fig6.update_yaxes(title_text="Delivery Rate (%)",
                          title_font=dict(color=C["subtext"]))
        ax(fig6)
        st.plotly_chart(fig6, use_container_width=True)
        warn("Cluster 2 — 1,649 high-fee applications ($744 avg) with 0% delivery. These applicants paid in full but their permits were never issued. This represents $1.23M in revenue collected but undelivered — a critical operational backlog concentrated in June and July 2026.")

# ──────────────────────────────────────────────────────────
# TAB 4 — PROCESS PERFORMANCE
# ──────────────────────────────────────────────────────────
with tabs[3]:
    sec("M/M/s Queuing Model — Real-Time Capacity Check")
    pc1,pc2,pc3 = st.columns(3)
    with pc1:
        lam = st.number_input("Daily applications (λ)",1,400,51,1,
                              key="pp_lam")
    with pc2:
        s_in = st.number_input("Officers available (s)",1,20,3,1,
                               key="pp_s")
    with pc3:
        mu_in = st.number_input("Applications/officer/day (μ)",1,50,5,1,
                                key="pp_mu")

    m = mms(lam, mu_in, s_in)
    if m["stable"]:
        st.markdown(f"""
        <div class="pred-green">
          <h3>🟢 SYSTEM STABLE</h3>
          <p style="color:{C['accent']};">
          Server utilisation: <b>{m['rho']*100:.1f}%</b> &nbsp;·&nbsp;
          Processing time: <b>{m['W']:.3f} days
          ({m['W']*8:.1f} hrs)</b> &nbsp;·&nbsp;
          Avg queue: <b>{m['Lq']:.1f} applications</b></p>
        </div>""", unsafe_allow_html=True)
    else:
        cap   = s_in*mu_in
        extra = int(np.ceil((lam-cap)/mu_in))
        st.markdown(f"""
        <div class="pred-red">
          <h3>🔴 SYSTEM OVERLOADED — Queue grows indefinitely</h3>
          <p style="color:#FF8A80;">
          Capacity: <b>{cap}/day</b> &nbsp;·&nbsp;
          Demand: <b>{lam}/day</b> &nbsp;·&nbsp;
          Add at least <b>{extra} more officer(s)</b>
          or defer {lam-cap:.0f} applications.</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    c1,c2 = st.columns(2)

    with c1:
        sec("AS-IS vs TO-BE Processing Time Across All Demand Scenarios")
        demands = {"Jan\n(Low)":11.62,"Feb":37.96,"Mar":37.93,
                   "Apr":55.43,"May":68.26,"Jun\n(Peak)":87.80,
                   "Jul":52.87,"Aug":42.67}
        scenarios = {
            "AS-IS (s=3, μ=5)"        :(3,5,  C["highlight"]),
            "Min Viable (s=6, μ=15)"  :(6,15, C["warning"]),
            "Recommended (s=8, μ=12)" :(8,12, C["secondary"]),
            "Optimal (s=10, μ=10)"    :(10,10,C["success"]),
        }
        fig = go.Figure()
        for label,(sc,mu_v,col) in scenarios.items():
            W_vals=[mms(lv,mu_v,sc)["W"]
                    if mms(lv,mu_v,sc)["stable"] else None
                    for lv in demands.values()]
            fig.add_trace(go.Scatter(
                x=list(demands.keys()),y=W_vals,
                mode="lines+markers",name=label,
                line=dict(color=col,width=2.5),
                marker=dict(size=8,color=col),
                connectgaps=False))
        fig.add_hline(y=1.0,line_dash="dash",
                      line_color=C["accent"],
                      annotation_text="1-day internal target",
                      annotation_font_color=C["accent"])
        fig.add_hline(y=3.0,line_dash="dot",
                      line_color=C["subtext"],
                      annotation_text="3-day overall target",
                      annotation_font_color=C["subtext"])
        fig.update_layout(**LAYOUT,height=420,
            legend=dict(orientation="h",y=1.12,
                        bgcolor="rgba(0,0,0,0)",
                        font=dict(color=C["subtext"])))
        fig.update_yaxes(title_text="Total Days in System (W)",
                         title_font=dict(color=C["subtext"]),
                         range=[0,6])
        fig.update_xaxes(title_text="Month",
                         title_font=dict(color=C["subtext"]))
        ax(fig)
        st.plotly_chart(fig, use_container_width=True)
        insight("The recommended configuration (s=8, μ=12) remains stable across all demand scenarios including the June peak of 87.80 applications per day — the only configuration that achieves this.")

    with c2:
        sec(f"Sensitivity Analysis — Processing Time (days) | λ={lam}/day")
        server_range=list(range(3,14))
        mu_range=[5,8,10,12,15,20]
        heat=[]
        for sc in server_range:
            row={"Servers":sc}
            for mv in mu_range:
                res=mms(lam,mv,sc)
                row[f"μ={mv}"]=round(res["W"],3) if res["stable"] else None
            heat.append(row)
        hdf=pd.DataFrame(heat).set_index("Servers")
        fig2=px.imshow(hdf,text_auto=".2f",aspect="auto",
                       color_continuous_scale="RdYlGn_r",
                       labels={"x":"Service Rate (μ)",
                               "y":"Servers","color":"Days"})
        fig2.update_layout(**LAYOUT,height=420)
        fig2.update_coloraxes(
            colorbar_tickfont_color=C["subtext"],
            colorbar_title_font_color=C["subtext"])
        ax(fig2)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    sec("Configuration Summary")
    rows=[]
    for label,(sc,mu_v,_) in scenarios.items():
        am=mms(50.77,mu_v,sc)
        pm=mms(87.80,mu_v,sc)
        rows.append({
            "Scenario":label,"Servers":sc,"μ":mu_v,
            "Avg W (days)":f"{am['W']:.4f}" if am["stable"] else "UNSTABLE",
            "Peak W (days)":f"{pm['W']:.4f}" if pm["stable"] else "UNSTABLE",
            "Feasible":"✅" if am["stable"] and pm["stable"] else "❌"
        })
    st.dataframe(pd.DataFrame(rows),
                 use_container_width=True,hide_index=True)
    finding("The primary lever for improvement is not headcount alone — it is service rate (μ). Digitising identity verification (NCRA API integration) is the single highest-impact technical intervention available to SLID.")

# ──────────────────────────────────────────────────────────
# TAB 5 — REVENUE FORECAST
# ──────────────────────────────────────────────────────────
with tabs[4]:
    c1,c2 = st.columns(2)

    with c1:
        sec("Residency Permit — OLS Linear Trend Forecast (Sep–Dec 2026)")
        rm = df.groupby("Month")["Amount ($)"].sum().reset_index()
        rm.columns = ["Month","Revenue"]
        rm["MI"] = np.arange(1,len(rm)+1)
        md = rm.iloc[:7].copy()
        X  = sm.add_constant(md["MI"])
        y  = md["Revenue"]
        ols = sm.OLS(y,X).fit()
        fut = pd.DataFrame({"Month":["2026-09","2026-10","2026-11","2026-12"],
                            "MI":[9,10,11,12]})
        fX  = sm.add_constant(fut["MI"],has_constant="add")
        pred= ols.get_prediction(fX).summary_frame(alpha=0.05)
        fut["Forecast"] = pred["mean"].values
        fut["Lo95"]     = pred["obs_ci_lower"].values
        fut["Hi95"]     = pred["obs_ci_upper"].values

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=rm["Month"],y=rm["Revenue"],
            name="Actual",mode="lines+markers",
            line=dict(color=C["success"],width=2.5),
            marker=dict(size=8,color=C["success"])))
        fig.add_trace(go.Scatter(
            x=fut["Month"],y=fut["Forecast"],
            name="OLS Forecast",mode="lines+markers",
            line=dict(color=C["secondary"],width=2,dash="dash"),
            marker=dict(size=8,symbol="diamond",
                        color=C["secondary"])))
        fig.add_trace(go.Scatter(
            x=fut["Month"],y=[851150]*4,
            name="Conservative",mode="lines",
            line=dict(color=C["warning"],width=2,dash="dot")))
        fig.add_trace(go.Scatter(
            x=list(fut["Month"])+list(fut["Month"][::-1]),
            y=list(fut["Hi95"])+list(fut["Lo95"][::-1]),
            fill="toself",
            fillcolor=f"rgba(69,123,157,0.12)",
            line=dict(color="rgba(0,0,0,0)"),
            name="95% Interval"))
        fig.update_layout(**LAYOUT,height=400,
            legend=dict(orientation="h",y=1.12,
                        bgcolor="rgba(0,0,0,0)",
                        font=dict(color=C["subtext"])))
        fig.update_yaxes(tickformat="$,.0f",
                         title_text="Revenue ($)",
                         title_font=dict(color=C["subtext"]))
        fig.update_xaxes(title_text="Month",
                         title_font=dict(color=C["subtext"]))
        ax(fig)
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"R²={ols.rsquared:.3f} | Monthly trend coefficient: "
                   f"${ols.params['MI']:,.0f} | Fitted on Jan–Jul 2026 (n=7)")

    with c2:
        sec("Passport — Scenario-Based Projection (Aug–Dec 2026)")
        pf_months=["2026-08","2026-09","2026-10","2026-11","2026-12"]
        pf = pd.DataFrame({
            "Month":pf_months,
            "Conservative":[pp["Revenue"].min()]*5,
            "Midpoint"    :[pp["Revenue"].mean()]*5,
            "Optimistic"  :[pp["Revenue"].max()]*5,
        })
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=pp["MF"],y=pp["Revenue"],
            name="Actual",mode="lines+markers",
            line=dict(color=C["success"],width=2.5),
            marker=dict(size=8,color=C["success"])))
        for label,col,dash in [
            ("Optimistic",  C["accent"],   "dashdot"),
            ("Midpoint",    C["secondary"],"dash"),
            ("Conservative",C["warning"],  "dot"),
        ]:
            fig2.add_trace(go.Scatter(
                x=pf["Month"],y=pf[label],
                name=label,mode="lines+markers",
                line=dict(color=col,width=2,dash=dash),
                marker=dict(size=8,symbol="diamond",color=col)))
        fig2.add_trace(go.Scatter(
            x=pf_months+pf_months[::-1],
            y=list(pf["Optimistic"])+list(pf["Conservative"][::-1]),
            fill="toself",
            fillcolor="rgba(42,157,143,0.08)",
            line=dict(color="rgba(0,0,0,0)"),
            name="Projection Range"))
        fig2.update_layout(**LAYOUT,height=400,
            legend=dict(orientation="h",y=1.12,
                        bgcolor="rgba(0,0,0,0)",
                        font=dict(color=C["subtext"])))
        fig2.update_yaxes(tickformat="$,.0f",
                          title_text="Revenue ($)",
                          title_font=dict(color=C["subtext"]))
        fig2.update_xaxes(title_text="Month",
                          title_font=dict(color=C["subtext"]))
        ax(fig2)
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("Scenario-based — no OLS applied. No consistent linear trend in passport production data.")

    st.markdown("<br>", unsafe_allow_html=True)
    sec("2026 Combined Revenue Projection — Three Scenarios")
    pp_act = pp["Revenue"].sum()
    rp_act = df["Amount ($)"].sum()
    scens  = {
        "Conservative":(pp["Revenue"].min()*5, 9649100),
        "Midpoint"    :(pp["Revenue"].mean()*5,11789332),
        "Optimistic"  :(pp["Revenue"].max()*5, 13929564),
    }
    fig3 = go.Figure()
    for name,col in [
        ("Passport Actual (Jan–Jul)",C["secondary"]),
        ("Passport Projection (Aug–Dec)",C["accent"]),
        ("Permit Actual (Jan–Aug)",C["success"]),
        ("Permit Projection (Sep–Dec)","#52B788"),
    ]:
        vals=[]
        for sc,(pp_proj,rp_proj) in scens.items():
            if name=="Passport Actual (Jan–Jul)":
                vals.append(pp_act)
            elif name=="Passport Projection (Aug–Dec)":
                vals.append(pp_proj)
            elif name=="Permit Actual (Jan–Aug)":
                vals.append(rp_act)
            else:
                vals.append(rp_proj-rp_act)
        fig3.add_trace(go.Bar(
            name=name,x=list(scens.keys()),y=vals,
            marker_color=col,opacity=0.9))
    totals=[pp_act+v[0]+v[1] for v in scens.values()]
    for i,(sc,tot) in enumerate(zip(scens.keys(),totals)):
        fig3.add_annotation(
            x=sc,y=tot+300000,
            text=f"<b>${tot/1e6:.1f}M</b>",
            showarrow=False,
            font=dict(size=13,color=C["text"]))
    fig3.update_layout(**LAYOUT,height=480,barmode="stack",
        legend=dict(orientation="h",y=1.12,
                    bgcolor="rgba(0,0,0,0)",
                    font=dict(color=C["subtext"])))
    fig3.update_yaxes(tickformat="$,.0f",
                      title_text="Revenue (USD)",
                      title_font=dict(color=C["subtext"]))
    fig3.update_xaxes(title_text="Scenario",
                      title_font=dict(color=C["subtext"]))
    ax(fig3)
    st.plotly_chart(fig3, use_container_width=True)

    rows2=[]
    for sc,(pp_proj,rp_proj) in scens.items():
        rows2.append({
            "Scenario":sc,
            "Passport Full Year":f"${pp_act+pp_proj:,.0f}",
            "Residency Permit Full Year":f"${rp_proj:,.0f}",
            "Combined Total":f"${pp_act+pp_proj+rp_proj:,.0f}"
        })
    st.dataframe(pd.DataFrame(rows2),
                 use_container_width=True,hide_index=True)
    st.caption("Passport revenue: $100/passport (Ordinary + Service). Diplomatic passports fee-exempt. Source: SLID official fee schedule.")

# ──────────────────────────────────────────────────────────
# TAB 6 — PREDICTIVE ANALYTICS
# ──────────────────────────────────────────────────────────
with tabs[5]:
    st.markdown(f"""
    <p style='font-size:0.88rem;color:{C["subtext"]};margin-bottom:1rem;'>
    This tool uses a trained logistic regression model
    <b style='color:{C["text"]};'>(AUC = 0.867, Accuracy = 82.7%)</b>
    to predict whether a residency permit application is likely to be
    delivered based on its characteristics at the point of submission.</p>
    """, unsafe_allow_html=True)

    if not models_ok:
        st.error("Model files not found. Ensure all .joblib files "
                 "are in the same folder as the dashboard.")
        st.stop()

    pc1,pc2 = st.columns([1,1])

    with pc1:
        sec("Application Input")
        cat_in  = st.selectbox("Permit Category",
            meta.get("categories",["Category B"]),key="pred_cat")
        proc_in = st.selectbox("Process Code",
            meta.get("process_codes",["Resident Permit"]),key="pred_proc")
        amt_in  = st.slider("Payment Amount ($)",
            int(meta.get("amount_min",0)),
            int(meta.get("amount_max",1000)),
            int(meta.get("amount_mean",500)),50,key="pred_amt")
        month_in= st.selectbox("Month of Application",
            list(range(1,13)),
            format_func=lambda x:["Jan","Feb","Mar","Apr","May","Jun",
                                  "Jul","Aug","Sep","Oct","Nov","Dec"][x-1],
            index=5,key="pred_mon")
        dow_in  = st.selectbox("Day of Week",
            ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
            key="pred_dow")
        exp_in  = st.slider("Expected Permit Duration (days)",
            30,400,364,1,key="pred_exp")
        card_in = st.radio("Card Number Assigned?",
            ["Yes","No"],horizontal=True,key="pred_card")
        predict = st.button("🔮  Predict Application Outcome",
                            use_container_width=True)

    with pc2:
        sec("Prediction Result")
        if predict:
            try:
                dow_map = {"Monday":0,"Tuesday":1,"Wednesday":2,
                           "Thursday":3,"Friday":4,"Saturday":5}
                cat_enc  = le_cat.transform([cat_in])[0]
                proc_enc = le_proc.transform([proc_in])[0]
                card_val = 1 if card_in=="Yes" else 0
                X_in = np.array([[amt_in,month_in,
                                  dow_map[dow_in],
                                  exp_in,card_val,
                                  cat_enc,proc_enc]])
                X_sc = scaler.transform(X_in)
                p_del = lr_model.predict_proba(X_sc)[0][1]

                if p_del>=0.75:
                    css,icon,verdict,action = (
                        "pred-green","🟢",
                        "LOW RISK — Likely to be Delivered",
                        "Process normally. No immediate intervention required.")
                elif p_del>=0.50:
                    css,icon,verdict,action = (
                        "pred-gold","🟡",
                        "MEDIUM RISK — Monitor Closely",
                        "Flag for follow-up. Verify document completeness. Assign to senior officer.")
                else:
                    css,icon,verdict,action = (
                        "pred-red","🔴",
                        "HIGH RISK — Application Likely to Stall",
                        "Escalate immediately. Conduct priority identity verification. Assign for manual review.")

                st.markdown(f"""
                <div class="{css}">
                  <h2>{icon} {verdict}</h2>
                  <h3 style='margin:0.5rem 0;'>
                    Delivery Probability: {p_del*100:.1f}%
                  </h3>
                  <p style='font-size:0.88rem;margin:0;'>
                    <b>Recommended Action:</b> {action}
                  </p>
                </div>""", unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                # Gauge
                fig_g = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=p_del*100,
                    title={"text":"Delivery Probability (%)",
                           "font":{"color":C["subtext"]}},
                    number={"font":{"color":C["text"]}},
                    gauge={
                        "axis":{"range":[0,100],
                                "tickcolor":C["subtext"],
                                "tickfont":{"color":C["subtext"]}},
                        "bar":{"color":C["success"] if p_del>=0.75
                               else C["warning"] if p_del>=0.5
                               else C["highlight"]},
                        "steps":[
                            {"range":[0,50], "color":"rgba(230,57,70,0.15)"},
                            {"range":[50,75],"color":"rgba(233,196,106,0.15)"},
                            {"range":[75,100],"color":"rgba(42,157,143,0.15)"},
                        ],
                        "threshold":{
                            "line":{"color":C["subtext"],"width":2},
                            "thickness":0.75,"value":74.7
                        }
                    }
                ))
                fig_g.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color=C["subtext"],family="Inter"),
                    height=280,
                    margin=dict(l=20,r=20,t=40,b=20))
                ax(fig_g)
                st.plotly_chart(fig_g, use_container_width=True)

                # Feature importance
                sec("Feature Influence on Prediction")
                coef_df = pd.DataFrame({
                    "Feature":["Amount ($)","Month","Day of Week",
                               "Days to Expiry","Card Issued",
                               "Category","Process Code"],
                    "Coefficient":lr_model.coef_[0]
                }).sort_values("Coefficient")

                fig_c = go.Figure(go.Bar(
                    x=coef_df["Coefficient"],
                    y=coef_df["Feature"],
                    orientation="h",
                    marker_color=[C["success"] if v>0
                                  else C["highlight"]
                                  for v in coef_df["Coefficient"]]))
                fig_c.update_layout(**LAYOUT,height=280,showlegend=False)
                fig_c.update_xaxes(
                    title_text="Coefficient (positive = increases delivery probability)",
                    title_font=dict(color=C["subtext"]))
                ax(fig_c)
                st.plotly_chart(fig_c, use_container_width=True)

            except Exception as e:
                st.error(f"Prediction error: {e}")

        else:
            st.info("Complete the application details on the left "
                    "and click **Predict Application Outcome**.")
            sec("Model Performance Summary")
            perf = pd.DataFrame({
                "Metric":["Accuracy","ROC-AUC",
                          "Precision (Delivered)",
                          "Recall (Delivered)",
                          "Recall (Not Delivered)",
                          "Training Records"],
                "Value":["82.7%","0.867","85%",
                         "93%","51%","8,894"]
            })
            st.dataframe(perf,use_container_width=True,
                         hide_index=True)

            st.markdown("<br>", unsafe_allow_html=True)
            sec("Applicant Segments — K-Means Cluster Profiles")
            cl_df = pd.DataFrame({
                "Cluster":["Cluster 0","Cluster 1",
                           "Cluster 2","Cluster 3"],
                "Size"   :[2934,6104,1649,373],
                "Avg Fee ($)":[225,709,744,0],
                "Delivery Rate":["67%","100%","0%","47%"],
                "Revenue at Risk":["—","—","$1,226,800","—"],
                "Profile":[
                    "Low-fee, Category E — NGOs, Diplomatic applicants",
                    "High-fee, Category B — Core productive segment. Fully processed.",
                    "High-fee, recent submissions — Permits paid for but NOT issued. $1.23M backlog concentrated in June–July 2026.",
                    "Zero-fee — Diplomatic exemptions. Shorter permit duration (~167 days).",
                ]
            })
            st.dataframe(cl_df,use_container_width=True,
                         hide_index=True)
            warn("Cluster 2 is the most operationally critical finding: 1,649 applicants paid a full average fee of $744 but received no permit. This $1.23M backlog represents a direct reputational and compliance risk for SLID — not an analytical artefact.")
