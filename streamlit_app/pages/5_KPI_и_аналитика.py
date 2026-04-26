import pandas as pd
import requests
import streamlit as st

st.title("KPI и аналитика")
api = st.sidebar.text_input("URL API", "http://127.0.0.1:8000", key="api_kpi")
token = st.session_state.get("token")
if not token:
    st.warning("Сначала войдите")
    st.stop()
headers = {"Authorization": f"Bearer {token}"}

kpi = requests.get(f"{api}/analytics/kpi", headers=headers, timeout=30)
if kpi.ok:
    df = pd.DataFrame(kpi.json())
    st.dataframe(df)
    if not df.empty:
        st.bar_chart(df.set_index("manager")["closed_amount"])
