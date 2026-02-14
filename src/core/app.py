from fastapi import FastAPI

from core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Telega",
        docs_url="/docs",
        openapi_url="/openapi.json",
    )

    return app
