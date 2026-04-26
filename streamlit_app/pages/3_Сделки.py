import pandas as pd
import requests
import streamlit as st

st.title("Сделки")
api = st.sidebar.text_input("URL API", "http://127.0.0.1:8000", key="api_deals")
token = st.session_state.get("token")
if not token:
    st.warning("Сначала войдите")
    st.stop()
headers = {"Authorization": f"Bearer {token}"}

deals = requests.get(f"{api}/deals", headers=headers, timeout=30).json()
if deals:
    df = pd.DataFrame(deals)
    st.dataframe(df)
