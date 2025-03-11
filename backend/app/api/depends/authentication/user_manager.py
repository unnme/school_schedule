from fastapi import Depends
from app.api.depends.authentication.users import get_user_db

from app.entities._auth.services import UserManager


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
