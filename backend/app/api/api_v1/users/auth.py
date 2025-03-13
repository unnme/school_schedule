from fastapi import APIRouter

from app.api.depends.authentication.fastapi_users import auth_backend, fastapi_users
from app.core.config import settings
from app.entities._auth.schemas import UserCreate, UserRead

router = APIRouter(
    prefix=settings.api_config.auth,
    tags=["Auth"],
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend, requires_verification=True)  # NOTE: ?!
)
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
router.include_router(fastapi_users.get_reset_password_router())
router.include_router(fastapi_users.get_verify_router(UserRead))
