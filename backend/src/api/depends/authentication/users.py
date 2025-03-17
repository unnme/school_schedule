from fastapi_users.db import SQLAlchemyUserDatabase

from src.core.depends import AsyncSessionDep
from src.entities._auth.models import User


async def get_user_db(session: AsyncSessionDep):
    yield SQLAlchemyUserDatabase(session, User)
