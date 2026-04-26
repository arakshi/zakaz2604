import pandas as pd
import requests
import streamlit as st

st.title("Задачи")
api = st.sidebar.text_input("URL API", "http://127.0.0.1:8000", key="api_tasks")
token = st.session_state.get("token")
if not token:
    st.warning("Сначала войдите")
    st.stop()
headers = {"Authorization": f"Bearer {token}"}

tasks = requests.get(f"{api}/tasks", headers=headers, timeout=30).json()
if tasks:
    df = pd.DataFrame(tasks)
    st.dataframe(df)
