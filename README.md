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


## Если не получается войти
- Для Streamlit используйте: `head@example.com / password` (или `manager@example.com / password`, `analyst@example.com / password`).
- В Swagger (`/docs`) кнопка **Authorize** использует endpoint `/auth/token`: в поле `username` вводите **email** пользователя, в поле `password` — пароль.
- Если вручную вызываете `/auth/login`, отправляйте JSON вида `{"email": "head@example.com", "password": "password"}`.
- Если запускали старые версии проекта и логин не проходит, удалите файл `sales.db` и перезапустите backend (demo-пользователи будут созданы заново).


### Быстрая диагностика (если "ничего не работает")
1. Откройте `http://127.0.0.1:8000/health` — должен вернуться `{"status":"ok"}`.
2. Откройте `http://127.0.0.1:8000/auth/demo-users` — должны быть demo-пользователи.
3. Для входа используйте `POST /auth/login` с JSON:
   `{"email":"head@example.com","password":"password"}`
   (также поддерживается `{"username":"head@example.com","password":"password"}`).
4. Если список пользователей пустой или пароль не подходит — удалите `sales.db` и перезапустите `python -m app.main`.
