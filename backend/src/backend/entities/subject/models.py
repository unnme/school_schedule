from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.entities.base import Base

if TYPE_CHECKING:
    from backend.entities.relations.models import (
        ClassroomSubject,
        StudentGroupSubject,
        TeacherSubject,
    )


class Subject(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    teachers: Mapped[List["TeacherSubject"]] = relationship(
        back_populates="subject",
        cascade="all, delete-orphan",
    )

    student_groups: Mapped[List["StudentGroupSubject"]] = relationship(
        back_populates="subject",
        cascade="all, delete-orphan",
    )

    classrooms: Mapped[List["ClassroomSubject"]] = relationship(
        back_populates="subject",
        cascade="all, delete-orphan",
    )
