from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
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


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.backend_host, port=settings.backend_port, reload=True)
