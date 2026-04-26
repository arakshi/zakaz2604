# Прототип модуля «Управление продажами»

## Запуск (одной командой)

```bash
python -m app.main
```

После запуска **в лог выводится одна главная ссылка интерфейса**:

- `http://127.0.0.1:8501`

Открывайте именно её — это интерфейс всей программы (Streamlit), backend поднимается автоматически вместе с ним.

## Демо-вход
- `head@example.com / password`
- `manager@example.com / password`
- `analyst@example.com / password`


## Новое в аналитике
- Фильтрация по периоду `date_from/date_to` для dashboard, funnel и KPI.
- Отдельные endpoint'ы: `/analytics/monthly` (по месяцам) и `/analytics/daily` (по дням).
- На страницах Dashboard и KPI добавлены фильтры периода и дополнительные графики динамики.
