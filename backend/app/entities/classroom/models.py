from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.entities.base import Base


class Classroom(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)
