from fastapi import HTTPException, status

from app.models.models import Deal, User


def can_read_deal(user: User, deal: Deal) -> bool:
    if user.role.name in {"head", "analyst"}:
        return True
    return deal.manager_id == user.id


def can_edit_deal(user: User, deal: Deal) -> bool:
    if user.role.name == "analyst":
        return False
    if user.role.name == "head":
        return True
    return deal.manager_id == user.id


def assert_can_edit_deal(user: User, deal: Deal) -> None:
    if not can_edit_deal(user, deal):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Редактирование сделки запрещено")
