# Прототип модуля «Управление продажами»

Учебно-практический прототип для дипломного проекта: FastAPI + Streamlit + PostgreSQL + Redis.

## Запуск в PyCharm / локально

1. Скопируйте `.env.example` в `.env` и при необходимости измените значения.
2. Запустите:

```bash
docker compose up --build
```

3. Сервисы:
- Backend: http://localhost:8000/docs
- Frontend: http://localhost:8501

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
