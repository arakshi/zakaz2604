from sqlalchemy.orm import Session

from app.models.models import Notification


def create_notification(db: Session, user_id: int, text: str, type_: str = "info") -> Notification:
    obj = Notification(user_id=user_id, text=text, type=type_)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
