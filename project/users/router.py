from fastapi import APIRouter

from project.users import models # noqa

users_router = APIRouter(
    prefix="/users"
)
