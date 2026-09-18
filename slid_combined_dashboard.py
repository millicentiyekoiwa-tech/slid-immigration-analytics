"""
SLID Immigration Analytics Dashboard
Digitalization and Process Optimization of Immigration Services in Sierra Leone
Author: Millicent Iye Koiwa | MSc Business Analytics | AUB | 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import statsmodels.api as sm
from math import factorial
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="SLID Analytics",
    page_icon="slid",
    layout="wide",
    initial_sidebar_state="expanded"
)

P = {
    "navy"  : "#1D3557",
    "steel" : "#457B9D",
    "teal"  : "#2A9D8F",
    "gold"  : "#E9C46A",
    "red"   : "#E63946",
    "dark"  : "#0D1B2A",
    "card"  : "#1A2B3C",
    "border": "#2C3E50",
    "text"  : "#F1FAEE",
    "sub"   : "#A8C5D8",
    "mint"  : "#A8DADC",
}
COLORS = [P["steel"], P["teal"], P["gold"], P["red"],
          P["mint"], "#8ECAE6", "#FB8500", "#219EBC"]

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html,body,[class*="css"]{{font-family:'Inter',sans-serif;
  background:{P['dark']};color:{P['text']};}}
.main-header{{background:linear-gradient(135deg,{P['dark']},{P['navy']});
  border-bottom:2px solid {P['steel']};padding:1rem 1.5rem;
  border-radius:10px;margin-bottom:1.2rem;}}
.main-header h1{{color:{P['text']};font-size:1.4rem;font-weight:700;margin:0;}}
.main-header p{{color:{P['sub']};font-size:0.8rem;margin:0.2rem 0 0;}}
.kpi{{background:{P['card']};border-radius:10px;padding:1rem 1.1rem;
  border:1px solid {P['border']};border-top:3px solid {P['steel']};
  margin-bottom:0.7rem;}}
.kpi.g{{border-top-color:{P['teal']};}}
.kpi.r{{border-top-color:{P['red']};}}
.kpi.o{{border-top-color:{P['gold']};}}
.kpi.m{{border-top-color:{P['mint']};}}
.kv{{font-size:1.7rem;font-weight:700;color:{P['text']};margin:0;line-height:1;}}
.kl{{font-size:0.72rem;color:{P['sub']};margin:0.25rem 0 0;
  text-transform:uppercase;letter-spacing:0.05em;}}
.sec{{font-size:0.82rem;font-weight:600;color:{P['sub']};
  text-transform:uppercase;letter-spacing:0.07em;
  border-bottom:1px solid {P['border']};padding-bottom:0.3rem;
  margin-bottom:0.8rem;}}
.ins{{background:rgba(42,157,143,0.1);border-left:3px solid {P['teal']};
  border-radius:5px;padding:0.6rem 0.9rem;font-size:0.8rem;
  color:{P['mint']};margin:0.4rem 0;}}
.wrn{{background:rgba(230,57,70,0.1);border-left:3px solid {P['red']};
  border-radius:5px;padding:0.6rem 0.9rem;font-size:0.8rem;
  color:#FF8A80;margin:0.4rem 0;}}
.fnd{{background:rgba(233,196,106,0.1);border-left:3px solid {P['gold']};
  border-radius:5px;padding:0.6rem 0.9rem;font-size:0.8rem;
  color:{P['gold']};margin:0.4rem 0;}}
.pg{{background:rgba(42,157,143,0.12);border:1.5px solid {P['teal']};
  border-radius:10px;padding:1.1rem;text-align:center;}}
.py{{background:rgba(233,196,106,0.12);border:1.5px solid {P['gold']};
  border-radius:10px;padding:1.1rem;text-align:center;}}
.pr{{background:rgba(230,57,70,0.12);border:1.5px solid {P['red']};
  border-radius:10px;padding:1.1rem;text-align:center;}}
section[data-testid="stSidebar"]{{background:{P['card']};
  border-right:1px solid {P['border']};}}
.stButton>button{{background:{P['navy']};color:{P['text']};
  border:1px solid {P['steel']};border-radius:7px;
  font-weight:600;font-size:0.85rem;padding:0.5rem 1.2rem;}}
.stButton>button:hover{{background:{P['steel']};}}
.block-container{{padding:1.2rem 1.8rem;max-width:100%;}}
</style>""", unsafe_allow_html=True)

# ── Auth ─────────────────────────────────────────────────────
CREDS = {"SLID": "SLID2026"}

if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown(f"""
        <div style="background:{P['card']};border-radius:14px;
          padding:2.2rem;border:1px solid {P['border']};
          box-shadow:0 8px 32px rgba(0,0,0,0.4);margin-top:5rem;">
          <div style="text-align:center;font-size:1.5rem;font-weight:700;
            color:{P['steel']};letter-spacing:0.15em;">SLID</div>
          <div style="text-align:center;font-size:1.1rem;font-weight:700;
            color:{P['text']};margin:0.4rem 0 0.15rem;">
            Analytics Dashboard</div>
          <div style="text-align:center;font-size:0.78rem;color:{P['sub']};
            margin-bottom:1.5rem;">
            Sierra Leone Immigration Department<br>Authorized Access Only</div>
        </div>""", unsafe_allow_html=True)
        with st.form("login"):
            u  = st.text_input("Username", placeholder="Username")
            pw = st.text_input("Password", type="password",
                               placeholder="Password")
            if st.form_submit_button("Sign In", use_container_width=True):
                if u in CREDS and CREDS[u] == pw:
                    st.session_state["auth"] = True
                    st.rerun()
                else:
                    st.error("Invalid credentials.")
        st.markdown(
            f'<p style="text-align:center;font-size:0.72rem;'
            f'color:{P["sub"]};margin-top:1rem;">'
            f'Digitalization and Process Optimization Initiative<br>'
            f'MSc Business Analytics — AUB 2026</p>',
            unsafe_allow_html=True)
    st.stop()

# ── Chart helper ─────────────────────────────────────────────
def L(fig, h=380, legend_h=False, show_legend=True):
    kw = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=h,
        font=dict(family="Inter", color=P["sub"], size=11),
        margin=dict(l=0, r=0, t=28, b=0),
        showlegend=show_legend,
    )
    if show_legend:
        if legend_h:
            kw["legend"] = dict(orientation="h", y=1.1,
                                bgcolor="rgba(0,0,0,0)",
                                font=dict(color=P["sub"]))
        else:
            kw["legend"] = dict(bgcolor="rgba(0,0,0,0)",
                                font=dict(color=P["sub"]))
    fig.update_layout(**kw)
    fig.update_xaxes(gridcolor=P["border"], linecolor=P["border"],
                     tickfont=dict(color=P["sub"]))
    fig.update_yaxes(gridcolor=P["border"], linecolor=P["border"],
                     tickfont=dict(color=P["sub"]))
    return fig

def kpi(label, val, t=""):
    st.markdown(
        f'<div class="kpi {t}"><p class="kv">{val}</p>'
        f'<p class="kl">{label}</p></div>',
        unsafe_allow_html=True)

def sec(t):
    st.markdown(f'<p class="sec">{t}</p>', unsafe_allow_html=True)

def ins(t):
    st.markdown(f'<div class="ins">{t}</div>', unsafe_allow_html=True)

def wrn(t):
    st.markdown(f'<div class="wrn">{t}</div>', unsafe_allow_html=True)

def fnd(t):
    st.markdown(f'<div class="fnd">{t}</div>', unsafe_allow_html=True)

def mms(lam, mu, s):
    rho = lam / (s * mu)
    if rho >= 1:
        return dict(rho=rho, stable=False, W=None, Lq=None)
    terms = sum([(s*rho)**n/factorial(n) for n in range(s)])
    last  = (s*rho)**s / (factorial(s)*(1-rho))
    P0    = 1 / (terms+last)
    Lq    = (P0*(lam/mu)**s*rho) / (factorial(s)*(1-rho)**2)
    Wq    = Lq / lam
    return dict(rho=round(rho,4), stable=True,
                W=round(Wq+1/mu,4), Lq=round(Lq,4))

# ── Data ─────────────────────────────────────────────────────
@st.cache_data
def load_rp():
    df = pd.read_excel("SLID_Residency_Final_Cleaned.xlsx",
                       engine="openpyxl")
    df["Date of Creation"] = pd.to_datetime(
        df["Date of Creation"], errors="coerce")
    df["Card Expiry Date"] = pd.to_datetime(
        df["Card Expiry Date"], errors="coerce")
    if "Month" not in df.columns:
        df["Month"] = df["Date of Creation"]\
            .dt.to_period("M").astype(str)
    if "Month_Num" not in df.columns:
        df["Month_Num"] = df["Date of Creation"].dt.month
    if "Day_of_Week" not in df.columns:
        df["Day_of_Week"] = df["Date of Creation"].dt.day_name()
    if "DOW_Num" not in df.columns:
        df["DOW_Num"] = df["Date of Creation"].dt.dayofweek
    if "Days_to_Expiry" not in df.columns:
        df["Days_to_Expiry"] = (
            df["Card Expiry Date"] - df["Date of Creation"]).dt.days
    if "Card_Issued" not in df.columns:
        df["Card_Issued"] = df["Card Number"].notna().astype(int)
    if "Completion" not in df.columns:
        df["Completion"] = np.where(
            df["Status"]==7, "Delivered", "Not Delivered")
    if "Completion_Binary" not in df.columns:
        df["Completion_Binary"] = (
            df["Completion"]=="Delivered").astype(int)
    if "Status_Name" not in df.columns:
        sm_ = {1:"Draft",2:"New",3:"Appointment Needed",
               5:"Printed",6:"Ready To Pickup",7:"Delivered",
               8:"Expired",11:"Rejected",15:"Need Extra Document",
               19:"Needs Edit"}
        df["Status_Name"] = df["Status"].map(sm_).fillna("Other")
    return df

@st.cache_resource
def load_models(_df):
    try:
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import LabelEncoder, StandardScaler
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import roc_auc_score, accuracy_score

        data = _df.copy()
        le_cat  = LabelEncoder()
        le_proc = LabelEncoder()
        data["Category"]     = data["Category"].fillna("Unknown")
        data["Process Code"] = data["Process Code"].fillna("Unknown")
        data["Cat_Enc"]  = le_cat.fit_transform(data["Category"])
        data["Proc_Enc"] = le_proc.fit_transform(data["Process Code"])

        features = ["Amount ($)","Month_Num","DOW_Num",
                    "Cat_Enc","Proc_Enc"]
        # Drop post-processing columns that cause data leakage
        # Card_Issued and Days_to_Expiry are outcomes, not inputs
        for col in features:
            if col not in data.columns:
                data[col] = 0
        data = data.dropna(subset=features+["Completion_Binary"])

        X = data[features]
        y = data["Completion_Binary"]

        scaler = StandardScaler()
        X_sc   = scaler.fit_transform(X)

        lr = LogisticRegression(max_iter=1000, random_state=42)
        lr.fit(X_sc, y)

        meta = {
            "categories"   : sorted(data["Category"].unique().tolist()),
            "process_codes": sorted(data["Process Code"].unique().tolist()),
            "amount_min"   : float(data["Amount ($)"].min()),
            "amount_max"   : float(data["Amount ($)"].max()),
            "amount_mean"  : float(data["Amount ($)"].mean()),
        }

        X_tr, X_te, y_tr, y_te = train_test_split(
            X_sc, y, test_size=0.2, stratify=y, random_state=42)
        acc = accuracy_score(y_te, lr.predict(X_te))
        auc = roc_auc_score(y_te, lr.predict_proba(X_te)[:,1])

        return lr, scaler, le_cat, le_proc, meta, acc, auc, True
    except Exception as e:
        return None, None, None, None, {}, 0, 0, False

@st.cache_data
def load_pp():
    pp = pd.DataFrame({
        "Month":["Jan","Feb","Mar","Apr","May","Jun","Jul"],
        "MF"   :["2026-01","2026-02","2026-03","2026-04",
                 "2026-05","2026-06","2026-07"],
        "Ord"  :[5894,6370,5094,5468,4102,4754,6685],
        "Svc"  :[55,103,108,10,7,8,83],
        "Dip"  :[15,25,30,27,16,32,17],
        "Tot"  :[5964,6498,5232,5505,4125,4794,6785],
        "WD"   :[26,25,27,26,27,26,27],
    })
    pp["Rev"]  = pp["Ord"]*100 + pp["Svc"]*100
    pp["Rate"] = (pp["Tot"]/pp["WD"]).round(1)
    pp["MoM"]  = pp["Tot"].diff()
    office = pd.DataFrame({
        "Office":["Freetown","Makeni","Kenema","Online","Bo"],
        "Total" :[38195,279,170,130,129],
        "Pct"   :[98.18,0.72,0.44,0.33,0.33],
        "Lat"   :[8.484,8.879,7.876,8.484,7.965],
        "Lon"   :[-13.234,-12.059,-11.190,-13.234,-11.738],
    })
    return pp, office

df                              = load_rp()
pp, office                      = load_pp()
lr_, sc_, lc_, lp_, meta_, acc_, auc_, ok = load_models(df)

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:0.8rem 0 0.5rem;">
      <div style="font-size:1.3rem;font-weight:700;
        color:{P['steel']};letter-spacing:0.15em;">SLID</div>
      <div style="font-weight:600;color:{P['text']};font-size:0.9rem;
        margin:0.2rem 0;">Analytics Dashboard</div>
      <div style="font-size:0.65rem;color:{P['sub']};">
        Sierra Leone Immigration Department</div>
      <div style="font-size:0.62rem;color:{P['sub']};margin-top:0.5rem;
        border-top:1px solid {P['border']};padding-top:0.4rem;">
        MSc Business Analytics<br>
        American University of Beirut<br>
        Suliman S. Olayan School of Business</div>
    </div>""", unsafe_allow_html=True)
    st.divider()
    page = st.radio("", [
        "Overview",
        "Passport Analysis",
        "Residency Permit Analysis",
        "Process Performance",
        "Revenue Forecast",
        "Predictive Analytics",
    ], label_visibility="collapsed")
    st.divider()
    st.caption(
        "Digitalization and Process Optimization\n"
        "of Immigration Services in Sierra Leone\n"
        "Capstone Project — 2026")
    st.divider()
    if st.button("Sign Out", use_container_width=True):
        st.session_state["auth"] = False
        st.rerun()

# ── Header ───────────────────────────────────────────────────
st.markdown(f"""
<div class="main-header">
  <h1>Sierra Leone Immigration Department — Analytics Dashboard</h1>
  <p>Passport Production Jan–Jul 2026  |
     Residency Permit Applications Jan–Aug 2026  |
     Digitalization and Process Optimization Initiative</p>
</div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# OVERVIEW
# ════════════════════════════════════════════════════════════
if page == "Overview":
    with st.expander("Filters", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            all_m   = sorted(df["Month"].dropna().unique())
            sel_m   = st.multiselect("Permit Month", all_m,
                                     default=all_m, key="ov_m")
        with c2:
            sel_pp  = st.multiselect("Passport Month",
                pp["Month"].tolist(),
                default=pp["Month"].tolist(), key="ov_pp")
    fdf = df[df["Month"].isin(sel_m)]
    fpp = pp[pp["Month"].isin(sel_pp)]

    k1,k2,k3,k4,k5,k6 = st.columns(6)
    with k1: kpi("Passports Produced",  f"{fpp['Tot'].sum():,}","m")
    with k2: kpi("Permit Applications", f"{len(fdf):,}")
    with k3:
        dr = (fdf["Completion"]=="Delivered").mean()*100
        kpi("Permit Delivery Rate", f"{dr:.1f}%",
            "g" if dr>70 else "r")
    with k4: kpi("Passport Revenue (Est.)",
                 f"${fpp['Rev'].sum()/1e6:.2f}M","o")
    with k5: kpi("Permit Revenue",
                 f"${fdf['Amount ($)'].sum()/1e6:.2f}M","o")
    with k6:
        tot = fpp["Rev"].sum()+fdf["Amount ($)"].sum()
        kpi("Combined Revenue", f"${tot/1e6:.2f}M","g")

    st.markdown("")
    c1, c2 = st.columns(2)
    with c1:
        sec("Monthly Volume — Passport vs Residency Permit")
        rp_m = fdf.groupby("Month").size().reset_index(name="Apps")
        fig  = go.Figure()
        fig.add_trace(go.Scatter(
            x=fpp["MF"], y=fpp["Tot"], name="Passport",
            mode="lines+markers",
            line=dict(color=P["steel"],width=2.5),
            marker=dict(size=7),
            fill="tozeroy", fillcolor="rgba(69,123,157,0.1)"))
        fig.add_trace(go.Scatter(
            x=rp_m["Month"], y=rp_m["Apps"],
            name="Residency Permit",
            mode="lines+markers",
            line=dict(color=P["teal"],width=2.5),
            marker=dict(size=7),
            fill="tozeroy", fillcolor="rgba(42,157,143,0.1)"))
        L(fig, 380, True)
        fig.update_xaxes(title_text="Month")
        fig.update_yaxes(title_text="Volume")
        st.plotly_chart(fig, use_container_width=True)
        ins("Passport volumes are 5–10x higher than permit applications, "
            "reflecting Sierra Leone's broader citizen travel document demand "
            "versus foreign national residency applications.")

    with c2:
        sec("Monthly Revenue — Passport vs Residency Permit")
        rp_r = fdf.groupby("Month")["Amount ($)"].sum().reset_index()
        rp_r.columns = ["Month","Rev"]
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=fpp["MF"], y=fpp["Rev"], name="Passport (Est.)",
            marker_color=P["steel"], opacity=0.85))
        fig2.add_trace(go.Bar(
            x=rp_r["Month"], y=rp_r["Rev"],
            name="Residency Permit",
            marker_color=P["teal"], opacity=0.85))
        L(fig2, 380, True)
        fig2.update_layout(barmode="group")
        fig2.update_yaxes(tickformat="$,.0f",
                          title_text="Revenue (USD)")
        fig2.update_xaxes(title_text="Month")
        st.plotly_chart(fig2, use_container_width=True)
        ins("Residency permit revenue shows a stronger growth trajectory "
            "through June 2026 compared to passport revenue.")

    st.markdown("")
    c3, c4 = st.columns(2)
    with c3:
        sec("Revenue Split — Passport vs Residency Permit")
        fig3 = go.Figure(go.Pie(
            labels=["Passport (Est.)","Residency Permit"],
            values=[fpp["Rev"].sum(), fdf["Amount ($)"].sum()],
            hole=0.55,
            marker_colors=[P["steel"],P["teal"]],
            textinfo="label+percent",
            textfont=dict(color="white",size=11)))
        L(fig3, 300, show_legend=False)
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        sec("Service Delivery Scorecard")
        sc_df = pd.DataFrame({
            "Metric"  :["Passport Production","Permit Delivery Rate",
                        "Online Adoption","Freetown Concentration",
                        "Processing Time vs Target"],
            "Current" :["212/day","74.7%","0.33%","98.18%","~14 days"],
            "Target"  :["Sustained","95%","20%+","70% or less","3 days"],
            "Status"  :["On Track","Below Target","Critical","Critical","Critical"]
        })
        st.dataframe(sc_df, use_container_width=True, hide_index=True)
        wrn("Three of five delivery metrics are off-target. "
            "Online adoption and geographic decentralisation "
            "are the most urgent gaps.")

# ════════════════════════════════════════════════════════════
# PASSPORT ANALYSIS
# ════════════════════════════════════════════════════════════
elif page == "Passport Analysis":
    with st.expander("Filters", expanded=False):
        sel_pp2 = st.multiselect("Passport Month",
            pp["Month"].tolist(),
            default=pp["Month"].tolist(), key="pp2")
    fpp2 = pp[pp["Month"].isin(sel_pp2)]

    k1,k2,k3,k4,k5 = st.columns(5)
    with k1: kpi("Total Produced",      f"{fpp2['Tot'].sum():,}","m")
    with k2: kpi("Ordinary",            f"{fpp2['Ord'].sum():,}")
    with k3: kpi("Service",             f"{fpp2['Svc'].sum():,}","o")
    with k4: kpi("Diplomatic (Exempt)", f"{fpp2['Dip'].sum():,}")
    with k5: kpi("Est. Revenue",        f"${fpp2['Rev'].sum():,.0f}","g")

    st.markdown("")
    c1, c2 = st.columns(2)
    with c1:
        sec("Monthly Production Trend by Passport Type")
        fig = go.Figure()
        for col,clr,nm in [("Ord",P["steel"],"Ordinary"),
                           ("Svc",P["teal"],"Service"),
                           ("Dip",P["gold"],"Diplomatic")]:
            fig.add_trace(go.Scatter(
                x=fpp2["MF"], y=fpp2[col], name=nm,
                mode="lines+markers",
                line=dict(color=clr,width=2.5),
                marker=dict(size=8,color=clr)))
        L(fig, 380, True)
        fig.update_yaxes(title_text="Passports Produced")
        st.plotly_chart(fig, use_container_width=True)
        wrn("Service passport production collapsed 96% between March (108) "
            "and May (7). The cause remains unconfirmed by SLID and "
            "requires investigation.")

    with c2:
        sec("Passport Type — Volume and Revenue Share")
        td = pd.DataFrame({
            "Type":["Ordinary","Service","Diplomatic"],
            "Vol" :[fpp2["Ord"].sum(),fpp2["Svc"].sum(),
                    fpp2["Dip"].sum()],
            "Rev" :[fpp2["Ord"].sum()*100,
                    fpp2["Svc"].sum()*100, 0]
        })
        fig2 = make_subplots(1, 2,
            subplot_titles=["Volume Share","Revenue Share"],
            specs=[[{"type":"pie"},{"type":"pie"}]])
        for i, col in enumerate(["Vol","Rev"]):
            fig2.add_trace(go.Pie(
                labels=td["Type"], values=td[col], hole=0.5,
                textinfo="label+percent",
                marker_colors=[P["steel"],P["teal"],P["gold"]],
                textfont=dict(color="white",size=11)),
                row=1, col=i+1)
        L(fig2, 380, show_legend=False)
        for a in fig2.layout.annotations:
            a.font.color = P["sub"]
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("")
    c3, c4 = st.columns(2)
    with c3:
        sec("Month-over-Month Production Change")
        mom = fpp2.dropna(subset=["MoM"]).copy()
        fig3 = go.Figure(go.Bar(
            x=mom["MF"], y=mom["MoM"],
            marker_color=[P["teal"] if v >= 0 else P["red"]
                          for v in mom["MoM"]]))
        fig3.add_hline(y=0, line_color=P["border"], line_width=1)
        L(fig3, 340, show_legend=False)
        fig3.update_yaxes(title_text="Change in Volume")
        st.plotly_chart(fig3, use_container_width=True)
        ins("Highest single-month gain: July. "
            "Steepest decline: May. "
            "No consistent linear trend — demand is highly variable.")

    with c4:
        sec("Daily Production Rate by Month")
        fig4 = go.Figure(go.Scatter(
            x=fpp2["MF"], y=fpp2["Rate"],
            mode="lines+markers+text",
            line=dict(color=P["steel"],width=2.5),
            marker=dict(size=10,color=P["steel"]),
            text=fpp2["Rate"].apply(lambda x: f"{x:.0f}/day"),
            textposition="top center",
            textfont=dict(color=P["sub"],size=10)))
        fig4.add_hline(
            y=fpp2["Rate"].mean(), line_dash="dash",
            line_color=P["gold"],
            annotation_text=f"Avg {fpp2['Rate'].mean():.0f}/day",
            annotation_font_color=P["gold"])
        L(fig4, 340, show_legend=False)
        fig4.update_yaxes(title_text="Passports per Working Day")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("")
    sec("Geographic Distribution — Passport Production by Office")
    cm1, cm2 = st.columns([3,2])
    with cm1:
        fig5 = px.scatter_geo(
            office, lat="Lat", lon="Lon",
            size="Total", color="Office",
            hover_name="Office",
            hover_data={"Total":True,"Pct":True,
                        "Lat":False,"Lon":False},
            size_max=60,
            color_discrete_sequence=COLORS,
            projection="natural earth")
        fig5.update_geos(
            visible=True, resolution=50,
            showcountries=True, countrycolor="#A8C5D8",
            showcoastlines=True, coastlinecolor="#A8C5D8",
            showland=True, landcolor="#1D3557",
            showocean=True, oceancolor=P["dark"],
            showlakes=False, showrivers=False,
            showsubunits=True, subunitcolor=P["steel"],
            center={"lat":8.5,"lon":-11.8},
            lataxis_range=[6.5,10.5],
            lonaxis_range=[-14.5,-10.0],
            bgcolor="rgba(0,0,0,0)")
        fig5.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=420,
            font=dict(family="Inter",color=P["sub"],size=11),
            margin=dict(l=0,r=0,t=28,b=0),
            legend=dict(bgcolor="rgba(0,0,0,0)",
                        font=dict(color=P["sub"])),
            geo_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig5, use_container_width=True)

    with cm2:
        sec("Production by Office")
        fig6 = go.Figure(go.Bar(
            x=office.sort_values("Total")["Total"],
            y=office.sort_values("Total")["Office"],
            orientation="h",
            marker_color=COLORS[:5]))
        L(fig6, 320, show_legend=False)
        fig6.update_xaxes(title_text="Passports Produced")
        st.plotly_chart(fig6, use_container_width=True)
        wrn("Freetown handles 98.18% of all production — "
            "a critical single point of failure. "
            "Any disruption in Freetown halts the entire national system.")
        fnd("Online channel: only 130 passports (0.33%) — "
            "negligible digital adoption despite the digitalization mandate.")

# ════════════════════════════════════════════════════════════
# RESIDENCY PERMIT ANALYSIS
# ════════════════════════════════════════════════════════════
elif page == "Residency Permit Analysis":
    with st.expander("Filters", expanded=False):
        rc1, rc2 = st.columns(2)
        with rc1:
            all_m3 = sorted(df["Month"].dropna().unique())
            sel_m3 = st.multiselect("Month", all_m3,
                                    default=all_m3, key="rp3")
        with rc2:
            cats   = ["All"]+sorted(df["Category"].dropna().unique())
            sel_c3 = st.selectbox("Category", cats, key="rc3")
    fdf3 = df[df["Month"].isin(sel_m3)]
    if sel_c3 != "All":
        fdf3 = fdf3[fdf3["Category"]==sel_c3]

    k1,k2,k3,k4,k5 = st.columns(5)
    with k1: kpi("Total Applications", f"{len(fdf3):,}")
    with k2:
        dr3 = (fdf3["Completion"]=="Delivered").mean()*100
        kpi("Delivery Rate", f"{dr3:.1f}%",
            "g" if dr3>70 else "r")
    with k3: kpi("Not Delivered",
                 f"{(fdf3['Completion']=='Not Delivered').sum():,}","r")
    with k4: kpi("Total Revenue",
                 f"${fdf3['Amount ($)'].sum():,.0f}","o")
    with k5: kpi("Average Fee",
                 f"${fdf3['Amount ($)'].mean():,.0f}")

    st.markdown("")
    c1, c2 = st.columns(2)
    with c1:
        sec("Monthly Volume and Revenue")
        m3  = fdf3.groupby("Month").agg(
            Apps=("Receipt Code","count"),
            Rev=("Amount ($)","sum")).reset_index()
        fig = make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(
            x=m3["Month"], y=m3["Apps"], name="Applications",
            marker_color=P["steel"], opacity=0.85),
            secondary_y=False)
        fig.add_trace(go.Scatter(
            x=m3["Month"], y=m3["Rev"], name="Revenue ($)",
            mode="lines+markers",
            line=dict(color=P["gold"],width=2.5),
            marker=dict(size=8,color=P["gold"])),
            secondary_y=True)
        L(fig, 380, True)
        fig.update_layout(barmode="relative")
        fig.update_yaxes(title_text="Applications", secondary_y=False,
                         gridcolor=P["border"],
                         tickfont=dict(color=P["sub"]))
        fig.update_yaxes(title_text="Revenue ($)", tickformat="$,.0f",
                         secondary_y=True,
                         gridcolor="rgba(0,0,0,0)",
                         tickfont=dict(color=P["sub"]))
        st.plotly_chart(fig, use_container_width=True)
        ins("June 2026 was the peak month for both volume (2,634 applications) "
            "and revenue ($1.49M), driven by annual permit renewals.")

    with c2:
        sec("Application Status Distribution")
        sd = fdf3["Status_Name"].value_counts().reset_index()
        sd.columns = ["Status","Count"]
        bar_c = [P["teal"] if s=="Delivered"
                 else P["red"] if s in ["Rejected","Expired"]
                 else P["steel"] for s in sd["Status"]]
        fig2 = go.Figure(go.Bar(
            x=sd["Count"], y=sd["Status"], orientation="h",
            marker_color=bar_c))
        L(fig2, 380, show_legend=False)
        fig2.update_xaxes(title_text="Count")
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("")
    c3, c4 = st.columns(2)
    with c3:
        sec("Applications and Revenue by Category")
        cs = fdf3.groupby("Category", dropna=False).agg(
            Count=("Receipt Code","count"),
            Revenue=("Amount ($)","sum"),
            AvgFee=("Amount ($)","mean"),
            DR=("Completion_Binary","mean")).reset_index()
        cs["Category"] = cs["Category"].fillna("Unknown")
        cs["DR"] = (cs["DR"]*100).round(1)
        fig3 = make_subplots(2,1,
            subplot_titles=["Applications by Category",
                            "Revenue by Category ($)"],
            vertical_spacing=0.16)
        fig3.add_trace(go.Bar(
            x=cs["Category"], y=cs["Count"],
            marker_color=P["steel"], name="Applications"),
            row=1, col=1)
        fig3.add_trace(go.Bar(
            x=cs["Category"], y=cs["Revenue"],
            marker_color=P["teal"], name="Revenue"),
            row=2, col=1)
        L(fig3, 520, show_legend=False)
        for a in fig3.layout.annotations:
            a.font.color = P["sub"]
        st.plotly_chart(fig3, use_container_width=True)

    with c4:
        sec("Delivery Rate and Average Fee by Category")
        fig4 = make_subplots(2,1,
            subplot_titles=["Delivery Rate (%)",
                            "Average Fee ($)"],
            vertical_spacing=0.16)
        dr_c = [P["teal"] if v>80 else P["gold"] if v>50
                else P["red"] for v in cs["DR"]]
        fig4.add_trace(go.Bar(
            x=cs["Category"], y=cs["DR"],
            marker_color=dr_c, name="DR"),
            row=1, col=1)
        fig4.add_hline(y=74.7, line_dash="dash",
                       line_color=P["gold"], row=1, col=1,
                       annotation_text="74.7% overall",
                       annotation_font_color=P["gold"])
        fig4.add_trace(go.Bar(
            x=cs["Category"], y=cs["AvgFee"],
            marker_color=P["gold"], name="Avg Fee"),
            row=2, col=1)
        L(fig4, 520, show_legend=False)
        for a in fig4.layout.annotations:
            a.font.color = P["sub"]
        st.plotly_chart(fig4, use_container_width=True)
        ins("Category B (General Merchandise) generates the highest total "
            "revenue at an average fee of $709. "
            "Category D (Dependants) is lowest at $213.")

    st.markdown("")
    sec("Revenue by Role — Top 10")
    cr1, cr2 = st.columns(2)
    with cr1:
        role_rev = fdf3.groupby("Role", dropna=False)["Amount ($)"].agg(
            ["sum","count","mean"]).sort_values(
            "sum", ascending=False).head(10).reset_index()
        role_rev.columns = ["Role","Total Revenue","Count","Avg Fee"]
        role_rev["Role"] = role_rev["Role"].fillna("Unknown")
        fig_rv = go.Figure(go.Bar(
            x=role_rev["Total Revenue"],
            y=role_rev["Role"],
            orientation="h",
            marker_color=P["steel"], opacity=0.9))
        L(fig_rv, 400, show_legend=False)
        fig_rv.update_xaxes(tickformat="$,.0f",
                            title_text="Total Revenue ($)")
        fig_rv.update_yaxes(categoryorder="total ascending")
        st.plotly_chart(fig_rv, use_container_width=True)
        ins("General Merchandise is the top revenue-generating role. "
            "Mining and Construction follow, reflecting Sierra Leone's "
            "extractive and development sector foreign workforce.")

    with cr2:
        fig_rf = go.Figure(go.Bar(
            x=role_rev["Role"],
            y=role_rev["Avg Fee"],
            marker_color=[P["teal"] if v > role_rev["Avg Fee"].mean()
                          else P["gold"]
                          for v in role_rev["Avg Fee"]],
            opacity=0.9))
        L(fig_rf, 400, show_legend=False)
        fig_rf.update_xaxes(tickangle=-35, title_text="Role")
        fig_rf.update_yaxes(tickformat="$,.0f",
                            title_text="Average Fee ($)")
        st.plotly_chart(fig_rf, use_container_width=True)
        fnd("Roles generating above-average fees tend to fall in "
            "Category A (Mining, Aviation, Casinos) and Category B (Banking). "
            "Domestic Staff and Dependants carry the lowest fees.")

    st.markdown("")
    c5, c6 = st.columns(2)
    with c5:
        sec("Applications by Day of Week")
        do  = ["Monday","Tuesday","Wednesday",
               "Thursday","Friday","Saturday"]
        dow = fdf3["Day_of_Week"].value_counts()\
              .reindex(do).dropna().reset_index()
        dow.columns = ["Day","Count"]
        fig5 = go.Figure(go.Bar(
            x=dow["Day"], y=dow["Count"],
            marker_color=[P["red"] if d=="Tuesday"
                          else P["steel"] for d in dow["Day"]]))
        L(fig5, 320, show_legend=False)
        fig5.update_yaxes(title_text="Applications")
        st.plotly_chart(fig5, use_container_width=True)
        ins("Monday is the busiest day. "
            "Tuesday shows an anomalously low volume — "
            "worth investigating with SLID.")

    with c6:
        sec("Applicant Segments — K-Means Cluster Analysis (k=4)")
        cl = pd.DataFrame({
            "Cluster":["Cluster 0","Cluster 1",
                       "Cluster 2","Cluster 3"],
            "Size"   :[2934,6104,1649,373],
            "Fee"    :[225,709,744,0],
            "DR"     :[67,100,0,47],
        })
        fig6 = go.Figure()
        for i, row in cl.iterrows():
            fig6.add_trace(go.Scatter(
                x=[row["Fee"]], y=[row["DR"]],
                mode="markers+text",
                marker=dict(size=max(row["Size"]/60,15),
                            color=COLORS[i], opacity=0.85,
                            line=dict(color="white",width=1.5)),
                text=[row["Cluster"]],
                textposition="top center",
                textfont=dict(color=P["sub"],size=10),
                name=row["Cluster"],
                hovertemplate=(
                    f"<b>{row['Cluster']}</b><br>"
                    f"Size: {row['Size']:,}<br>"
                    f"Avg Fee: ${row['Fee']}<br>"
                    f"Delivery Rate: {row['DR']}%"
                    "<extra></extra>")))
        L(fig6, 320, show_legend=False)
        fig6.update_xaxes(title_text="Average Fee ($)")
        fig6.update_yaxes(title_text="Delivery Rate (%)")
        st.plotly_chart(fig6, use_container_width=True)
        wrn("Cluster 2 — 1,649 applicants paid an average of $744 in full "
            "but received no permit. This represents $1.23M in revenue "
            "collected but undelivered — a critical backlog concentrated "
            "in June and July 2026.")

# ════════════════════════════════════════════════════════════
# PROCESS PERFORMANCE
# ════════════════════════════════════════════════════════════
elif page == "Process Performance":
    sec("M/M/s Queuing Model — Real-Time Capacity Check")
    pc1, pc2, pc3 = st.columns(3)
    with pc1:
        lam  = st.number_input("Daily applications (lambda)",
                               1, 400, 51, 1, key="lam")
    with pc2:
        s_in = st.number_input("Officers available (s)",
                               1, 20, 3, 1, key="sin")
    with pc3:
        mu_in = st.number_input("Applications per officer per day (mu)",
                                1, 50, 5, 1, key="muin")

    m_ = mms(lam, mu_in, s_in)
    if m_["stable"]:
        st.markdown(f"""<div class="pg">
          <h3>SYSTEM STABLE</h3>
          <p>Utilisation: <b>{m_['rho']*100:.1f}%</b> &nbsp;|&nbsp;
          Processing time: <b>{m_['W']:.3f} days
          ({m_['W']*8:.1f} hours)</b> &nbsp;|&nbsp;
          Average queue: <b>{m_['Lq']:.1f} applications</b></p>
        </div>""", unsafe_allow_html=True)
    else:
        cap   = s_in * mu_in
        extra = int(np.ceil((lam-cap)/mu_in))
        st.markdown(f"""<div class="pr">
          <h3>SYSTEM OVERLOADED — Queue grows indefinitely</h3>
          <p>Capacity: <b>{cap}/day</b> &nbsp;|&nbsp;
          Demand: <b>{lam}/day</b> &nbsp;|&nbsp;
          Requires at least <b>{extra} additional officer(s)</b></p>
        </div>""", unsafe_allow_html=True)

    st.markdown("")
    c1, c2 = st.columns(2)
    with c1:
        sec("AS-IS vs TO-BE Processing Time Across All Demand Scenarios")
        demands = {
            "Jan (Low)":11.62,"Feb":37.96,"Mar":37.93,
            "Apr":55.43,"May":68.26,"Jun (Peak)":87.80,
            "Jul":52.87,"Aug":42.67
        }
        scenarios = {
            "AS-IS (s=3, mu=5)"       :(3,5,  P["red"]),
            "Min Viable (s=6, mu=15)" :(6,15, P["gold"]),
            "Recommended (s=8, mu=12)":(8,12, P["steel"]),
            "Optimal (s=10, mu=10)"   :(10,10,P["teal"]),
        }
        fig = go.Figure()
        for lb,(sc,mv,col) in scenarios.items():
            Wv = [mms(lv,mv,sc)["W"]
                  if mms(lv,mv,sc)["stable"] else None
                  for lv in demands.values()]
            fig.add_trace(go.Scatter(
                x=list(demands.keys()), y=Wv,
                mode="lines+markers", name=lb,
                line=dict(color=col,width=2.5),
                marker=dict(size=8,color=col),
                connectgaps=False))
        fig.add_hline(y=1.0, line_dash="dash",
                      line_color=P["mint"],
                      annotation_text="1-day internal target",
                      annotation_font_color=P["mint"])
        fig.add_hline(y=3.0, line_dash="dot",
                      line_color=P["sub"],
                      annotation_text="3-day overall target",
                      annotation_font_color=P["sub"])
        L(fig, 420, True)
        fig.update_yaxes(title_text="Total Days in System (W)",
                         range=[0,6])
        fig.update_xaxes(title_text="Month")
        st.plotly_chart(fig, use_container_width=True)
        ins("The recommended configuration (s=8, mu=12) remains stable "
            "and within the 1-day internal target across all months "
            "including the June peak of 87.80 applications per day.")

    with c2:
        sec(f"Sensitivity Analysis — Processing Time (days) at lambda={lam}/day")
        sr  = list(range(3,14))
        mr  = [5,8,10,12,15,20]
        hd  = []
        for sc in sr:
            row = {"Servers":sc}
            for mv in mr:
                r = mms(lam, mv, sc)
                row[f"mu={mv}"] = round(r["W"],3) if r["stable"] else None
            hd.append(row)
        hdf = pd.DataFrame(hd).set_index("Servers")
        fig2 = px.imshow(hdf, text_auto=".2f", aspect="auto",
                         color_continuous_scale="RdYlGn_r",
                         labels={"x":"Service Rate (mu)",
                                 "y":"Servers","color":"Days"})
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=420,
            font=dict(family="Inter",color=P["sub"],size=11),
            margin=dict(l=0,r=0,t=28,b=0))
        fig2.update_xaxes(tickfont=dict(color=P["sub"]))
        fig2.update_yaxes(tickfont=dict(color=P["sub"]))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("")
    sec("Configuration Summary")
    rows = []
    for lb,(sc,mv,_) in scenarios.items():
        am = mms(50.77, mv, sc)
        pm = mms(87.80, mv, sc)
        rows.append({
            "Scenario"    : lb,
            "Servers"     : sc,
            "mu"          : mv,
            "Avg W (days)": f"{am['W']:.4f}" if am["stable"] else "UNSTABLE",
            "Peak W (days)":f"{pm['W']:.4f}" if pm["stable"] else "UNSTABLE",
            "Feasible"    : "Yes" if am["stable"] and pm["stable"] else "No"
        })
    st.dataframe(pd.DataFrame(rows),
                 use_container_width=True, hide_index=True)
    fnd("Digitising identity verification through NCRA API integration is "
        "the single highest-impact technical intervention available to SLID. "
        "It raises the service rate (mu) without requiring proportional "
        "headcount increases.")

# ════════════════════════════════════════════════════════════
# REVENUE FORECAST
# ════════════════════════════════════════════════════════════
elif page == "Revenue Forecast":
    c1, c2 = st.columns(2)
    with c1:
        sec("Residency Permit — OLS Linear Trend Forecast (Sep–Dec 2026)")
        rm = df.groupby("Month")["Amount ($)"].sum().reset_index()
        rm.columns = ["Month","Revenue"]
        rm["MI"]   = np.arange(1, len(rm)+1)
        md = rm.iloc[:7].copy()
        Xo = sm.add_constant(md["MI"])
        yo = md["Revenue"]
        ols = sm.OLS(yo, Xo).fit()
        fut = pd.DataFrame({
            "Month":["2026-09","2026-10","2026-11","2026-12"],
            "MI"   :[9,10,11,12]})
        fXo  = sm.add_constant(fut["MI"], has_constant="add")
        pred = ols.get_prediction(fXo).summary_frame(alpha=0.05)
        fut["Fc"] = pred["mean"].values
        fut["Lo"] = pred["obs_ci_lower"].values
        fut["Hi"] = pred["obs_ci_upper"].values

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=rm["Month"], y=rm["Revenue"], name="Actual",
            mode="lines+markers",
            line=dict(color=P["teal"],width=2.5),
            marker=dict(size=8,color=P["teal"])))
        fig.add_trace(go.Scatter(
            x=fut["Month"], y=fut["Fc"], name="OLS Forecast",
            mode="lines+markers",
            line=dict(color=P["steel"],width=2,dash="dash"),
            marker=dict(size=8,symbol="diamond",color=P["steel"])))
        fig.add_trace(go.Scatter(
            x=fut["Month"], y=[851150]*4,
            name="Conservative",
            mode="lines",
            line=dict(color=P["gold"],width=2,dash="dot")))
        fig.add_trace(go.Scatter(
            x=list(fut["Month"])+list(fut["Month"][::-1]),
            y=list(fut["Hi"])+list(fut["Lo"][::-1]),
            fill="toself",
            fillcolor="rgba(69,123,157,0.1)",
            line=dict(color="rgba(0,0,0,0)"),
            name="95% Interval"))
        L(fig, 400, True)
        fig.update_yaxes(tickformat="$,.0f", title_text="Revenue ($)")
        fig.update_xaxes(title_text="Month")
        st.plotly_chart(fig, use_container_width=True)
        st.caption(
            f"R-squared = {ols.rsquared:.3f}  |  "
            f"Monthly trend: ${ols.params['MI']:,.0f}  |  "
            f"Fitted on Jan–Jul 2026 (n=7)")

    with c2:
        sec("Passport — Scenario-Based Projection (Aug–Dec 2026)")
        pf_m = ["2026-08","2026-09","2026-10","2026-11","2026-12"]
        pf   = pd.DataFrame({
            "Month"       : pf_m,
            "Conservative": [pp["Rev"].min()]*5,
            "Midpoint"    : [pp["Rev"].mean()]*5,
            "Optimistic"  : [pp["Rev"].max()]*5,
        })
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=pp["MF"], y=pp["Rev"], name="Actual",
            mode="lines+markers",
            line=dict(color=P["teal"],width=2.5),
            marker=dict(size=8,color=P["teal"])))
        for lb,col,dsh in [
            ("Optimistic",  P["mint"],  "dashdot"),
            ("Midpoint",    P["steel"], "dash"),
            ("Conservative",P["gold"],  "dot"),
        ]:
            fig2.add_trace(go.Scatter(
                x=pf["Month"], y=pf[lb], name=lb,
                mode="lines+markers",
                line=dict(color=col,width=2,dash=dsh),
                marker=dict(size=8,symbol="diamond",color=col)))
        fig2.add_trace(go.Scatter(
            x=pf_m+pf_m[::-1],
            y=list(pf["Optimistic"])+list(pf["Conservative"][::-1]),
            fill="toself",
            fillcolor="rgba(42,157,143,0.07)",
            line=dict(color="rgba(0,0,0,0)"),
            name="Projection Range"))
        L(fig2, 400, True)
        fig2.update_yaxes(tickformat="$,.0f", title_text="Revenue ($)")
        fig2.update_xaxes(title_text="Month")
        st.plotly_chart(fig2, use_container_width=True)
        st.caption(
            "Scenario-based projection — OLS not applied. "
            "No consistent linear trend identified in passport production data.")

    st.markdown("")
    sec("2026 Combined Revenue Projection — Three Scenarios")
    pa    = pp["Rev"].sum()
    ra    = df["Amount ($)"].sum()
    scens = {
        "Conservative": (pp["Rev"].min()*5,   9649100),
        "Midpoint"    : (pp["Rev"].mean()*5, 11789332),
        "Optimistic"  : (pp["Rev"].max()*5,  13929564),
    }
    fig3 = go.Figure()
    for nm,col in [
        ("Passport Actual",       P["steel"]),
        ("Passport Projection",   P["mint"]),
        ("Permit Actual",         P["teal"]),
        ("Permit Projection",     "#52B788"),
    ]:
        vals = []
        for sc,(pp_,rp_) in scens.items():
            if   nm=="Passport Actual":     vals.append(pa)
            elif nm=="Passport Projection": vals.append(pp_)
            elif nm=="Permit Actual":       vals.append(ra)
            else:                           vals.append(rp_-ra)
        fig3.add_trace(go.Bar(name=nm,
            x=list(scens.keys()), y=vals,
            marker_color=col, opacity=0.9))
    tots = [pa+v[0]+v[1] for v in scens.values()]
    for i,(sc,tot) in enumerate(zip(scens.keys(), tots)):
        fig3.add_annotation(x=sc, y=tot+200000,
            text=f"<b>${tot/1e6:.1f}M</b>",
            showarrow=False,
            font=dict(size=13, color=P["text"]))
    L(fig3, 460, True)
    fig3.update_layout(barmode="stack")
    fig3.update_yaxes(tickformat="$,.0f", title_text="Revenue (USD)")
    fig3.update_xaxes(title_text="Scenario")
    st.plotly_chart(fig3, use_container_width=True)

    rows2 = []
    for sc,(pp_,rp_) in scens.items():
        rows2.append({
            "Scenario"          : sc,
            "Passport Full Year": f"${pa+pp_:,.0f}",
            "Permit Full Year"  : f"${rp_:,.0f}",
            "Combined Total"    : f"${pa+pp_+rp_:,.0f}"
        })
    st.dataframe(pd.DataFrame(rows2),
                 use_container_width=True, hide_index=True)
    st.caption(
        "Passport revenue estimated at $100 per passport (Ordinary and Service). "
        "Diplomatic passports are fee-exempt. "
        "Source: SLID official fee schedule.")

# ════════════════════════════════════════════════════════════
# PREDICTIVE ANALYTICS
# ════════════════════════════════════════════════════════════
elif page == "Predictive Analytics":
    acc_disp = f"{acc_*100:.1f}%" if ok else "N/A"
    auc_disp = f"{auc_:.3f}"     if ok else "N/A"

    st.markdown(
        f"<p style='font-size:0.85rem;color:{P['sub']};'>"
        "Logistic regression model trained on 11,118 residency permit records. "
        f"<b style='color:{P['text']};'>"
        f"AUC = {auc_disp} &nbsp;|&nbsp; Accuracy = {acc_disp}</b>. "
        "Predicts whether an application will be delivered "
        "based on its characteristics at the point of submission.</p>",
        unsafe_allow_html=True)

    if not ok:
        st.error("Model could not be trained. Check that "
                 "SLID_Residency_Final_Cleaned.xlsx is in the repository.")
        st.stop()

    pc1, pc2 = st.columns([1,1])
    with pc1:
        sec("Application Input")
        cat_in  = st.selectbox("Permit Category",
            meta_.get("categories", ["Category B"]), key="pcat")
        prc_in  = st.selectbox("Process Code",
            meta_.get("process_codes", ["Resident Permit"]), key="pprc")
        amt_in  = st.slider("Payment Amount ($)",
            int(meta_.get("amount_min",0)),
            int(meta_.get("amount_max",1000)),
            int(meta_.get("amount_mean",500)), 50, key="pamt")
        mon_in  = st.selectbox("Month of Application",
            list(range(1,13)),
            format_func=lambda x: [
                "Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"][x-1],
            index=5, key="pmon")
        dow_in  = st.selectbox("Day of Week",
            ["Monday","Tuesday","Wednesday",
             "Thursday","Friday","Saturday"], key="pdow")
        go_btn  = st.button("Predict Outcome",
                            use_container_width=True)

    with pc2:
        sec("Prediction Result")
        if go_btn:
            try:
                dm = {"Monday":0,"Tuesday":1,"Wednesday":2,
                      "Thursday":3,"Friday":4,"Saturday":5}
                try:
                    ce = lc_.transform([cat_in])[0]
                except Exception:
                    ce = 0
                try:
                    pe = lp_.transform([prc_in])[0]
                except Exception:
                    pe = 0
                Xi  = np.array([[amt_in, mon_in, dm[dow_in],
                                 ce, pe]])
                Xs  = sc_.transform(Xi)
                pd_ = lr_.predict_proba(Xs)[0][1]

                if pd_ >= 0.75:
                    css, vd, ac = (
                        "pg",
                        "LOW RISK — Likely to be Delivered",
                        "Process normally. No immediate intervention required.")
                elif pd_ >= 0.50:
                    css, vd, ac = (
                        "py",
                        "MEDIUM RISK — Monitor Closely",
                        "Flag for follow-up. Verify document completeness. "
                        "Assign to senior officer.")
                else:
                    css, vd, ac = (
                        "pr",
                        "HIGH RISK — Application Likely to Stall",
                        "Escalate immediately. "
                        "Conduct priority identity verification. "
                        "Assign for manual review.")

                st.markdown(f"""<div class="{css}">
                  <h3>{vd}</h3>
                  <h2>Delivery Probability: {pd_*100:.1f}%</h2>
                  <p><b>Recommended Action:</b> {ac}</p>
                </div>""", unsafe_allow_html=True)

                st.markdown("")
                fg = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=pd_*100,
                    title={"text":"Delivery Probability (%)"},
                    number={"font":{"color":P["text"]}},
                    gauge={
                        "axis":{"range":[0,100],
                                "tickfont":{"color":P["sub"]}},
                        "bar":{"color": P["teal"]  if pd_>=0.75
                               else     P["gold"]  if pd_>=0.5
                               else     P["red"]},
                        "steps":[
                            {"range":[0,50],
                             "color":"rgba(230,57,70,0.12)"},
                            {"range":[50,75],
                             "color":"rgba(233,196,106,0.12)"},
                            {"range":[75,100],
                             "color":"rgba(42,157,143,0.12)"},
                        ],
                        "threshold":{
                            "line":{"color":P["sub"],"width":2},
                            "thickness":0.75,"value":74.7}
                    }))
                fg.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=260,
                    font=dict(family="Inter",color=P["sub"],size=11),
                    margin=dict(l=20,r=20,t=40,b=20))
                st.plotly_chart(fg, use_container_width=True)

                sec("Feature Influence on Prediction")
                cdf = pd.DataFrame({
                    "Feature":["Amount ($)","Month",
                               "Day of Week","Category",
                               "Process Code"],
                    "Coef": lr_.coef_[0]
                }).sort_values("Coef")
                fc = go.Figure(go.Bar(
                    x=cdf["Coef"], y=cdf["Feature"],
                    orientation="h",
                    marker_color=[P["teal"] if v>0 else P["red"]
                                  for v in cdf["Coef"]]))
                fc.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    height=280, showlegend=False,
                    font=dict(family="Inter",color=P["sub"],size=11),
                    margin=dict(l=0,r=0,t=28,b=0))
                fc.update_xaxes(gridcolor=P["border"],
                                tickfont=dict(color=P["sub"]),
                                title_text="Coefficient")
                fc.update_yaxes(gridcolor=P["border"],
                                tickfont=dict(color=P["sub"]))
                st.plotly_chart(fc, use_container_width=True)

            except Exception as e:
                st.error(f"Prediction error: {e}")
        else:
            st.info("Fill in the application details on the left "
                    "and click Predict Outcome.")

            sec("Model Performance Summary")
            st.dataframe(pd.DataFrame({
                "Metric":["Accuracy","ROC-AUC",
                          "Precision (Delivered)",
                          "Recall (Delivered)",
                          "Recall (Not Delivered)",
                          "Training Records"],
                "Value" :[acc_disp, auc_disp,
                          "~85%","~93%","~51%","~8,894"]
            }), use_container_width=True, hide_index=True)

            st.markdown("")
            sec("K-Means Cluster Profiles (k=4)")
            st.dataframe(pd.DataFrame({
                "Cluster":["Cluster 0","Cluster 1",
                           "Cluster 2","Cluster 3"],
                "Size"   :[2934,6104,1649,373],
                "Avg Fee ($)":[225,709,744,0],
                "Delivery Rate":["67%","100%","0%","47%"],
                "Revenue at Risk":["—","—","$1,226,800","—"],
                "Description":[
                    "Low-fee, Category E — NGOs and Diplomatic applicants",
                    "High-fee, Category B — Core productive segment. "
                    "Fully processed.",
                    "High-fee — Permits paid in full but NOT issued. "
                    "$1.23M backlog concentrated in June–July 2026.",
                    "Zero-fee — Diplomatic exemptions. "
                    "Shorter permit duration (~167 days).",
                ]
            }), use_container_width=True, hide_index=True)
            wrn("Cluster 2 is the most critical finding: 1,649 applicants "
                "paid an average of $744 but received no permit. "
                "This is not an analytical artefact — it is a $1.23M "
                "operational backlog requiring urgent management attention.")
