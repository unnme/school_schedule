from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase, declared_attr
from pydantic import BaseModel

from app.core.config import settings
from app.utils.case_converter import camel_case_to_snake_case


# sqlalchemy
class Base(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.database.NAMING_CONVENTION,
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"


# pydantic
class CustomBaseModel(BaseModel):
    class Config:
        from_attributes = True
