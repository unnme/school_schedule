from typing import Optional, Annotated
from dataclasses import dataclass

from fastapi import Query, Depends


@dataclass
class PaginationParams:
    offset: int = Query(0, ge=0, description="Смещение для пагинации")
    limit: int = Query(10, ge=1, le=100, description="Количество элементов на странице")
    order_by: Optional[str] = Query(None, description="Поле для сортировки")
    desc: bool = Query(False, description="Сортировка по убыванию")

def pagination_params(params: PaginationParams):
    return params

PaginationParamsDep = Annotated[PaginationParams, Depends(pagination_params)]
