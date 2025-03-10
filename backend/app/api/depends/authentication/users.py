from fastapi_users.db import SQLAlchemyUserDatabase

from app.core.depends import AsyncSessionDep
from app.entities.auth.models import User


async def get_user_db(session: AsyncSessionDep):
    yield SQLAlchemyUserDatabase(session, User)
