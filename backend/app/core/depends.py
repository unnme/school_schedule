from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyUserDatabase

from app.core.database import session_manager
from app.utils.pagination import PaginationParamsModel, pagination_params
from app.entities.users.models import User
from app.entities.users.services import UserManager


AsyncSessionDep = Annotated[AsyncSession, Depends(session_manager.get_async_session)]
PaginationParamsDep = Annotated[PaginationParamsModel, Depends(pagination_params)]

async def get_user_db(session: AsyncSessionDep):
    yield SQLAlchemyUserDatabase(session, User)

GetUserDBDep = Annotated[SQLAlchemyUserDatabase, Depends(get_user_db)]

async def get_user_manager(user_db: GetUserDBDep):
    yield UserManager(user_db)

