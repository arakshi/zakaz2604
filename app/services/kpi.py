from datetime import date

import pandas as pd
from sqlalchemy.orm import Session

from app.models.models import Deal, DealStage, User


def dashboard_metrics(db: Session, manager_id: int | None = None) -> dict:
    query = db.query(Deal)
    if manager_id:
        query = query.filter(Deal.manager_id == manager_id)
    deals = query.all()
    if not deals:
        return {"deals_count": 0, "active_amount": 0, "closed_amount": 0}

    rows = [{"status": d.status, "amount": float(d.amount)} for d in deals]
    df = pd.DataFrame(rows)
    return {
        "deals_count": int(df.shape[0]),
        "active_amount": float(df[df["status"] == "active"]["amount"].sum()),
        "closed_amount": float(df[df["status"] == "won"]["amount"].sum()),
    }


def funnel_metrics(db: Session, manager_id: int | None = None) -> list[dict]:
    query = db.query(Deal, DealStage).join(DealStage, Deal.stage_id == DealStage.id)
    if manager_id:
        query = query.filter(Deal.manager_id == manager_id)
    data = query.all()
    rows = [{"stage": s.name, "amount": float(d.amount)} for d, s in data]
    if not rows:
        return []
    df = pd.DataFrame(rows)
    grouped = df.groupby("stage", as_index=False).agg(count=("stage", "count"), amount=("amount", "sum"))
    return grouped.to_dict(orient="records")


def manager_kpi(db: Session) -> list[dict]:
    users = db.query(User).all()
    result = []
    for user in users:
        if user.role.name not in {"manager", "head"}:
            continue
        metrics = dashboard_metrics(db, manager_id=user.id)
        all_deals = metrics["deals_count"]
        won_count = db.query(Deal).filter(Deal.manager_id == user.id, Deal.status == "won").count()
        conv = (won_count / all_deals * 100) if all_deals else 0.0
        result.append(
            {
                "manager": user.full_name,
                "deals_count": all_deals,
                "closed_amount": metrics["closed_amount"],
                "conversion_rate": round(conv, 2),
            }
        )
    return result


def deal_overdue(planned_close_date: date) -> bool:
    return planned_close_date < date.today()
