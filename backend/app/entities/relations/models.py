from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.entities.base import Base


if TYPE_CHECKING:
    from app.entities.teacher.models import Teacher
    from app.entities.subject.models import Subject
    from app.entities.student_group.models import StudentGroup


class TeacherSubject(Base):

    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id", ondelete="CASCADE"), primary_key=True
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="CASCADE"), primary_key=True
    )
    teaching_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="subjects")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="teachers")


class StudentGroupSubject(Base):

    student_group_id: Mapped[int] = mapped_column(
        ForeignKey("student_groups.id", ondelete="CASCADE"), primary_key=True
    )
    subject_id: Mapped[int] = mapped_column(
        ForeignKey("subjects.id", ondelete="CASCADE"), primary_key=True
    )
    study_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    student_group: Mapped["StudentGroup"] = relationship(
        "StudentGroup", back_populates="subjects"
    )
    subject: Mapped["Subject"] = relationship(
        "Subject", back_populates="student_groups"
    )
