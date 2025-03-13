from typing import Any, Optional, Sequence, Type

from pydantic import BaseModel
from sqlalchemy import MetaData, Select, inspect, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    joinedload,
    lazyload,
    selectinload,
    subqueryload,
)

from app.core.config import settings
from app.core.exceptions import InvalidLoadStrategyException, NotFoundException
from app.core.logging_config import get_logger
from app.utils.case_converter import camel_case_to_snake_case
from app.utils.pagination import PaginationParamsDep

logger = get_logger(__name__)


# INFO: sqlalchemy
class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.database.naming_convention,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"


# INFO: pydantic
class CustomBaseModel(BaseModel):
    class Config:
        from_attributes = True


class BaseRepository:
    def __init__(self, sql_model: Type[Any]) -> None:
        self.sql_model = sql_model

    def _apply_load_strategy(
        self, stmt: Select, load_strategy: Optional[str] = None
    ) -> Select:
        model_relations = inspect(self.sql_model).relationships.keys()
        if not model_relations or load_strategy is None:
            return stmt

        load_methods = {
            "selectin": selectinload,
            "joined": joinedload,
            "subquery": subqueryload,
            "lazy": lazyload,
        }

        if load_strategy not in load_methods:
            logger.error(f"Invalid load strategy: {load_strategy}.")
            raise InvalidLoadStrategyException(load_strategy, load_methods.keys())

        load_method = load_methods[load_strategy]
        options = [
            load_method(getattr(self.sql_model, relation))
            for relation in model_relations
        ]

        return stmt.options(*options)

    def _apply_pagination(
        self, stmt: Select, pagination: PaginationParamsDep
    ) -> Select:
        if pagination.order_by and hasattr(self.sql_model, pagination.order_by):
            order_clause = getattr(self.sql_model, pagination.order_by)
            stmt = stmt.order_by(
                order_clause.desc() if pagination.desc else order_clause
            )

        return stmt.offset(pagination.offset).limit(pagination.limit)

    async def get_by_id(
        self, session: AsyncSession, id: int, load_strategy: Optional[str] = None
    ):
        stmt = select(self.sql_model).where(self.sql_model.id == id)

        if load_strategy is not None:
            stmt = self._apply_load_strategy(stmt, load_strategy)
        result = await session.execute(stmt)
        entity = result.scalars().first()

        if entity is None:
            logger.error(f"Entity {self.sql_model.__name__} with id:{id} wasn't found")
            raise NotFoundException(self.sql_model.__name__, id)

        return entity

    async def list_all(
        self,
        session: AsyncSession,
        pagination: PaginationParamsDep,
        load_strategy: Optional[str] = None,
    ) -> Sequence[Any]:
        stmt = select(self.sql_model)
        stmt = self._apply_load_strategy(stmt, load_strategy)
        stmt = self._apply_pagination(stmt, pagination)

        result = await session.execute(stmt)
        entities = result.scalars().unique().all()
        return entities
