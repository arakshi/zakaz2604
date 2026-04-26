from app.core.database import SessionLocal
from app.utils.seed import seed_data

if __name__ == "__main__":
    with SessionLocal() as db:
        seed_data(db)
    print("Демо-данные загружены")
