from fastapi_users.db import (
    SQLAlchemyBaseUserTableUUID,
)

from app.entities.base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
