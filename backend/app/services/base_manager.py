import logging
from typing import Any, Optional, Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, lazyload, selectinload, subqueryload
from sqlalchemy import inspect, select

from app.core.depends import PaginationParamsModel
from app.core.exceptions import NotFoundException

logger = logging.getLogger(__name__)


# =========== БАЗОВЫЙ МЕНЕДЖЕР =============
class BaseManager:
    model = None

    @classmethod
    def _get_model(cls) -> Type[Any]:
        if cls.model is None:
            raise ValueError(f"{cls.__name__}: model is not defined")
        return cls.model

    @classmethod
    def _apply_load_strategy(cls, load_strategy: Optional[str] = None):
        stmt = select(cls._get_model())

        model_relations = inspect(cls._get_model()).relationships.keys()
        if not model_relations or load_strategy is None:
            return stmt

        load_methods = {
            "selectin": selectinload,
            "joined": joinedload,
            "subquery": subqueryload,
            "lazy": lazyload,
        }

        if load_strategy not in load_methods:
            logger.error(
                f"Неверный формат загрузки моделей: {load_strategy}. Допустимые значения: {list(load_methods.keys())}"
            )
            return stmt

        load_method = load_methods[load_strategy]
        options = [
            load_method(getattr(cls._get_model(), relation))
            for relation in model_relations
        ]

        return stmt.options(*options)

    @classmethod
    def _apply_pagination(cls, stmt, pagination: PaginationParamsModel):
        if pagination.order_by and hasattr(cls.model, pagination.order_by):
            order_clause = getattr(cls.model, pagination.order_by)
            stmt = stmt.order_by(
                order_clause.desc() if pagination.desc else order_clause
            )

        return stmt.offset(pagination.offset).limit(pagination.limit)

    @classmethod
    async def get_by_id(cls, db: AsyncSession, id: int, load_strategy="selectin"):
        stmt = cls._apply_load_strategy(load_strategy).where(cls._get_model().id == id)
        result = await db.execute(stmt)
        entity = result.scalars().first()

        if entity is None:
            raise NotFoundException(cls._get_model().__name__, id)

        return entity

    @classmethod
    async def list_all(
        cls,
        db: AsyncSession,
        pagination: PaginationParamsModel,
        load_stategy: Optional[str] = None,
    ):
        stmt = cls._apply_load_strategy(load_stategy)
        stmt = cls._apply_pagination(stmt, pagination)

        result = await db.execute(stmt)
        entities = result.scalars().unique().all()
        return entities
