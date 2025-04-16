from typing import Optional

from fastapi import Query
from pydantic.dataclasses import dataclass

from backend.core.config import settings


@dataclass
class PaginationParams:
    offset: int
    limit: int
    order_by: Optional[str]
    desc: bool


def get_pagination(
    offset: int = Query(0, ge=0, description="Смещение для пагинации"),
    limit: int = Query(
        10, ge=1, le=settings.api_config.PAGINATION_LIMIT, description="Количество элементов на странице"
    ),
    order_by: Optional[str] = Query("id", description="Поле для сортировки"),
    desc: bool = Query(False, description="Сортировка по убыванию"),
) -> PaginationParams:
    return PaginationParams(offset=offset, limit=limit, order_by=order_by, desc=desc)
