from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.entities.base import Base

if TYPE_CHECKING:
    from backend.entities.relations.models import TeacherSubject


class Teacher(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    patronymic: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    subjects: Mapped[list["TeacherSubject"]] = relationship(
        back_populates="teacher",
        cascade="all, delete-orphan",
    )

    @property
    def name(self) -> str:
        return f"{self.last_name} {self.first_name} {self.patronymic}"
