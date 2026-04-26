from io import BytesIO

import pandas as pd
from sqlalchemy.orm import Session

from app.models.models import Client, Deal, ImportLog


def _read_df(file_name: str, payload: bytes) -> pd.DataFrame:
    if file_name.endswith(".csv"):
        return pd.read_csv(BytesIO(payload))
    return pd.read_excel(BytesIO(payload))


def import_clients(db: Session, file_name: str, payload: bytes) -> int:
    df = _read_df(file_name, payload)
    required = {"company_name", "contact_person", "phone", "email", "segment", "source"}
    if not required.issubset(df.columns):
        raise ValueError("Некорректные колонки")
    for _, row in df.iterrows():
        db.add(Client(**{k: str(row[k]) for k in required}))
    db.add(ImportLog(file_name=file_name, imported_rows=len(df), status="success"))
    db.commit()
    return len(df)


def import_deals(db: Session, file_name: str, payload: bytes, default_stage_id: int) -> int:
    df = _read_df(file_name, payload)
    required = {"title", "client_id", "manager_id", "amount", "probability", "planned_close_date", "status"}
    if not required.issubset(df.columns):
        raise ValueError("Некорректные колонки")
    for _, row in df.iterrows():
        db.add(
            Deal(
                title=str(row["title"]),
                client_id=int(row["client_id"]),
                manager_id=int(row["manager_id"]),
                stage_id=default_stage_id,
                amount=float(row["amount"]),
                probability=float(row["probability"]),
                planned_close_date=pd.to_datetime(row["planned_close_date"]).date(),
                status=str(row["status"]),
            )
        )
    db.add(ImportLog(file_name=file_name, imported_rows=len(df), status="success"))
    db.commit()
    return len(df)
