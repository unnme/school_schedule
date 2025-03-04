from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase

from app.core.database import AsyncSessionDep
from app.entities.user.models import User
from app.entities.user.services import UserManager



async def get_user_db(session: AsyncSessionDep):
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
