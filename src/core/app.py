import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from core.config import Settings, get_settings
from infrastructure.telegram import bot
from api.controllers import routers_v1


def create_lifespan(settings: Settings):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.pooling_task = asyncio.create_task(bot.start_pooling())

        yield

        app.state.pooling_task.cancel()

    return lifespan


def register_routers(app: FastAPI):
    app.include_router(routers_v1)


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title="Telega",
        docs_url="/docs",
        openapi_url="/openapi.json",
        lifespan=create_lifespan(settings),
    )

    register_routers(app)

    return app
