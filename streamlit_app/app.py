import requests
import streamlit as st

st.set_page_config(page_title="Управление продажами", layout="wide")

API_URL = st.sidebar.text_input("URL API", "http://backend:8000")

if "token" not in st.session_state:
    st.session_state.token = None

st.title("Модуль управления продажами")

if not st.session_state.token:
    st.subheader("Вход")
    email = st.text_input("Email", "head@example.com")
    password = st.text_input("Пароль", "password", type="password")
    if st.button("Войти"):
        r = requests.post(f"{API_URL}/auth/login", json={"email": email, "password": password}, timeout=30)
        if r.ok:
            st.session_state.token = r.json()["access_token"]
            st.success("Вход выполнен")
            st.rerun()
        else:
            st.error("Ошибка входа")
else:
    st.success("Авторизация активна. Используйте страницы в боковом меню.")
