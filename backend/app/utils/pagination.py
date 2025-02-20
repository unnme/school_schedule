from fastapi import Query

from app.core.base import PaginationParamsModel


def pagination_params(
    offset: int = Query(0, ge=0, description="Смещение для пагинации"),
    limit: int = Query(
        10, ge=1, le=100, description="Количество элементов на странице"
    ),
    order_by: str | None = Query(None, description="Поле для сортировки"),
    desc: bool = Query(False, description="Сортировка по убыванию"),
) -> PaginationParamsModel:
    return PaginationParamsModel(
        offset=offset, limit=limit, order_by=order_by, desc=desc
    )


