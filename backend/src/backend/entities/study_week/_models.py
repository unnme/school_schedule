from sqlalchemy.orm import Mapped, mapped_column

from backend.entities.base import Base


class StudyWeek(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    study_year: Mapped[int]
    week_number: Mapped[int]
