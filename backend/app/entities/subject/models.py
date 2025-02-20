from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from app.core.database import Base



if TYPE_CHECKING:
    from app.entities.relations.models import TeacherSubject
    from app.entities.relations.models import StudentGroupSubject


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    teachers: Mapped[list["TeacherSubject"]] = relationship(
        back_populates="subject",
        cascade="all, delete-orphan",
    )

    student_groups: Mapped[list["StudentGroupSubject"]] = relationship(
        back_populates="subject", cascade="all, delete-orphan", lazy="selectin"
    )
