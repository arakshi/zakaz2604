import pandas as pd
import requests
import streamlit as st

st.title("KPI и аналитика")
api = st.sidebar.text_input("URL API", "http://127.0.0.1:8000", key="api_kpi")
token = st.session_state.get("token")
if not token:
    st.warning("Сначала войдите")
    st.stop()

col1, col2 = st.columns(2)
date_from = col1.date_input("Период с", value=None, key="kpi_from")
date_to = col2.date_input("Период по", value=None, key="kpi_to")

params = {}
if date_from:
    params["date_from"] = str(date_from)
if date_to:
    params["date_to"] = str(date_to)

headers = {"Authorization": f"Bearer {token}"}

kpi = requests.get(f"{api}/analytics/kpi", headers=headers, params=params, timeout=30)
if kpi.ok:
    df = pd.DataFrame(kpi.json())
    st.subheader("KPI менеджеров")
    st.dataframe(df)
    if not df.empty:
        st.bar_chart(df.set_index("manager")[["closed_amount", "avg_deal_amount"]])


daily = requests.get(f"{api}/analytics/daily", headers=headers, params=params, timeout=30)
if daily.ok:
    ddf = pd.DataFrame(daily.json())
    if not ddf.empty:
        st.subheader("Дневная динамика")
        st.line_chart(ddf.set_index("day")[["deals_count", "total_amount"]])
