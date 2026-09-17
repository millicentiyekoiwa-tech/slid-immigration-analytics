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
    page_title="SLID — Immigration Analytics Dashboard",
    page_icon="🛂",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════
# STYLING
# ═══════════════════════════════════════════════════════════
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1B5E20, #2E7D32);
        padding: 1.5rem 2rem; border-radius: 12px;
        margin-bottom: 1.5rem; color: white;
    }
    .main-header h1 { color: white; font-size: 1.8rem;
                      font-weight: 700; margin: 0; }
    .main-header p  { color: #C8E6C9; margin: 0.3rem 0 0 0;
                      font-size: 0.95rem; }
    .kpi-card { background: white; border-radius: 10px;
                padding: 1.2rem; border-left: 5px solid #2E7D32;
                box-shadow: 0 2px 8px rgba(0,0,0,0.08);
                margin-bottom: 1rem; }
    .kpi-card.red   { border-left-color: #C62828; }
    .kpi-card.amber { border-left-color: #E65100; }
    .kpi-card.blue  { border-left-color: #1565C0; }
    .kpi-card.purple{ border-left-color: #6A1B9A; }
    .kpi-value { font-size: 1.9rem; font-weight: 700;
                 color: #1B5E20; margin: 0; }
    .kpi-value.red    { color: #C62828; }
    .kpi-value.amber  { color: #E65100; }
    .kpi-value.blue   { color: #1565C0; }
    .kpi-value.purple { color: #6A1B9A; }
    .kpi-label { font-size: 0.82rem; color: #546E7A;
                 margin: 0.2rem 0 0 0; font-weight: 500; }
    .kpi-delta { font-size: 0.78rem; margin: 0.1rem 0 0 0; }
    .section-header { font-size: 1.05rem; font-weight: 700;
                      color: #1B5E20; border-bottom: 2px solid #2E7D32;
                      padding-bottom: 0.35rem; margin-bottom: 1rem; }
    .insight-box { background: #E8F5E9; border-left: 4px solid #2E7D32;
                   padding: 0.8rem 1rem; border-radius: 6px;
                   margin: 0.5rem 0; font-size: 0.88rem; color: #1B5E20; }
    .warning-box { background: #FFF3E0; border-left: 4px solid #E65100;
                   padding: 0.8rem 1rem; border-radius: 6px;
                   margin: 0.5rem 0; font-size: 0.88rem; color: #E65100; }
    .prediction-green  { background:#E8F5E9; border:2px solid #2E7D32;
                         border-radius:10px; padding:1rem; text-align:center; }
    .prediction-amber  { background:#FFF3E0; border:2px solid #E65100;
                         border-radius:10px; padding:1rem; text-align:center; }
    .prediction-red    { background:#FFEBEE; border:2px solid #C62828;
                         border-radius:10px; padding:1rem; text-align:center; }
    #MainMenu {visibility:hidden;} footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════
def kpi(label, value, color="green", delta=None, prefix="", suffix=""):
    delta_html = f'<p class="kpi-delta" style="color:{"#2E7D32" if delta and "▲" in str(delta) else "#C62828"}">{delta}</p>' if delta else ""
    st.markdown(f"""
    <div class="kpi-card {color}">
        <p class="kpi-value {color}">{prefix}{value}{suffix}</p>
        <p class="kpi-label">{label}</p>
        {delta_html}
    </div>""", unsafe_allow_html=True)

def section(title):
    st.markdown(f'<p class="section-header">{title}</p>', unsafe_allow_html=True)

def insight(text):
    st.markdown(f'<div class="insight-box">💡 {text}</div>', unsafe_allow_html=True)

def warning(text):
    st.markdown(f'<div class="warning-box">⚠️ {text}</div>', unsafe_allow_html=True)

def mms(lam, mu, s):
    rho = lam / (s * mu)
    if rho >= 1:
        return {"rho":rho,"stable":False,"W":None,"Lq":None,"Wq":None}
    terms = sum([(s*rho)**n/factorial(n) for n in range(s)])
    last  = (s*rho)**s/(factorial(s)*(1-rho))
    P0    = 1/(terms+last)
    Lq    = (P0*(lam/mu)**s*rho)/(factorial(s)*(1-rho)**2)
    Wq    = Lq/lam
    W     = Wq + 1/mu
    return {"rho":round(rho,4),"stable":True,
            "W":round(W,4),"Lq":round(Lq,4),
            "Wq":round(Wq,4),"P0":round(P0,4)}

# ═══════════════════════════════════════════════════════════
# LOAD DATA & MODELS
# ═══════════════════════════════════════════════════════════
@st.cache_data
def load_residency_data():
    df = pd.read_excel("SLID_Residency_Final_Cleaned.xlsx", engine="openpyxl")
    df["Date of Creation"] = pd.to_datetime(df["Date of Creation"], errors="coerce")
    df["Card Expiry Date"]  = pd.to_datetime(df["Card Expiry Date"],  errors="coerce")
    if "Month" not in df.columns:
        df["Month"] = df["Date of Creation"].dt.to_period("M").astype(str)
    if "Month_Num" not in df.columns:
        df["Month_Num"] = df["Date of Creation"].dt.month
    if "Day_of_Week" not in df.columns:
        df["Day_of_Week"] = df["Date of Creation"].dt.day_name()
    if "DOW_Num" not in df.columns:
        df["DOW_Num"] = df["Date of Creation"].dt.dayofweek
    if "Days_to_Expiry" not in df.columns:
        df["Days_to_Expiry"] = (df["Card Expiry Date"] - df["Date of Creation"]).dt.days
    if "Card_Issued" not in df.columns:
        df["Card_Issued"] = df["Card Number"].notna().astype(int)
    if "Completion" not in df.columns:
        status_map = {7:"Delivered"}
        df["Status_Name"] = df["Status"].map(status_map).fillna("Not Delivered")
        df["Completion"] = np.where(df["Status"]==7,"Delivered","Not Delivered")
    if "Completion_Binary" not in df.columns:
        df["Completion_Binary"] = (df["Completion"]=="Delivered").astype(int)
    return df

@st.cache_resource
def load_models():
    try:
        lr_model  = joblib.load("slid_logistic_model.joblib")
        scaler    = joblib.load("slid_scaler.joblib")
        le_cat    = joblib.load("slid_le_category.joblib")
        le_proc   = joblib.load("slid_le_process.joblib")
        km_model  = joblib.load("slid_kmeans_model.joblib")
        kscaler   = joblib.load("slid_kscaler.joblib")
        with open("slid_feature_meta.json") as f:
            meta = json.load(f)
        with open("slid_ols_params.json") as f:
            ols_params = json.load(f)
        return lr_model, scaler, le_cat, le_proc, km_model, kscaler, meta, ols_params
    except Exception as e:
        return None, None, None, None, None, None, {}, {}

# ── Passport data (hardcoded from PPTX) ──────────────────
@st.cache_data
def load_passport_data():
    pp = pd.DataFrame({
        "Month"     : ["Jan","Feb","Mar","Apr","May","Jun","Jul"],
        "Month_Full": ["2026-01","2026-02","2026-03","2026-04",
                       "2026-05","2026-06","2026-07"],
        "Month_Num" : [1,2,3,4,5,6,7],
        "Ordinary"  : [5894,6370,5094,5468,4102,4754,6685],
        "Service"   : [55,103,108,10,7,8,83],
        "Diplomatic": [15,25,30,27,16,32,17],
        "Total"     : [5964,6498,5232,5505,4125,4794,6785],
        "Working_Days":[26,25,27,26,27,26,27],
    })
    pp["Revenue"]    = pp["Ordinary"]*100 + pp["Service"]*100
    pp["Daily_Rate"] = (pp["Total"]/pp["Working_Days"]).round(1)
    pp["MoM_Change"] = pp["Total"].diff()
    pp["MoM_Pct"]    = pp["Total"].pct_change()*100

    office = pd.DataFrame({
        "Office": ["Freetown","Makeni","Kenema","Online","Bo"],
        "Total" : [38195,279,170,130,129],
        "Pct"   : [98.18,0.72,0.44,0.33,0.33],
        "Lat"   : [8.484,8.879,7.876,8.484,7.965],
        "Lon"   : [-13.234,-12.059,-11.190,-13.234,-11.738],
    })
    return pp, office

df   = load_residency_data()
pp, office = load_passport_data()
lr_model, scaler, le_cat, le_proc, km_model, kscaler, meta, ols_params = load_models()

# ═══════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 🛂 SLID Analytics")
    st.markdown("*Immigration Services Dashboard*")
    st.divider()

    page = st.radio("Navigation", [
        "📊 Executive Overview",
        "🛂 Passport Analysis",
        "📋 Residency Permit Analysis",
        "⚙️ Process Performance",
        "💰 Revenue Forecast",
        "🔮 Predictive Analytics",
    ], label_visibility="collapsed")

    st.divider()
    st.markdown("**Filters**")

    # Month filter
    all_rp_months = sorted(df["Month"].dropna().unique().tolist())
    sel_months = st.multiselect("Residency Permit Month",
                                all_rp_months, default=all_rp_months)

    # Category filter
    all_cats = ["All"] + sorted(df["Category"].dropna().unique().tolist())
    sel_cat  = st.selectbox("Permit Category", all_cats)

    # Passport month filter
    pp_months = pp["Month"].tolist()
    sel_pp_months = st.multiselect("Passport Month",
                                   pp_months, default=pp_months)

    st.divider()
    st.caption("Digitalization & Process Optimization\n"
               "of Immigration Services in Sierra Leone\n"
               "MSc Business Analytics — AUB 2026")

# ── Apply filters ─────────────────────────────────────────
fdf = df[df["Month"].isin(sel_months)]
if sel_cat != "All":
    fdf = fdf[fdf["Category"] == sel_cat]
fpp = pp[pp["Month"].isin(sel_pp_months)]

# ── Colours ───────────────────────────────────────────────
C = {"green":"#2E7D32","blue":"#1565C0","red":"#C62828",
     "amber":"#E65100","purple":"#6A1B9A","teal":"#00695C",
     "green_light":"#E8F5E9","blue_light":"#E3F2FD"}

# ═══════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════
st.markdown("""
<div class="main-header">
  <h1>🛂 Sierra Leone Immigration Department — Analytics Dashboard</h1>
  <p>Passport Production (Jan–Jul 2026) &nbsp;|&nbsp;
     Residency Permit Applications (Jan–Aug 2026) &nbsp;|&nbsp;
     Digitalization & Process Optimization Initiative</p>
</div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════
# TAB 1 — EXECUTIVE OVERVIEW
# ═══════════════════════════════════════════════════════════
if page == "📊 Executive Overview":

    section("Key Performance Indicators — Combined Services")
    c1,c2,c3,c4,c5,c6 = st.columns(6)
    with c1: kpi("Total Passports Produced", f"{pp['Total'].sum():,}", "green")
    with c2: kpi("Total Permit Applications", f"{len(df):,}", "blue")
    with c3:
        del_rate = (df["Completion"]=="Delivered").mean()*100
        kpi("Permit Delivery Rate", f"{del_rate:.1f}%", "green")
    with c4: kpi("Passport Revenue (Est.)", f"${pp['Revenue'].sum():,.0f}", "blue")
    with c5: kpi("Permit Revenue (Actual)", f"${df['Amount ($)'].sum():,.0f}", "green")
    with c6:
        combined = pp["Revenue"].sum() + df["Amount ($)"].sum()
        kpi("Combined Revenue", f"${combined:,.0f}", "purple")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        section("Monthly Volume — Passport vs Residency Permit")
        rp_monthly = df.groupby("Month").size().reset_index()
        rp_monthly.columns = ["Month","Applications"]

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=pp["Month_Full"], y=pp["Total"],
            mode="lines+markers", name="Passport Production",
            line=dict(color=C["green"], width=2.5),
            marker=dict(size=8),
            fill="tozeroy", fillcolor="rgba(46,125,50,0.08)"
        ))
        fig.add_trace(go.Scatter(
            x=rp_monthly["Month"], y=rp_monthly["Applications"],
            mode="lines+markers", name="Residency Permit Applications",
            line=dict(color=C["blue"], width=2.5),
            marker=dict(size=8),
            fill="tozeroy", fillcolor="rgba(21,101,192,0.08)"
        ))
        fig.update_layout(height=380, hovermode="x unified",
                          legend=dict(orientation="h", y=1.08),
                          yaxis_title="Volume",
                          xaxis_title="Month",
                          margin=dict(l=0,r=0,t=30,b=0))
        st.plotly_chart(fig, use_container_width=True)
        insight("Passport volumes are 5–10x higher than permit applications, reflecting Sierra Leone's broader travel document demand versus foreign national residency applications.")

    with col2:
        section("Monthly Revenue — Passport vs Residency Permit")
        rp_rev = df.groupby("Month")["Amount ($)"].sum().reset_index()
        rp_rev.columns = ["Month","Revenue"]

        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=pp["Month_Full"], y=pp["Revenue"],
            name="Passport Revenue (Est.)",
            marker_color=C["green"], opacity=0.85,
            text=pp["Revenue"].apply(lambda x: f"${x/1e6:.2f}M"),
            textposition="inside"
        ))
        fig2.add_trace(go.Bar(
            x=rp_rev["Month"], y=rp_rev["Revenue"],
            name="Residency Permit Revenue",
            marker_color=C["blue"], opacity=0.85,
            text=rp_rev["Revenue"].apply(lambda x: f"${x/1e6:.2f}M"),
            textposition="inside"
        ))
        fig2.update_layout(
            barmode="group", height=380, hovermode="x unified",
            legend=dict(orientation="h", y=1.08),
            yaxis=dict(tickformat="$,.0f", title="Revenue (USD)"),
            xaxis_title="Month",
            margin=dict(l=0,r=0,t=30,b=0)
        )
        st.plotly_chart(fig2, use_container_width=True)
        insight("Passport revenue is significantly higher per month due to volume. Residency permit revenue shows stronger month-over-month growth trajectory.")

    st.divider()
    col3, col4 = st.columns(2)

    with col3:
        section("Service Delivery Performance")
        perf = pd.DataFrame({
            "Metric": ["Passport Delivery Rate","Permit Delivery Rate",
                       "Online Channel Adoption","Freetown Concentration",
                       "Current Processing Time"],
            "Value" : [f"{pp['Total'].sum()/pp['Total'].sum()*100:.0f}%",
                       f"{del_rate:.1f}%","0.33%","98.18%","~14 days"],
            "Target": ["100%","100%","≥20%","≤70%","3 days"],
            "Status": ["✅","⚠️","❌","❌","❌"]
        })
        st.dataframe(perf, use_container_width=True, hide_index=True)

    with col4:
        section("Revenue Split — Passport vs Residency Permit")
        fig3 = px.pie(
            values=[pp["Revenue"].sum(), df["Amount ($)"].sum()],
            names=["Passport (Est.)","Residency Permit"],
            hole=0.5,
            color_discrete_sequence=[C["green"], C["blue"]]
        )
        fig3.update_traces(textinfo="label+percent+value",
                           texttemplate="%{label}<br>%{percent}<br>$%{value:,.0f}")
        fig3.update_layout(height=320, showlegend=False,
                           margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig3, use_container_width=True)

# ═══════════════════════════════════════════════════════════
# TAB 2 — PASSPORT ANALYSIS
# ═══════════════════════════════════════════════════════════
elif page == "🛂 Passport Analysis":

    section("Passport Production KPIs — Jan–Jul 2026")
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: kpi("Total Produced", f"{fpp['Total'].sum():,}", "green")
    with c2: kpi("Ordinary", f"{fpp['Ordinary'].sum():,}", "blue")
    with c3: kpi("Service", f"{fpp['Service'].sum():,}", "amber")
    with c4: kpi("Diplomatic (exempt)", f"{fpp['Diplomatic'].sum():,}", "purple")
    with c5: kpi("Est. Revenue", f"${fpp['Revenue'].sum():,.0f}", "green")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        section("Monthly Production Trend by Passport Type")
        fig = go.Figure()
        for ptype, color in [("Ordinary",C["green"]),
                              ("Service",C["blue"]),
                              ("Diplomatic",C["amber"])]:
            fig.add_trace(go.Scatter(
                x=fpp["Month_Full"], y=fpp[ptype],
                mode="lines+markers", name=ptype,
                line=dict(color=color, width=2.5),
                marker=dict(size=9)
            ))
        fig.update_layout(height=400, hovermode="x unified",
                          legend=dict(orientation="h", y=1.08),
                          yaxis_title="Passports Produced",
                          xaxis_title="Month",
                          margin=dict(l=0,r=0,t=30,b=0))
        st.plotly_chart(fig, use_container_width=True)
        warning("Service passport production dropped 96% between March and May 2026 — from 108 to 7. This anomaly requires investigation with SLID.")

    with col2:
        section("Passport Type Breakdown")
        type_data = pd.DataFrame({
            "Type"   : ["Ordinary","Service","Diplomatic"],
            "Volume" : [fpp["Ordinary"].sum(), fpp["Service"].sum(), fpp["Diplomatic"].sum()],
            "Revenue": [fpp["Ordinary"].sum()*100, fpp["Service"].sum()*100, 0]
        })
        fig2 = make_subplots(rows=1, cols=2,
            subplot_titles=["Volume Share","Revenue Share"],
            specs=[[{"type":"pie"},{"type":"pie"}]])
        fig2.add_trace(go.Pie(
            labels=type_data["Type"], values=type_data["Volume"],
            hole=0.45, textinfo="label+percent",
            marker_colors=[C["green"],C["blue"],C["amber"]]
        ), row=1, col=1)
        fig2.add_trace(go.Pie(
            labels=type_data["Type"], values=type_data["Revenue"],
            hole=0.45, textinfo="label+percent",
            marker_colors=[C["green"],C["blue"],C["amber"]]
        ), row=1, col=2)
        fig2.update_layout(height=400, showlegend=False,
                           margin=dict(l=0,r=0,t=40,b=0))
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    col3, col4 = st.columns(2)

    with col3:
        section("Month-over-Month Production Change")
        mom = fpp.dropna(subset=["MoM_Change"]).copy()
        fig3 = px.bar(
            mom, x="Month_Full", y="MoM_Change",
            text=mom["MoM_Change"].apply(lambda x: f"{x:+,.0f}"),
            color="MoM_Change",
            color_continuous_scale="RdYlGn",
            labels={"MoM_Change":"Change","Month_Full":"Month"}
        )
        fig3.add_hline(y=0, line_color="gray", line_width=1)
        fig3.update_traces(textposition="outside")
        fig3.update_layout(height=380, showlegend=False,
                           margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig3, use_container_width=True)
        insight(f"Largest single-month increase: July (+{pp['MoM_Change'].max():,.0f}). Largest decline: May ({pp['MoM_Change'].min():,.0f}). Demand is highly variable — no consistent trend.")

    with col4:
        section("Daily Production Rate by Month")
        fig4 = go.Figure()
        fig4.add_trace(go.Scatter(
            x=fpp["Month_Full"], y=fpp["Daily_Rate"],
            mode="lines+markers+text",
            line=dict(color=C["green"], width=2.5),
            marker=dict(size=10),
            text=fpp["Daily_Rate"].apply(lambda x: f"{x:.0f}/day"),
            textposition="top center"
        ))
        fig4.add_hline(
            y=fpp["Daily_Rate"].mean(),
            line_dash="dash", line_color=C["amber"],
            annotation_text=f"Avg: {fpp['Daily_Rate'].mean():.0f}/day",
            annotation_position="bottom right"
        )
        fig4.update_layout(height=380,
                           yaxis_title="Passports per Working Day",
                           xaxis_title="Month",
                           margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig4, use_container_width=True)

    st.divider()
    section("Geographic Distribution — Passport Production by Office")

    col5, col6 = st.columns([3, 2])
    with col5:
        fig5 = px.scatter_mapbox(
            office, lat="Lat", lon="Lon",
            size="Total", color="Office",
            hover_name="Office",
            hover_data={"Total":True,"Pct":True,"Lat":False,"Lon":False},
            size_max=60, zoom=6,
            mapbox_style="carto-positron",
            center={"lat":8.5,"lon":-11.8},
            title="Passport Production by Office"
        )
        fig5.update_layout(height=450, margin=dict(l=0,r=0,t=40,b=0))
        st.plotly_chart(fig5, use_container_width=True)

    with col6:
        section("Office Distribution")
        fig6 = px.bar(
            office.sort_values("Total", ascending=True),
            x="Total", y="Office", orientation="h",
            text=office.sort_values("Total")["Pct"].apply(lambda x: f"{x:.2f}%"),
            color="Total", color_continuous_scale="Greens"
        )
        fig6.update_traces(textposition="outside")
        fig6.update_layout(height=350, showlegend=False,
                           margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig6, use_container_width=True)
        warning("Freetown handles 98.18% of all passport production — a single point of failure for the entire national system.")
        insight("Online channel accounts for only 0.33% of production (130 passports) despite the digitalization initiative — indicating very low digital adoption.")

# ═══════════════════════════════════════════════════════════
# TAB 3 — RESIDENCY PERMIT ANALYSIS
# ═══════════════════════════════════════════════════════════
elif page == "📋 Residency Permit Analysis":

    section("Residency Permit KPIs")
    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: kpi("Total Applications", f"{len(fdf):,}", "green")
    with c2:
        dr = (fdf["Completion"]=="Delivered").mean()*100
        kpi("Delivery Rate", f"{dr:.1f}%", "green" if dr>70 else "amber")
    with c3:
        nd = (fdf["Completion"]=="Not Delivered").sum()
        kpi("Not Delivered", f"{nd:,}", "red")
    with c4: kpi("Total Revenue", f"${fdf['Amount ($)'].sum():,.0f}", "blue")
    with c5: kpi("Average Fee", f"${fdf['Amount ($)'].mean():,.0f}", "blue")

    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        section("Monthly Application Volume & Revenue")
        monthly = fdf.groupby("Month").agg(
            Applications=("Receipt Code","count"),
            Revenue=("Amount ($)","sum")
        ).reset_index()

        fig = make_subplots(specs=[[{"secondary_y":True}]])
        fig.add_trace(go.Bar(
            x=monthly["Month"], y=monthly["Applications"],
            name="Applications", marker_color=C["green"],
            opacity=0.8,
            text=monthly["Applications"],
            textposition="outside"
        ), secondary_y=False)
        fig.add_trace(go.Scatter(
            x=monthly["Month"], y=monthly["Revenue"],
            name="Revenue ($)", mode="lines+markers",
            line=dict(color=C["blue"], width=2.5),
            marker=dict(size=8)
        ), secondary_y=True)
        fig.update_layout(height=400, hovermode="x unified",
                          legend=dict(orientation="h", y=1.08),
                          margin=dict(l=0,r=0,t=30,b=0))
        fig.update_yaxes(title_text="Applications", secondary_y=False)
        fig.update_yaxes(title_text="Revenue ($)", tickformat="$,.0f",
                         secondary_y=True)
        st.plotly_chart(fig, use_container_width=True)
        insight("June 2026 was peak month for both volume (2,634 applications) and revenue ($1.49M) — driven by foreign nationals renewing annual permits.")

    with col2:
        section("Application Status Distribution")
        status_dist = fdf["Status_Name"].value_counts().reset_index() if "Status_Name" in fdf.columns else \
                      pd.DataFrame({"Status_Name":["Delivered","Not Delivered"],
                                    "count":[(fdf["Completion"]=="Delivered").sum(),
                                             (fdf["Completion"]=="Not Delivered").sum()]})
        if "Status_Name" in fdf.columns:
            status_dist = fdf["Status_Name"].value_counts().reset_index()
            status_dist.columns = ["Status","Count"]
        else:
            status_dist = pd.DataFrame({
                "Status":["Delivered","Not Delivered"],
                "Count":[(fdf["Completion"]=="Delivered").sum(),
                         (fdf["Completion"]=="Not Delivered").sum()]
            })

        fig2 = px.bar(
            status_dist.sort_values("Count"),
            x="Count", y="Status", orientation="h",
            text="Count", color="Count",
            color_continuous_scale="Greens"
        )
        fig2.update_traces(textposition="outside")
        fig2.update_layout(height=400, showlegend=False,
                           margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    col3, col4 = st.columns(2)

    with col3:
        section("Applications & Revenue by Category")
        cat_summary = fdf.groupby("Category", dropna=False).agg(
            Count=("Receipt Code","count"),
            Revenue=("Amount ($)","sum"),
            Avg_Fee=("Amount ($)","mean"),
            Delivery_Rate=("Completion_Binary","mean")
        ).reset_index()
        cat_summary["Category"] = cat_summary["Category"].fillna("Unknown")
        cat_summary["Delivery_Rate"] = (cat_summary["Delivery_Rate"]*100).round(1)

        fig3 = make_subplots(rows=2, cols=1,
            subplot_titles=["Applications by Category",
                            "Revenue by Category ($)"],
            vertical_spacing=0.15)
        fig3.add_trace(go.Bar(
            x=cat_summary["Category"], y=cat_summary["Count"],
            marker_color=C["green"], text=cat_summary["Count"],
            textposition="outside", name="Applications"
        ), row=1, col=1)
        fig3.add_trace(go.Bar(
            x=cat_summary["Category"], y=cat_summary["Revenue"],
            marker_color=C["blue"],
            text=cat_summary["Revenue"].apply(lambda x: f"${x:,.0f}"),
            textposition="outside", name="Revenue"
        ), row=2, col=1)
        fig3.update_layout(height=560, showlegend=False,
                           margin=dict(l=0,r=0,t=40,b=0))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        section("Delivery Rate & Average Fee by Category")
        fig4 = make_subplots(rows=2, cols=1,
            subplot_titles=["Delivery Rate by Category (%)",
                            "Average Fee by Category ($)"],
            vertical_spacing=0.15)
        fig4.add_trace(go.Bar(
            x=cat_summary["Category"],
            y=cat_summary["Delivery_Rate"],
            marker_color=[C["green"] if v>80 else C["amber"] if v>50 else C["red"]
                          for v in cat_summary["Delivery_Rate"]],
            text=cat_summary["Delivery_Rate"].apply(lambda x: f"{x:.1f}%"),
            textposition="outside", name="Delivery Rate"
        ), row=1, col=1)
        fig4.add_hline(y=74.7, line_dash="dash",
                       line_color=C["amber"],
                       annotation_text="Overall avg: 74.7%",
                       row=1, col=1)
        fig4.add_trace(go.Bar(
            x=cat_summary["Category"],
            y=cat_summary["Avg_Fee"],
            marker_color=C["purple"],
            text=cat_summary["Avg_Fee"].apply(lambda x: f"${x:,.0f}"),
            textposition="outside", name="Avg Fee"
        ), row=2, col=1)
        fig4.update_layout(height=560, showlegend=False,
                           margin=dict(l=0,r=0,t=40,b=0))
        st.plotly_chart(fig4, use_container_width=True)
        insight("Category B (General Merchandise) generates the highest total revenue and has the highest average fee ($709). Category D has the lowest fee ($213) — reflecting the dependent/housewife applicant profile.")

    st.divider()
    col5, col6 = st.columns(2)

    with col5:
        section("Applications by Day of Week")
        day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        dow = fdf["Day_of_Week"].value_counts().reindex(day_order).dropna().reset_index()
        dow.columns = ["Day","Count"]
        fig5 = px.bar(
            dow, x="Day", y="Count", text="Count",
            color="Count", color_continuous_scale="Greens"
        )
        fig5.update_traces(textposition="outside")
        fig5.update_layout(height=360, showlegend=False,
                           margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig5, use_container_width=True)
        insight("Monday is the busiest day. Tuesday is surprisingly low — potentially a data anomaly worth investigating with SLID.")

    with col6:
        section("Cluster Profiles — Applicant Segments")
        cluster_profile = pd.DataFrame({
            "Cluster": ["Cluster 0","Cluster 1","Cluster 2","Cluster 3"],
            "Size"   : [2934, 6104, 1649, 373],
            "Avg Fee": [225, 709, 744, 0],
            "Delivery Rate (%)": [67, 100, 0, 47],
            "Segment": ["Low-fee, partial delivery\n(Category E)",
                        "High-fee, fully delivered\n(Core productive segment)",
                        "High-fee, zero delivery\n(Backlog — $1.23M at risk)",
                        "Zero-fee exemptions\n(Diplomatic waivers)"]
        })
        fig6 = px.scatter(
            cluster_profile,
            x="Avg Fee", y="Delivery Rate (%)",
            size="Size", color="Cluster",
            text="Cluster",
            size_max=60,
            color_discrete_sequence=[C["amber"],C["green"],C["red"],C["purple"]],
            title=""
        )
        fig6.update_traces(textposition="top center")
        fig6.update_layout(height=360, showlegend=False,
                           xaxis_title="Average Fee ($)",
                           yaxis_title="Delivery Rate (%)",
                           margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig6, use_container_width=True)
        warning("Cluster 2: 1,649 high-fee applications ($744 avg) with 0% delivery — representing $1.23M in permits paid for but not yet issued.")

# ═══════════════════════════════════════════════════════════
# TAB 4 — PROCESS PERFORMANCE
# ═══════════════════════════════════════════════════════════
elif page == "⚙️ Process Performance":

    section("M/M/s Queuing Model — Real-Time Capacity Check")

    col1, col2, col3 = st.columns(3)
    with col1:
        lam = st.number_input("Daily applications (λ)", 1, 400, 51, 1)
    with col2:
        s   = st.number_input("Officers available (s)", 1, 20, 3, 1)
    with col3:
        mu  = st.number_input("Applications/officer/day (μ)", 1, 50, 5, 1)

    m = mms(lam, mu, s)
    if m["stable"]:
        w_hours = m["W"] * 8
        st.markdown(f"""
        <div class="prediction-green">
            <h3>🟢 SYSTEM STABLE</h3>
            <p>Utilisation: <b>{m['rho']*100:.1f}%</b> &nbsp;|&nbsp;
            Processing time: <b>{m['W']:.3f} days ({w_hours:.1f} hrs)</b> &nbsp;|&nbsp;
            Avg queue: <b>{m['Lq']:.1f} applications</b></p>
        </div>""", unsafe_allow_html=True)
    else:
        cap = s * mu
        extra = int(np.ceil((lam - cap) / mu))
        st.markdown(f"""
        <div class="prediction-red">
            <h3>🔴 SYSTEM OVERLOADED — Queue grows indefinitely</h3>
            <p>Capacity: <b>{cap}/day</b> &nbsp;|&nbsp; Demand: <b>{lam}/day</b> &nbsp;|&nbsp;
            Add at least <b>{extra} more officer(s)</b> or defer applications.</p>
        </div>""", unsafe_allow_html=True)

    st.divider()
    section("AS-IS vs TO-BE Processing Time — All Demand Scenarios")

    demands = {"Jan (Low)":11.62,"Feb":37.96,"Mar":37.93,
               "Apr":55.43,"May":68.26,"Jun (Peak)":87.80,
               "Jul":52.87,"Aug":42.67}
    scenarios_comp = {
        "AS-IS (s=3, μ=5)"          : (3,  5,  C["red"]),
        "Min Viable (s=6, μ=15)"    : (6,  15, C["amber"]),
        "Recommended (s=8, μ=12)"   : (8,  12, C["blue"]),
        "Optimal (s=10, μ=10)"      : (10, 10, C["green"]),
    }

    fig = go.Figure()
    for label, (sc, mu_v, color) in scenarios_comp.items():
        W_vals = []
        for lam_v in demands.values():
            mv = mms(lam_v, mu_v, sc)
            W_vals.append(mv["W"] if mv["stable"] else None)
        fig.add_trace(go.Scatter(
            x=list(demands.keys()), y=W_vals,
            mode="lines+markers", name=label,
            line=dict(color=color, width=2.5),
            marker=dict(size=9), connectgaps=False
        ))
    fig.add_hline(y=1.0, line_dash="dash", line_color=C["purple"],
                  annotation_text="1-day internal target")
    fig.add_hline(y=3.0, line_dash="dot", line_color="gray",
                  annotation_text="3-day overall target")
    fig.update_layout(height=480, hovermode="x unified",
                      xaxis_title="Month", yaxis_title="Total Days (W)",
                      legend=dict(orientation="h", y=1.08),
                      yaxis=dict(range=[0,6]),
                      margin=dict(l=0,r=0,t=30,b=0))
    st.plotly_chart(fig, use_container_width=True)
    insight("The AS-IS system collapses under all demand conditions except January. The recommended configuration (s=8, μ=12) stays stable and within the 1-day target across all months including the June peak.")

    st.divider()
    section("Sensitivity Analysis — Processing Time (days) by Servers and Service Rate")
    st.caption(f"Current demand: λ = {lam} applications/day")

    server_range = list(range(3,16))
    mu_range     = [5,8,10,12,15,20]

    heat_data = []
    for sc in server_range:
        row = {"Servers":sc}
        for mu_v in mu_range:
            mv = mms(lam, mu_v, sc)
            row[f"μ={mu_v}"] = round(mv["W"],3) if mv["stable"] else None
        heat_data.append(row)

    heat_df = pd.DataFrame(heat_data).set_index("Servers")
    fig2 = px.imshow(
        heat_df, text_auto=".2f", aspect="auto",
        color_continuous_scale="RdYlGn_r",
        labels={"x":"Service Rate (μ)","y":"Servers","color":"Days"}
    )
    fig2.update_layout(height=450, margin=dict(l=0,r=0,t=20,b=0))
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    section("Configuration Recommendation Summary")
    rows = []
    for label, (sc, mu_v, _) in scenarios_comp.items():
        avg_m  = mms(50.77, mu_v, sc)
        peak_m = mms(87.80, mu_v, sc)
        rows.append({
            "Scenario": label, "Servers": sc, "μ": mu_v,
            "Avg W (days)": f"{avg_m['W']:.4f}" if avg_m["stable"] else "UNSTABLE",
            "Peak W (days)": f"{peak_m['W']:.4f}" if peak_m["stable"] else "UNSTABLE",
            "Feasible": "✅" if avg_m["stable"] and peak_m["stable"] else "❌"
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ═══════════════════════════════════════════════════════════
# TAB 5 — REVENUE FORECAST
# ═══════════════════════════════════════════════════════════
elif page == "💰 Revenue Forecast":

    section("Revenue Forecast — Passport & Residency Permit")

    col1, col2 = st.columns(2)

    with col1:
        section("Residency Permit — OLS Linear Trend Forecast")
        rp_monthly = df.groupby("Month")["Amount ($)"].agg(["sum","count"]).reset_index()
        rp_monthly.columns = ["Month","Revenue","Applications"]
        rp_monthly["Month_Index"] = np.arange(1, len(rp_monthly)+1)

        model_data = rp_monthly.iloc[:7].copy()
        X   = sm.add_constant(model_data["Month_Index"])
        y   = model_data["Revenue"]
        ols = sm.OLS(y, X).fit()

        future = pd.DataFrame({
            "Month": ["2026-09","2026-10","2026-11","2026-12"],
            "Month_Index": [9,10,11,12]
        })
        fX   = sm.add_constant(future["Month_Index"], has_constant="add")
        pred = ols.get_prediction(fX).summary_frame(alpha=0.05)
        future["Forecast"]  = pred["mean"].values
        future["Lower_95"]  = pred["obs_ci_lower"].values
        future["Upper_95"]  = pred["obs_ci_upper"].values

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=rp_monthly["Month"], y=rp_monthly["Revenue"],
            mode="lines+markers", name="Actual",
            line=dict(color=C["green"], width=2.5), marker=dict(size=8)
        ))
        fig.add_trace(go.Scatter(
            x=future["Month"], y=future["Forecast"],
            mode="lines+markers", name="Forecast (Linear Trend)",
            line=dict(color=C["blue"], width=2, dash="dash"),
            marker=dict(size=8, symbol="diamond")
        ))
        fig.add_trace(go.Scatter(
            x=future["Month"], y=[851150]*4,
            mode="lines", name="Conservative",
            line=dict(color=C["amber"], width=2, dash="dot")
        ))
        fig.add_trace(go.Scatter(
            x=list(future["Month"])+list(future["Month"][::-1]),
            y=list(future["Upper_95"])+list(future["Lower_95"][::-1]),
            fill="toself", fillcolor="rgba(21,101,192,0.10)",
            line=dict(color="rgba(0,0,0,0)"), name="95% Interval"
        ))
        fig.update_layout(
            height=420, hovermode="x unified",
            legend=dict(orientation="h", y=1.08),
            yaxis=dict(tickformat="$,.0f", title="Revenue ($)"),
            xaxis_title="Month",
            margin=dict(l=0,r=0,t=30,b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        st.caption(f"R²={ols.rsquared:.3f} | Monthly trend: ${ols.params['Month_Index']:,.0f} | n=7 months")

    with col2:
        section("Passport — Scenario-Based Projection")
        pp_future = pd.DataFrame({
            "Month": ["2026-08","2026-09","2026-10","2026-11","2026-12"],
            "Conservative": [pp["Revenue"].min()]*5,
            "Midpoint"    : [pp["Revenue"].mean()]*5,
            "Optimistic"  : [pp["Revenue"].max()]*5,
        })

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=pp["Month_Full"], y=pp["Revenue"],
            mode="lines+markers", name="Actual",
            line=dict(color=C["green"], width=2.5), marker=dict(size=8)
        ))
        for label, color, dash in [
            ("Optimistic",  C["purple"],"dashdot"),
            ("Midpoint",    C["blue"],  "dash"),
            ("Conservative",C["amber"], "dot"),
        ]:
            fig2.add_trace(go.Scatter(
                x=pp_future["Month"], y=pp_future[label],
                mode="lines+markers", name=label,
                line=dict(color=color, width=2, dash=dash),
                marker=dict(size=8, symbol="diamond")
            ))
        fig2.add_trace(go.Scatter(
            x=list(pp_future["Month"])+list(pp_future["Month"][::-1]),
            y=list(pp_future["Optimistic"])+list(pp_future["Conservative"][::-1]),
            fill="toself", fillcolor="rgba(46,125,50,0.08)",
            line=dict(color="rgba(0,0,0,0)"), name="Projection Range"
        ))
        fig2.update_layout(
            height=420, hovermode="x unified",
            legend=dict(orientation="h", y=1.08),
            yaxis=dict(tickformat="$,.0f", title="Revenue ($)"),
            xaxis_title="Month",
            margin=dict(l=0,r=0,t=30,b=0)
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("Scenario-based — no OLS applied due to absence of linear trend in passport production data.")

    st.divider()
    section("2026 Combined Revenue Projection — Three Scenarios")

    pp_actual  = pp["Revenue"].sum()
    rp_actual  = df["Amount ($)"].sum()

    scenarios = {
        "Conservative": (pp["Revenue"].min()*5, 9649100),
        "Midpoint"    : (pp["Revenue"].mean()*5, 11789332),
        "Optimistic"  : (pp["Revenue"].max()*5, 13929564),
    }

    fig3 = go.Figure()
    fig3.add_trace(go.Bar(
        name="Passport (Actual Jan–Jul)",
        x=list(scenarios.keys()),
        y=[pp_actual]*3,
        marker_color=C["green"], opacity=0.9,
        text=[f"${pp_actual:,.0f}"]*3,
        textposition="inside"
    ))
    fig3.add_trace(go.Bar(
        name="Passport (Aug–Dec Projection)",
        x=list(scenarios.keys()),
        y=[v[0] for v in scenarios.values()],
        marker_color=C["teal"], opacity=0.8,
        text=[f"${v[0]:,.0f}" for v in scenarios.values()],
        textposition="inside"
    ))
    fig3.add_trace(go.Bar(
        name="Residency Permit (Actual Jan–Aug)",
        x=list(scenarios.keys()),
        y=[rp_actual]*3,
        marker_color=C["blue"], opacity=0.9,
        text=[f"${rp_actual:,.0f}"]*3,
        textposition="inside"
    ))
    fig3.add_trace(go.Bar(
        name="Residency Permit (Sep–Dec Projection)",
        x=list(scenarios.keys()),
        y=[v[1]-rp_actual for v in scenarios.values()],
        marker_color="#1E88E5", opacity=0.7,
        text=[f"${v[1]-rp_actual:,.0f}" for v in scenarios.values()],
        textposition="inside"
    ))

    totals = [pp_actual+v[0]+v[1] for v in scenarios.values()]
    for i, (sc, total) in enumerate(zip(scenarios.keys(), totals)):
        fig3.add_annotation(
            x=sc, y=total+200000,
            text=f"<b>Total: ${total:,.0f}</b>",
            showarrow=False, font=dict(size=12, color="#1B5E20")
        )

    fig3.update_layout(
        barmode="stack", height=520,
        xaxis_title="Scenario", yaxis=dict(tickformat="$,.0f", title="Revenue (USD)"),
        legend=dict(orientation="h", y=1.08),
        margin=dict(l=0,r=0,t=50,b=0)
    )
    st.plotly_chart(fig3, use_container_width=True)

    # Summary table
    rows = []
    for sc, (pp_proj, rp_proj) in scenarios.items():
        rows.append({
            "Scenario": sc,
            "Passport (Full Year)": f"${pp_actual+pp_proj:,.0f}",
            "Residency Permit (Full Year)": f"${rp_proj:,.0f}",
            "Combined Total": f"${pp_actual+pp_proj+rp_proj:,.0f}"
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    st.caption("Passport revenue estimated at $100/passport (Ordinary + Service). Diplomatic passports fee-exempt. Source: SLID official fee schedule.")

# ═══════════════════════════════════════════════════════════
# TAB 6 — PREDICTIVE ANALYTICS
# ═══════════════════════════════════════════════════════════
elif page == "🔮 Predictive Analytics":

    st.markdown("### Predictive Analytics — Application Completion Predictor")
    st.markdown("This tool uses a trained logistic regression model (AUC = 0.867, Accuracy = 82.7%) "
                "to predict whether a residency permit application is likely to be delivered.")

    if lr_model is None:
        st.error("Model files not found. Please ensure all .joblib files are in the same folder as app.py")
        st.stop()

    st.divider()
    col1, col2 = st.columns([1,1])

    with col1:
        section("Application Input")
        cat_input  = st.selectbox("Permit Category",
                                  meta.get("categories", ["Category B"]))
        proc_input = st.selectbox("Process Code",
                                  meta.get("process_codes", ["Resident Permit"]))
        amt_input  = st.slider("Payment Amount ($)",
                               int(meta.get("amount_min",0)),
                               int(meta.get("amount_max",1000)),
                               int(meta.get("amount_mean",500)), 50)
        month_input = st.selectbox("Month of Application", list(range(1,13)),
                                   format_func=lambda x: ["Jan","Feb","Mar","Apr",
                                   "May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"][x-1],
                                   index=5)
        dow_input  = st.selectbox("Day of Week",
                                  ["Monday","Tuesday","Wednesday",
                                   "Thursday","Friday","Saturday"],
                                  index=0)
        dow_map    = {"Monday":0,"Tuesday":1,"Wednesday":2,
                      "Thursday":3,"Friday":4,"Saturday":5}
        expiry_input = st.slider("Expected Permit Duration (days)", 30, 400, 364, 1)
        card_issued  = st.radio("Card Number Assigned?", ["Yes","No"], horizontal=True)

        predict_btn = st.button("🔮 Predict Completion", use_container_width=True)

    with col2:
        section("Prediction Result")
        if predict_btn:
            try:
                cat_enc  = le_cat.transform([cat_input])[0]
                proc_enc = le_proc.transform([proc_input])[0]
                card_val = 1 if card_issued=="Yes" else 0

                X_input = np.array([[amt_input, month_input,
                                     dow_map[dow_input],
                                     expiry_input, card_val,
                                     cat_enc, proc_enc]])
                X_scaled = scaler.transform(X_input)
                prob_delivered    = lr_model.predict_proba(X_scaled)[0][1]
                prob_not_delivered= lr_model.predict_proba(X_scaled)[0][0]

                if prob_delivered >= 0.75:
                    color_class = "prediction-green"
                    icon = "🟢"
                    verdict = "LOW RISK — Likely to be Delivered"
                    action = "Process normally. No immediate intervention required."
                elif prob_delivered >= 0.50:
                    color_class = "prediction-amber"
                    icon = "🟡"
                    verdict = "MEDIUM RISK — Monitor Closely"
                    action = "Flag for follow-up. Check document completeness. Assign to senior officer."
                else:
                    color_class = "prediction-red"
                    icon = "🔴"
                    verdict = "HIGH RISK — Likely to Stall"
                    action = "Escalate immediately. Verify identity manually. Assign priority review."

                st.markdown(f"""
                <div class="{color_class}">
                    <h2>{icon} {verdict}</h2>
                    <h3>Delivery Probability: {prob_delivered*100:.1f}%</h3>
                    <p><b>Recommended Action:</b> {action}</p>
                </div>""", unsafe_allow_html=True)

                st.divider()

                # Probability gauge
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=prob_delivered*100,
                    title={"text":"Delivery Probability (%)"},
                    gauge={
                        "axis": {"range":[0,100]},
                        "bar" : {"color": C["green"] if prob_delivered>=0.75 else
                                          C["amber"] if prob_delivered>=0.5 else C["red"]},
                        "steps":[
                            {"range":[0,50],  "color":"#FFEBEE"},
                            {"range":[50,75], "color":"#FFF3E0"},
                            {"range":[75,100],"color":"#E8F5E9"},
                        ],
                        "threshold":{
                            "line":{"color":"gray","width":3},
                            "thickness":0.75, "value":74.7
                        }
                    }
                ))
                fig.update_layout(height=320, margin=dict(l=20,r=20,t=40,b=20))
                st.plotly_chart(fig, use_container_width=True)

                # Feature breakdown
                st.markdown("**What is driving this prediction:**")
                coef_df = pd.DataFrame({
                    "Feature"    : ["Amount ($)","Month","Day of Week",
                                    "Days to Expiry","Card Issued",
                                    "Category","Process Code"],
                    "Coefficient": lr_model.coef_[0]
                }).sort_values("Coefficient", ascending=True)

                fig2 = px.bar(
                    coef_df, x="Coefficient", y="Feature",
                    orientation="h", color="Coefficient",
                    color_continuous_scale="RdYlGn",
                    title="Feature Influence on Delivery Probability"
                )
                fig2.update_layout(height=320, showlegend=False,
                                   margin=dict(l=0,r=0,t=40,b=0))
                st.plotly_chart(fig2, use_container_width=True)

            except Exception as e:
                st.error(f"Prediction error: {e}. Check that model files match the trained features.")

        else:
            st.info("Fill in the application details on the left and click **Predict Completion**.")

            # Model performance summary
            st.markdown("**Model Performance Summary**")
            perf = pd.DataFrame({
                "Metric": ["Accuracy","ROC-AUC","Precision (Delivered)",
                           "Recall (Delivered)","Recall (Not Delivered)","Training Size"],
                "Value" : ["82.7%","0.867","85%","93%","51%","8,894 records"]
            })
            st.dataframe(perf, use_container_width=True, hide_index=True)

            st.divider()
            section("Cluster-Based Applicant Segmentation")
            cluster_df = pd.DataFrame({
                "Cluster"       : ["Cluster 0","Cluster 1","Cluster 2","Cluster 3"],
                "Size"          : [2934, 6104, 1649, 373],
                "Avg Fee ($)"   : [225, 709, 744, 0],
                "Delivery Rate" : ["67%","100%","0%","47%"],
                "Revenue at Risk": ["$0","$0","$1,226,800","$0"],
                "Profile"       : [
                    "Low-fee, Category E — NGOs, Diplomatic",
                    "High-fee, Category B — Core productive segment",
                    "High-fee, recent backlog — June/July submissions",
                    "Zero-fee — Diplomatic exemptions"
                ]
            })
            st.dataframe(cluster_df, use_container_width=True, hide_index=True)

            fig3 = px.scatter(
                cluster_df,
                x="Avg Fee ($)",
                y=[67,100,0,47],
                size="Size", color="Cluster",
                text="Cluster",
                size_max=60,
                color_discrete_sequence=[C["amber"],C["green"],C["red"],C["purple"]],
                labels={"y":"Delivery Rate (%)","x":"Average Fee ($)"}
            )
            fig3.update_traces(textposition="top center")
            fig3.update_layout(height=380, showlegend=False,
                               margin=dict(l=0,r=0,t=20,b=0))
            st.plotly_chart(fig3, use_container_width=True)
