from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.entities.base import Base

if TYPE_CHECKING:
    from app.entities.relations.models import (
        ClassroomSubject,
        StudentGroupSubject,
        TeacherSubject,
    )


class Subject(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    teachers: Mapped[list["TeacherSubject"]] = relationship(
        back_populates="subject",
        cascade="all, delete-orphan",
    )

    student_groups: Mapped[list["StudentGroupSubject"]] = relationship(
        back_populates="subject",
        cascade="all, delete-orphan",
    )

    classrooms: Mapped[list["ClassroomSubject"]] = relationship(
        back_populates="subject",
        cascade="all, delete-orphan",
    )
