from datetime import datetime
from typing import Optional

from sqlalchemy import Date, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from backend.entities.base import Base


class Lesson(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    lesson_number: Mapped[int] = mapped_column(Integer)
    date: Mapped[datetime] = mapped_column(Date)
    school_shift: Mapped[int] = mapped_column(Integer)

    class_profile: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("subjects.id", ondelete="SET NULL"), nullable=True
    )

    subject: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id"))

    teacher: Mapped[int] = mapped_column(Integer, ForeignKey("teachers.id"))

    student_group: Mapped[int] = mapped_column(Integer, ForeignKey("student_groups.id"))
