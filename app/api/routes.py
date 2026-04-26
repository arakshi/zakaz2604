from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_roles
from app.core.security import create_access_token, verify_password
from app.models.models import Client, Deal, DealStage, Notification, Task, User
from app.schemas.common import (
    ClientIn,
    ClientOut,
    DealIn,
    DealOut,
    LoginIn,
    NotificationOut,
    TaskIn,
    TaskOut,
    TokenOut,
    UserOut,
)
from app.services.access import assert_can_edit_deal, can_read_deal
from app.services.importer import import_clients, import_deals
from app.services.kpi import dashboard_metrics, funnel_metrics, manager_kpi
from app.services.notifications import create_notification

router = APIRouter()


@router.post("/auth/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")
    return TokenOut(access_token=create_access_token(user.email))




@router.post("/auth/token", response_model=TokenOut)
def token_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Неверные учетные данные")
    return TokenOut(access_token=create_access_token(user.email))

@router.get("/users/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user


@router.get("/clients", response_model=list[ClientOut])
def list_clients(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Client).all()


@router.post("/clients", response_model=ClientOut)
def create_client(payload: ClientIn, db: Session = Depends(get_db), _: User = Depends(require_roles("head", "manager"))):
    obj = Client(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get("/clients/{item_id}", response_model=ClientOut)
def get_client(item_id: int, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    obj = db.query(Client).filter(Client.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Клиент не найден")
    return obj


@router.put("/clients/{item_id}", response_model=ClientOut)
def update_client(item_id: int, payload: ClientIn, db: Session = Depends(get_db), _: User = Depends(require_roles("head", "manager"))):
    obj = db.query(Client).filter(Client.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Клиент не найден")
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/clients/{item_id}")
def delete_client(item_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles("head"))):
    obj = db.query(Client).filter(Client.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Клиент не найден")
    db.delete(obj)
    db.commit()
    return {"ok": True}


@router.get("/deals", response_model=list[DealOut])
def list_deals(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(Deal)
    if user.role.name == "manager":
        query = query.filter(Deal.manager_id == user.id)
    return query.all()


@router.post("/deals", response_model=DealOut)
def create_deal(payload: DealIn, db: Session = Depends(get_db), _: User = Depends(require_roles("head", "manager"))):
    first_stage = db.query(DealStage).order_by(DealStage.sort_order.asc()).first()
    if not first_stage:
        raise HTTPException(500, "Не найдены этапы воронки")
    obj = Deal(**payload.model_dump(), stage_id=first_stage.id)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    create_notification(db, obj.manager_id, f"Вам назначена сделка: {obj.title}", "assignment")
    return obj


@router.get("/deals/{item_id}", response_model=DealOut)
def get_deal(item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    obj = db.query(Deal).filter(Deal.id == item_id).first()
    if not obj or not can_read_deal(user, obj):
        raise HTTPException(404, "Сделка не найдена")
    return obj


@router.put("/deals/{item_id}", response_model=DealOut)
def update_deal(item_id: int, payload: DealIn, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    obj = db.query(Deal).filter(Deal.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Сделка не найдена")
    assert_can_edit_deal(user, obj)
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/deals/{item_id}")
def delete_deal(item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    obj = db.query(Deal).filter(Deal.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Сделка не найдена")
    assert_can_edit_deal(user, obj)
    db.delete(obj)
    db.commit()
    return {"ok": True}


@router.patch("/deals/{item_id}/stage")
def patch_stage(item_id: int, stage_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    obj = db.query(Deal).filter(Deal.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Сделка не найдена")
    assert_can_edit_deal(user, obj)
    obj.stage_id = stage_id
    db.commit()
    return {"ok": True}


@router.get("/tasks", response_model=list[TaskOut])
def list_tasks(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(Task)
    if user.role.name == "manager":
        query = query.filter(Task.assigned_to == user.id)
    return query.all()


@router.post("/tasks", response_model=TaskOut)
def create_task(payload: TaskIn, db: Session = Depends(get_db), _: User = Depends(require_roles("head", "manager"))):
    obj = Task(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    create_notification(db, obj.assigned_to, f"Новая задача: {obj.title}", "task")
    return obj


@router.put("/tasks/{item_id}", response_model=TaskOut)
def update_task(item_id: int, payload: TaskIn, db: Session = Depends(get_db), _: User = Depends(require_roles("head", "manager"))):
    obj = db.query(Task).filter(Task.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Задача не найдена")
    for k, v in payload.model_dump().items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete("/tasks/{item_id}")
def delete_task(item_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles("head", "manager"))):
    obj = db.query(Task).filter(Task.id == item_id).first()
    if not obj:
        raise HTTPException(404, "Задача не найдена")
    db.delete(obj)
    db.commit()
    return {"ok": True}


@router.get("/analytics/dashboard")
def analytics_dashboard(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    manager_id = user.id if user.role.name == "manager" else None
    return dashboard_metrics(db, manager_id=manager_id)


@router.get("/analytics/funnel")
def analytics_funnel(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    manager_id = user.id if user.role.name == "manager" else None
    return funnel_metrics(db, manager_id=manager_id)


@router.get("/analytics/kpi")
def analytics_kpi(_: User = Depends(require_roles("head", "analyst")), db: Session = Depends(get_db)):
    return manager_kpi(db)


@router.get("/notifications", response_model=list[NotificationOut])
def list_notifications(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Notification).filter(Notification.user_id == user.id).order_by(Notification.created_at.desc()).all()


@router.patch("/notifications/{item_id}/read")
def read_notification(item_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    obj = db.query(Notification).filter(Notification.id == item_id, Notification.user_id == user.id).first()
    if not obj:
        raise HTTPException(404, "Уведомление не найдено")
    obj.is_read = True
    db.commit()
    return {"ok": True}


@router.post("/import/clients")
def upload_clients(file: UploadFile = File(...), db: Session = Depends(get_db), _: User = Depends(require_roles("head", "analyst"))):
    count = import_clients(db, file.filename, file.file.read())
    return {"imported": count}


@router.post("/import/deals")
def upload_deals(file: UploadFile = File(...), db: Session = Depends(get_db), _: User = Depends(require_roles("head", "analyst"))):
    stage = db.query(DealStage).order_by(DealStage.sort_order.asc()).first()
    if not stage:
        raise HTTPException(500, "Нет этапа по умолчанию")
    count = import_deals(db, file.filename, file.file.read(), stage.id)
    return {"imported": count}


@router.get("/integration/export")
def export_data(user: User = Depends(require_roles("head", "analyst")), db: Session = Depends(get_db)):
    deals = db.query(Deal).all()
    return {
        "exported_by": user.email,
        "deals": [{"id": d.id, "title": d.title, "amount": float(d.amount), "status": d.status} for d in deals],
    }


@router.post("/integration/sync")
def mock_sync(payload: dict, _: User = Depends(require_roles("head"))):
    return {"status": "accepted", "received": payload}
