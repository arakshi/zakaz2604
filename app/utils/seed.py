from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.models import Client, Deal, DealStage, Notification, Role, Task, User


def seed_data(db: Session) -> None:
    if db.query(Role).count() > 0:
        return

    roles = {name: Role(name=name) for name in ["head", "manager", "analyst"]}
    db.add_all(roles.values())
    db.flush()

    users = [
        User(full_name="Иван Руководитель", email="head@example.com", password_hash=hash_password("password"), role_id=roles["head"].id),
        User(full_name="Мария Менеджер", email="manager@example.com", password_hash=hash_password("password"), role_id=roles["manager"].id),
        User(full_name="Олег Аналитик", email="analyst@example.com", password_hash=hash_password("password"), role_id=roles["analyst"].id),
    ]
    db.add_all(users)
    db.flush()

    stages = ["Лид", "Квалификация", "Коммерческое предложение", "Переговоры", "Закрыта"]
    stage_objects = [DealStage(name=name, sort_order=i) for i, name in enumerate(stages, 1)]
    db.add_all(stage_objects)
    db.flush()

    clients = []
    for i in range(1, 16):
        clients.append(
            Client(
                company_name=f"Компания {i}",
                contact_person=f"Контакт {i}",
                phone=f"+79990000{i:03}",
                email=f"client{i}@mail.ru",
                segment="B2B",
                source="Сайт",
            )
        )
    db.add_all(clients)
    db.flush()

    deals = []
    for i in range(1, 26):
        deals.append(
            Deal(
                title=f"Сделка {i}",
                client_id=clients[(i - 1) % len(clients)].id,
                manager_id=users[1].id,
                stage_id=stage_objects[i % len(stage_objects)].id,
                amount=100000 + i * 5000,
                probability=0.2 + (i % 5) * 0.15,
                planned_close_date=date.today() + timedelta(days=i - 10),
                status="won" if i % 6 == 0 else "active",
            )
        )
    db.add_all(deals)
    db.flush()

    for i in range(1, 21):
        db.add(
            Task(
                title=f"Задача {i}",
                description="Связаться с клиентом",
                assigned_to=users[1].id,
                related_deal_id=deals[(i - 1) % len(deals)].id,
                due_date=date.today() + timedelta(days=i - 12),
                status="new",
                priority="high" if i % 2 == 0 else "medium",
            )
        )

    for i in range(1, 11):
        db.add(Notification(user_id=users[1].id, text=f"Уведомление {i}", type="info"))

    db.commit()
