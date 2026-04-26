from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.core.database import Base, SessionLocal, engine
from app.utils.seed import seed_data


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_data(db)
    yield


app = FastAPI(title="Sales Management Module", lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Модуль управления продажами запущен"}


app.include_router(router)
