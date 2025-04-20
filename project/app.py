from contextlib import asynccontextmanager
from broadcaster import Broadcast
from fastapi import FastAPI

from project.celery_utils import create_celery
from project.config import settings
from project.users.router import users_router
from project.users import tasks


broadcast = Broadcast(settings.WS_MESSAGE_QUEUE)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broadcast.connect()
    yield
    await broadcast.disconnect()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)

    app.celery_app = create_celery()

    app.include_router(users_router)

    from project.ws.router import ws_router

    app.include_router(ws_router)

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app
