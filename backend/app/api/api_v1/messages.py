from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends

from app.entities._auth.models import User
from app.entities._auth.schemas import UserRead
from app.core.config import settings
from app.api.depends.authentication.fastapi_users import current_active_superuser


router = APIRouter(
    prefix=settings.api_config.messages,
    tags=["Messages"],
)


@router.get("/error")
def view_may_raise_error(
    raise_error: bool = False,
):
    if raise_error:
        # 1 / 0
        UserRead.model_validate(None)
    return {"ok": True}


@router.get("")
def get_user_messages(
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    return {
        "messages": ["m1", "m2", "m3"],
        "user": UserRead.model_validate(user),
    }


@router.get("/secrets")
def get_superuser_messages(
    user: Annotated[
        User,
        Depends(current_active_superuser),
    ],
):
    return {
        "messages": ["secret-m1", "secret-m2", "secret-m3"],
        "user": UserRead.model_validate(user),
    }
