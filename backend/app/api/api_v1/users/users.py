from fastapi import APIRouter

from app.api.depends.authentication.fastapi_users import fastapi_users
from app.core.config import settings
from app.entities._auth.schemas import UserRead, UserUpdate

router = APIRouter(
    prefix=settings.api_config.users,
    tags=["Users"],
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=True),
)
