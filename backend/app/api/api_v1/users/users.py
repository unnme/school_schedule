from fastapi import APIRouter, Depends
from app.entities.users.models import User
from app.entities.users.schemas import UserRead, UserUpdate
from app.core.auth import fastapi_users, current_active_user

router = APIRouter()

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=True),
    prefix="/users",
    tags=["users"],
)


@router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
