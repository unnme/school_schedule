from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase

from app.core.depends import AsyncSessionDep
from app.entities._auth.models import AccessToken


async def get_access_token_db(
    session: AsyncSessionDep,
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
