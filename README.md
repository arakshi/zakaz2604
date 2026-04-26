# Прототип модуля «Управление продажами»

Учебно-практический прототип для дипломного проекта: FastAPI + Streamlit + PostgreSQL/SQLite + Redis.

## Запуск в PyCharm (основной сценарий)

1. Откройте проект в PyCharm.
2. Создайте `.env` на основе `.env.example`.
3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Запустите backend (можно прямо через `main.py` в PyCharm):

```bash
python -m app.main
```

(альтернатива: `uvicorn app.main:app --reload`)

5. Запустите frontend в отдельном терминале:

```bash
streamlit run streamlit_app/app.py
```

6. Откройте:
- Backend docs: http://127.0.0.1:8000/docs
- Frontend: http://127.0.0.1:8501

## Важно
- `@app.on_event("startup")` заменен на `lifespan`, чтобы убрать DeprecationWarning FastAPI.
- При старте приложения автоматически создаются таблицы и подгружаются демо-данные (если БД пустая).

## Демо-пользователи
- Руководитель: `head@example.com / password`
- Менеджер: `manager@example.com / password`
- Аналитик: `analyst@example.com / password`

## Возможности
- Авторизация и роли.
- CRUD клиентов, сделок и задач.
- KPI, воронка и dashboard.
- Уведомления.
- Импорт CSV/XLSX.
- Интеграционные endpoint'ы `/integration/export` и `/integration/sync`.

## Тесты

```bash
pytest -q
```
