from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base


class Classroom(Base):
    __tablename__ = "classrooms"

    id: Mapped[int] = mapped_column(primary_key=True)
