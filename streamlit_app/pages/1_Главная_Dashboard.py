import pandas as pd
import requests
import streamlit as st

st.title("Dashboard")
api = st.sidebar.text_input("URL API", "http://127.0.0.1:8000", key="api_dashboard")
token = st.session_state.get("token")
if not token:
    st.warning("Сначала войдите на главной странице")
    st.stop()

headers = {"Authorization": f"Bearer {token}"}
metrics = requests.get(f"{api}/analytics/dashboard", headers=headers, timeout=30).json()

c1, c2, c3 = st.columns(3)
c1.metric("Количество сделок", metrics.get("deals_count", 0))
c2.metric("Сумма активных", round(metrics.get("active_amount", 0), 2))
c3.metric("Сумма закрытых", round(metrics.get("closed_amount", 0), 2))

funnel = requests.get(f"{api}/analytics/funnel", headers=headers, timeout=30).json()
if funnel:
    df = pd.DataFrame(funnel)
    st.bar_chart(df.set_index("stage")["count"])
    st.line_chart(df.set_index("stage")["amount"])
