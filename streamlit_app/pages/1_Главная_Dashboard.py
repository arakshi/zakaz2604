import pandas as pd
import requests
import streamlit as st

st.title("Dashboard")
api = st.sidebar.text_input("URL API", "http://127.0.0.1:8000", key="api_dashboard")
token = st.session_state.get("token")
if not token:
    st.warning("Сначала войдите на главной странице")
    st.stop()

col1, col2 = st.columns(2)
date_from = col1.date_input("Дата с", value=None)
date_to = col2.date_input("Дата по", value=None)

params = {}
if date_from:
    params["date_from"] = str(date_from)
if date_to:
    params["date_to"] = str(date_to)

headers = {"Authorization": f"Bearer {token}"}
metrics = requests.get(f"{api}/analytics/dashboard", headers=headers, params=params, timeout=30).json()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Количество сделок", metrics.get("deals_count", 0))
c2.metric("Сумма активных", round(metrics.get("active_amount", 0), 2))
c3.metric("Сумма закрытых", round(metrics.get("closed_amount", 0), 2))
c4.metric("Средний чек", round(metrics.get("avg_deal_amount", 0), 2))

funnel = requests.get(f"{api}/analytics/funnel", headers=headers, params=params, timeout=30).json()
if funnel:
    df = pd.DataFrame(funnel)
    st.subheader("Воронка продаж")
    st.bar_chart(df.set_index("stage")["count"])
    st.line_chart(df.set_index("stage")["amount"])

monthly = requests.get(f"{api}/analytics/monthly", headers=headers, params=params, timeout=30).json()
if monthly:
    mdf = pd.DataFrame(monthly)
    st.subheader("Динамика по месяцам")
    st.bar_chart(mdf.set_index("month")[["deals_count"]])
    st.line_chart(mdf.set_index("month")[["total_amount", "won_amount"]])
