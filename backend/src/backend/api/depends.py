from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.logging_config import get_logger
from backend.core.database import session_manager


logger = get_logger(__name__)


AsyncSessionDep = Annotated[AsyncSession, Depends(session_manager.get_async_session)]
