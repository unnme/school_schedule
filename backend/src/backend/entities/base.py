from typing import Any, Generic, Optional, Sequence, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import MetaData, Select, func, inspect, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    DeclarativeBase,
    class_mapper,
    declared_attr,
    joinedload,
    lazyload,
    selectinload,
    subqueryload,
)

from backend.api.depends import PaginationParamsDep
from backend.core.config import settings
from backend.core.exceptions import (
    DatabaseConnectionError,
    InvalidLoadStrategyException,
    NotFoundException,
    RequestDataMissingException,
)
from backend.core.logging_config import get_logger
from backend.utils.case_converter import camel_case_to_snake_case
from backend.utils.common_utils import get_bound_arguments

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

    def to_dict(self, include_relationships=True, depth=1):
        result = {}

        for column in class_mapper(self.__class__).columns:
            value = getattr(self, column.name)
            result[column.name] = value

        if include_relationships and depth > 0:
            for rel in self.__mapper__.relationships:
                rel_name = rel.key
                relation = getattr(self, rel_name)
                if relation:
                    if isinstance(relation, list):
                        result[rel_name] = [
                            r.to_dict(depth=depth - 1) if hasattr(r, "to_dict") else str(r) for r in relation
                        ]
                    else:
                        result[rel_name] = (
                            relation.to_dict(depth=depth - 1) if hasattr(relation, "to_dict") else str(relation)
                        )
        return result


# INFO: pydantic


class CustomBaseModel(BaseModel):
    class Config:
        from_attributes = True


T = TypeVar("T")


class ListResponseModel(CustomBaseModel, Generic[T]):
    items: Sequence[T]
    total: int
    limit: int
    offset: int


# INFO: BASEs


class BaseRepository:
    def __init__(self, sql_model: Type[Any]) -> None:
        self.sql_model = sql_model

    async def get_by_id(self, session: AsyncSession, id: int, load_strategy: Optional[str] = None):
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
        return result.scalars().unique().all()

    async def entity_count(self, session) -> int:
        count_stmt = select(func.count()).select_from(self.sql_model)
        result = await session.execute(count_stmt)
        return result.scalar()

    def _apply_load_strategy(self, stmt: Select, load_strategy: Optional[str] = None) -> Select:
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
        options = [load_method(getattr(self.sql_model, rel)) for rel in model_relations]
        return stmt.options(*options)

    def _apply_pagination(self, stmt: Select, pagination: PaginationParamsDep) -> Select:
        if pagination.order_by and hasattr(self.sql_model, pagination.order_by):
            order_clause = getattr(self.sql_model, pagination.order_by)
            stmt = stmt.order_by(order_clause.desc() if pagination.desc else order_clause)
        return stmt.offset(pagination.offset).limit(pagination.limit)


class BaseValidator:
    def __init__(self, func, *args, **kwargs):
        bound_args = get_bound_arguments(func, *args, **kwargs)

        if not (session := bound_args.arguments.get("session")):
            raise DatabaseConnectionError()
        else:
            self.session = session

        if not (request_data := bound_args.arguments.get("request_data")):
            raise RequestDataMissingException()
        else:
            self.request_data = request_data

        self.id = next(
            (v for k, v in bound_args.arguments.items() if k.endswith("id")),
            None,
        )
