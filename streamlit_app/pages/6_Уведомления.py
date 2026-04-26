import pandas as pd
import requests
import streamlit as st

st.title("Уведомления")
api = st.sidebar.text_input("URL API", "http://backend:8000", key="api_notif")
token = st.session_state.get("token")
if not token:
    st.warning("Сначала войдите")
    st.stop()
headers = {"Authorization": f"Bearer {token}"}

notif = requests.get(f"{api}/notifications", headers=headers, timeout=30).json()
if notif:
    st.dataframe(pd.DataFrame(notif))
