from contextlib import asynccontextmanager
import logging

import uvicorn
from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from app.utils.seed import seed_data

logger = logging.getLogger("uvicorn")


def _print_startup_links() -> None:
    local_host = "127.0.0.1" if settings.backend_host == "0.0.0.0" else settings.backend_host
    base_url = f"http://{local_host}:{settings.backend_port}"

    logger.info("=" * 70)
    logger.info("МОДУЛЬ УПРАВЛЕНИЯ ПРОДАЖАМИ ЗАПУЩЕН")
    logger.info("API: %s", base_url)
    logger.info("Swagger UI: %s/docs", base_url)
    logger.info("ReDoc: %s/redoc", base_url)
    logger.info("Проверка API: %s/health", base_url)
    logger.info("Демо-пользователи: %s/auth/demo-users", base_url)
    logger.info("Логин JSON: POST %s/auth/login", base_url)
    logger.info("OAuth логин (Swagger Authorize): POST %s/auth/token", base_url)
    logger.info("Streamlit запуск: streamlit run streamlit_app/app.py")
    logger.info("Streamlit URL: http://127.0.0.1:8501")
    logger.info("Демо-аккаунты: head@example.com / password | manager@example.com / password | analyst@example.com / password")
    logger.info("Если не логинится: удалите sales.db и перезапустите backend")
    logger.info("=" * 70)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_data(db)
    _print_startup_links()
    yield


app = FastAPI(title="Sales Management Module", lifespan=lifespan)


@app.get("/")
def root():
    return {"message": "Модуль управления продажами запущен"}


app.include_router(router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=settings.backend_host, port=settings.backend_port, reload=True)
