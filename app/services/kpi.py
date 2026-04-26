from datetime import date

import pandas as pd
from sqlalchemy.orm import Session

from app.models.models import Deal, DealStage, User


def _deals_df(db: Session, manager_id: int | None = None, date_from: date | None = None, date_to: date | None = None) -> pd.DataFrame:
    query = db.query(Deal)
    if manager_id:
        query = query.filter(Deal.manager_id == manager_id)
    if date_from:
        query = query.filter(Deal.created_at >= date_from)
    if date_to:
        query = query.filter(Deal.created_at <= date_to)

    deals = query.all()
    if not deals:
        return pd.DataFrame(columns=["id", "status", "amount", "created_at", "planned_close_date", "manager_id", "stage_id"])

    return pd.DataFrame(
        [
            {
                "id": d.id,
                "status": d.status,
                "amount": float(d.amount),
                "created_at": pd.to_datetime(d.created_at),
                "planned_close_date": pd.to_datetime(d.planned_close_date),
                "manager_id": d.manager_id,
                "stage_id": d.stage_id,
            }
            for d in deals
        ]
    )


def dashboard_metrics(db: Session, manager_id: int | None = None, date_from: date | None = None, date_to: date | None = None) -> dict:
    df = _deals_df(db, manager_id, date_from, date_to)
    if df.empty:
        return {"deals_count": 0, "active_amount": 0, "closed_amount": 0, "avg_deal_amount": 0}

    return {
        "deals_count": int(df.shape[0]),
        "active_amount": float(df[df["status"] == "active"]["amount"].sum()),
        "closed_amount": float(df[df["status"] == "won"]["amount"].sum()),
        "avg_deal_amount": float(df["amount"].mean()),
    }


def funnel_metrics(db: Session, manager_id: int | None = None, date_from: date | None = None, date_to: date | None = None) -> list[dict]:
    query = db.query(Deal, DealStage).join(DealStage, Deal.stage_id == DealStage.id)
    if manager_id:
        query = query.filter(Deal.manager_id == manager_id)
    if date_from:
        query = query.filter(Deal.created_at >= date_from)
    if date_to:
        query = query.filter(Deal.created_at <= date_to)

    data = query.all()
    rows = [{"stage": s.name, "amount": float(d.amount)} for d, s in data]
    if not rows:
        return []
    df = pd.DataFrame(rows)
    grouped = df.groupby("stage", as_index=False).agg(count=("stage", "count"), amount=("amount", "sum"))
    return grouped.to_dict(orient="records")


def manager_kpi(db: Session, date_from: date | None = None, date_to: date | None = None) -> list[dict]:
    users = db.query(User).all()
    result = []
    for user in users:
        if user.role.name not in {"manager", "head"}:
            continue
        metrics = dashboard_metrics(db, manager_id=user.id, date_from=date_from, date_to=date_to)
        all_deals = metrics["deals_count"]
        won_count_query = db.query(Deal).filter(Deal.manager_id == user.id, Deal.status == "won")
        if date_from:
            won_count_query = won_count_query.filter(Deal.created_at >= date_from)
        if date_to:
            won_count_query = won_count_query.filter(Deal.created_at <= date_to)
        won_count = won_count_query.count()
        conv = (won_count / all_deals * 100) if all_deals else 0.0
        result.append(
            {
                "manager": user.full_name,
                "deals_count": all_deals,
                "closed_amount": metrics["closed_amount"],
                "avg_deal_amount": round(metrics["avg_deal_amount"], 2),
                "conversion_rate": round(conv, 2),
            }
        )
    return result


def monthly_analytics(db: Session, manager_id: int | None = None, date_from: date | None = None, date_to: date | None = None) -> list[dict]:
    df = _deals_df(db, manager_id, date_from, date_to)
    if df.empty:
        return []
    df["month"] = df["created_at"].dt.to_period("M").astype(str)
    grouped = df.groupby("month", as_index=False).agg(
        deals_count=("id", "count"),
        total_amount=("amount", "sum"),
        won_amount=("amount", lambda s: s[df.loc[s.index, "status"] == "won"].sum()),
    )
    return grouped.to_dict(orient="records")


def daily_analytics(db: Session, manager_id: int | None = None, date_from: date | None = None, date_to: date | None = None) -> list[dict]:
    df = _deals_df(db, manager_id, date_from, date_to)
    if df.empty:
        return []
    df["day"] = df["created_at"].dt.date.astype(str)
    grouped = df.groupby("day", as_index=False).agg(deals_count=("id", "count"), total_amount=("amount", "sum"))
    return grouped.to_dict(orient="records")


def deal_overdue(planned_close_date: date) -> bool:
    return planned_close_date < date.today()
