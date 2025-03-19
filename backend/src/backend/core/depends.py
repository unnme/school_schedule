from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import session_manager

AsyncSessionDep = Annotated[AsyncSession, Depends(session_manager.get_async_session)]
