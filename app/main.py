from fastapi import FastAPI

from app.api.routes import router
from app.core.database import Base, engine

app = FastAPI(title="Sales Management Module")


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Модуль управления продажами запущен"}


app.include_router(router)
