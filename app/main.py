from contextlib import asynccontextmanager
import atexit
import logging
import subprocess
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.api.routes import router
from app.core.config import settings
from app.core.database import Base, SessionLocal, engine
from app.utils.seed import seed_data

logger = logging.getLogger("uvicorn")
STREAMLIT_URL = "http://127.0.0.1:8501"
_streamlit_process: subprocess.Popen | None = None


def _start_streamlit_if_needed() -> None:
    global _streamlit_process
    if _streamlit_process and _streamlit_process.poll() is None:
        return

    project_root = Path(__file__).resolve().parents[1]
    streamlit_app = project_root / "streamlit_app" / "app.py"

    _streamlit_process = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(streamlit_app),
            "--server.port=8501",
            "--server.address=127.0.0.1",
        ],
        cwd=str(project_root),
    )
    logger.info("Интерфейс запущен: %s", STREAMLIT_URL)


def _stop_streamlit() -> None:
    if _streamlit_process and _streamlit_process.poll() is None:
        _streamlit_process.terminate()


def _print_startup_link() -> None:
    logger.info("=" * 70)
    logger.info("ОТКРОЙТЕ ИНТЕРФЕЙС: %s", STREAMLIT_URL)
    logger.info("=" * 70)


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_data(db)
    _print_startup_link()
    yield


app = FastAPI(title="Sales Management Module", lifespan=lifespan)


@app.get("/", include_in_schema=False)
def root_redirect():
    return RedirectResponse(url=STREAMLIT_URL)


@app.get("/ui", include_in_schema=False)
def ui_redirect():
    return RedirectResponse(url=STREAMLIT_URL)


app.include_router(router)


if __name__ == "__main__":
    atexit.register(_stop_streamlit)
    _start_streamlit_if_needed()
    uvicorn.run("app.main:app", host=settings.backend_host, port=settings.backend_port, reload=False)
