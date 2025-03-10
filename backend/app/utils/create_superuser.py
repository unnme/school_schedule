from contextlib import asynccontextmanager

from app.core.depends import get_user_db
from app.core.depends import get_user_manager
from app.core.database import session_manager
from app.entities.user.schemas import UserCreate
from app.entities.user.services import UserManager
from app.entities.user.models import User
from app.core.config import settings


get_users_db_context = asynccontextmanager(get_user_db)
get_user_manager_context = asynccontextmanager(get_user_manager)


async def create_user(
    user_manager: UserManager,
    user_create: UserCreate,
) -> User:
    user = await user_manager.create(
        user_create=user_create,
        safe=False, #NOTE: delfault = False! change this for regular user
    )
    return user


async def create_superuser():
    user_create = UserCreate(
        email=settings.base.SUPERUSER_MAIL,
        password=settings.base.SUPERUSER_PASS,
        is_active=True,
        is_superuser=True,
        is_verified=True,
    )
    async for session in session_manager.get_async_session():
        async with get_users_db_context(session) as users_db:
            async with get_user_manager_context(users_db) as user_manager:
                return await create_user(
                    user_manager=user_manager,
                    user_create=user_create,
                )
