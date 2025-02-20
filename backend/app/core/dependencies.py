from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.core.database import db_manager
from app.utils.pagination import pagination_params
from app.core.base import PaginationParamsModel


PaginationParams = Annotated[PaginationParamsModel, Depends(pagination_params)]

AsyncSessionDep = Annotated[AsyncSession, Depends(db_manager.get_async_session)]
