from datetime import date

from sqlalchemy.orm import Session

from app.models.models import Deal, Task
from app.services.notifications import create_notification


def mark_overdue_tasks(db: Session) -> int:
    tasks = db.query(Task).filter(Task.due_date < date.today(), Task.status != "done").all()
    for task in tasks:
        task.status = "overdue"
    db.commit()
    return len(tasks)


def notify_close_deadline(db: Session, days: int = 3) -> int:
    deals = db.query(Deal).filter(Deal.status == "active").all()
    counter = 0
    for deal in deals:
        if (deal.planned_close_date - date.today()).days <= days:
            create_notification(db, deal.manager_id, f"Сделка '{deal.title}' скоро к закрытию", "deadline")
            counter += 1
    return counter
