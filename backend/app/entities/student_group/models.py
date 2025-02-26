from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.entities.relations.models import StudentGroupSubject


class StudentGroup(Base):
    __tablename__ = "student_groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    subjects: Mapped[list["StudentGroupSubject"]] = relationship(
        back_populates="student_group",
        cascade="all, delete-orphan",
    )
