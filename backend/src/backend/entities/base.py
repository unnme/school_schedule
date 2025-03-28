from abc import ABC, abstractmethod
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
from backend.utils.pagination import PaginationParamsDep

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


# INFO: BASEs

class BaseRepository(ABC):
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

    def _get_related_model(self, field_name: str):
        relationship_prop = self.sql_model.__mapper__.relationships.get(field_name)
        if not relationship_prop:
            raise ValueError(f"Не найдено отношение для поля '{field_name}' в модели {self.sql_model.__name__}")

        return relationship_prop.mapper.class_

    async def update_fields(self, session: AsyncSession, id: int, request_data):
        entity = await self.get_by_id(session, id)

        for k, v in request_data.model_dump(exclude_none=True).items():
            if hasattr(entity, k):
                attr = getattr(entity, k)

                if isinstance(attr, list) and isinstance(v, list):  # Если поле — список (многие ко многим или один ко многим)
                    related_model = self._get_related_model(k)  # Получаем модель связанной таблицы
                    existing_items = {item.id: item for item in attr}  # Текущие объекты связи

                    for item_data in v:
                        item_id = item_data.get("id")
                        if item_id and item_id in existing_items:
                            # Обновляем существующий объект
                            for field, value in item_data.items():
                                setattr(existing_items[item_id], field, value)
                        else:
                            # Создаём новый объект и добавляем в список
                            new_item = related_model(**item_data)
                            attr.append(new_item)

                else:
                    setattr(entity, k, v)  # Обычные поля

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

    # @abstractmethod
    # async def create(self, session: AsyncSession, request_data) -> Any:
    #     pass
    #
    # @abstractmethod
    # async def update(self, session: AsyncSession, id: int, request_data) -> Any:
    #     pass
    #
    # @abstractmethod
    # async def delete(self, session: AsyncSession, id: int) -> Any:
    #     pass

class BaseValidator(ABC):
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
            (
                v for k, v in bound_args.arguments.items()
                if k.endswith("_id")
            ),
            None,
        )

    @abstractmethod
    async def validate(self) -> None:
        pass
