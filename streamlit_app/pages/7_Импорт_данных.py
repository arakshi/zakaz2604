import requests
import streamlit as st

st.title("Импорт данных")
api = st.sidebar.text_input("URL API", "http://127.0.0.1:8000", key="api_import")
token = st.session_state.get("token")
if not token:
    st.warning("Сначала войдите")
    st.stop()
headers = {"Authorization": f"Bearer {token}"}

file = st.file_uploader("Выберите CSV/XLSX")
entity = st.selectbox("Сущность", ["clients", "deals"])
if file and st.button("Загрузить"):
    r = requests.post(f"{api}/import/{entity}", headers=headers, files={"file": (file.name, file.getvalue())}, timeout=60)
    if r.ok:
        st.success(f"Импортировано: {r.json().get('imported')}")
    else:
        st.error(r.text)
