from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.entities.base import Base

if TYPE_CHECKING:
    from backend.entities.relations.models import StudentGroupSubject


class StudentGroup(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    subjects: Mapped[List["StudentGroupSubject"]] = relationship(
        back_populates="student_group",
        cascade="all, delete-orphan",
    )
