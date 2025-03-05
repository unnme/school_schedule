from typing import Optional, Annotated

from fastapi import Query, Depends
from pydantic.dataclasses import dataclass


@dataclass
class PaginationParams:
    offset: int
    limit: int
    order_by: Optional[str]
    desc: bool


def get_pagination(
    offset: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(
        10, ge=1, le=100, description="Number of items per page"
    ),
    order_by: Optional[str] = Query(None, description="Field for sorting"),
    desc: bool = Query(False, description="Sort in descending order"),
) -> PaginationParams:
    return PaginationParams(offset=offset, limit=limit, order_by=order_by, desc=desc)


PaginationParamsDep = Annotated[PaginationParams, Depends(get_pagination)]
