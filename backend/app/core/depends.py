from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from .database import session_manager


AsyncSessionDep = Annotated[AsyncSession, Depends(session_manager.get_async_session)]
