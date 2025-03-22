from datetime import date
from functools import cached_property

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.entities.base import Base


class Lesson(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    leeson_date: Mapped[date] = mapped_column(Date)
    school_shift: Mapped[int]
    lesson_number: Mapped[int]

    classroom_id: Mapped[int] = mapped_column(ForeignKey("classrooms.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    student_group_id: Mapped[int] = mapped_column(ForeignKey("student_groups.id"))

    classroom = relationship("Classroom", lazy="joined")
    subject = relationship("Subject", lazy="joined")
    teacher = relationship("Teacher", lazy="joined")
    student_group = relationship("StudentGroup", lazy="joined")

    @cached_property
    def lesson_day(self) -> int:
        return self.leeson_date.weekday()
