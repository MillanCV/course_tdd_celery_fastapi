from fastapi import FastAPI

from project.celery_utils import create_celery
from project.users.router import users_router
from project.users import task


def create_app() -> FastAPI:
    app = FastAPI()

    app.celery_app = create_celery()
    
    app.include_router(users_router)
    
    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    return app
