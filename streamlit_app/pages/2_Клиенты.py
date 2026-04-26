import pandas as pd
import requests
import streamlit as st

st.title("Клиенты")
api = st.sidebar.text_input("URL API", "http://backend:8000", key="api_clients")
token = st.session_state.get("token")
if not token:
    st.warning("Сначала войдите")
    st.stop()
headers = {"Authorization": f"Bearer {token}"}

clients = requests.get(f"{api}/clients", headers=headers, timeout=30).json()
if clients:
    df = pd.DataFrame(clients)
    q = st.text_input("Поиск по компании")
    if q:
        df = df[df["company_name"].str.contains(q, case=False)]
    st.dataframe(df)
