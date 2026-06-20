import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
import os

st.set_page_config(page_title="FraudLens", page_icon="🔍", layout="wide")

@st.cache_resource
def get_engine():
    db_url = os.getenv("DATABASE_URL", "postgresql://fraud_user:fraud_pass@localhost:5432/fraudlens")
    return create_engine(db_url)

@st.cache_data(ttl=60)
def query(sql):
    return pd.read_sql(sql, get_engine())

# ── Header ────────────────────────────────────────────────────────────────────
st.title("🔍 FraudLens — Fraud Analytics Dashboard")
st.markdown("Rule-based anomaly detection · PostgreSQL · Streamlit")
st.divider()

# ── KPI Cards ────────────────────────────────────────────────────────────────
kpi = query("""
    SELECT
        COUNT(*)                              AS total_flags,
        COUNT(DISTINCT customer_id)           AS flagged_customers,
        SUM(CASE WHEN reviewed THEN 1 END)    AS reviewed,
        SUM(CASE WHEN NOT reviewed THEN 1 END) AS pending
    FROM fraud_flags
""").iloc[0]

c1, c2, c3, c4 = st.columns(4)
c1.metric("🚨 Total Flags",        f"{kpi['total_flags']:,}")
c2.metric("👤 Flagged Customers",  f"{kpi['flagged_customers']:,}")
c3.metric("✅ Reviewed",           f"{kpi['reviewed']:,}")
c4.metric("⏳ Pending Review",     f"{kpi['pending']:,}")

st.divider()

col1, col2 = st.columns(2)

# ── Fraud Trend ───────────────────────────────────────────────────────────────
with col1:
    st.subheader("📈 Daily Fraud Flags Trend")
    trend_df = query("""
        SELECT flagged_at::DATE AS date, COUNT(*) AS flags
        FROM fraud_flags
        GROUP BY 1 ORDER BY 1
    """)
    fig1 = px.line(trend_df, x="date", y="flags", markers=True,
                   color_discrete_sequence=["#E74C3C"])
    st.plotly_chart(fig1, use_container_width=True)

# ── Rule Breakdown ────────────────────────────────────────────────────────────
with col2:
    st.subheader("⚡ Rule Trigger Breakdown")
    rule_df = query("""
        SELECT rule_triggered, COUNT(*) AS count
        FROM fraud_flags
        GROUP BY 1 ORDER BY 2 DESC
    """)
    fig2 = px.bar(rule_df, x="rule_triggered", y="count",
                  color="count", color_continuous_scale="Reds")
    st.plotly_chart(fig2, use_container_width=True)

# ── High-Risk Accounts ────────────────────────────────────────────────────────
st.subheader("🔴 High-Risk Accounts")
risk_df = query("""
    SELECT customer_id, COUNT(*) AS total_flags, MAX(risk_score) AS max_risk_score
    FROM fraud_flags
    WHERE reviewed = FALSE
    GROUP BY customer_id
    ORDER BY total_flags DESC
    LIMIT 20
""")
st.dataframe(risk_df, use_container_width=True)

# ── Transaction Heatmap ───────────────────────────────────────────────────────
st.subheader("🕐 Fraud by Hour of Day")
hour_df = query("""
    SELECT EXTRACT(HOUR FROM flagged_at) AS hour, COUNT(*) AS flags
    FROM fraud_flags
    GROUP BY 1 ORDER BY 1
""")
fig3 = px.bar(hour_df, x="hour", y="flags",
              title="Flagged Transactions by Hour",
              color="flags", color_continuous_scale="OrRd")
st.plotly_chart(fig3, use_container_width=True)

st.caption("FraudLens · Built by Kishoor · Refreshes every 60 seconds")
