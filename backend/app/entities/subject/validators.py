from functools import wraps
from typing import Optional
from sqlalchemy import select

from app.core.database import db_manager
from app.core.exceptions import (
    SubjectNameExistsException,
    RequestDataMissingException,
)
from app.utils.inspect import func_inspect
from app.entities.subject.models import Subject


class SubjectValidator:
    def __init__(self, session, request_data, subject_id: Optional[int]):
        self._session = session
        self._request_data = request_data
        self._subject_id = subject_id

    async def check_duplicate_subject(self):
        """Проверяет имя предмета на уникальность"""
        stmt = select(Subject).where(Subject.name == self._request_data.name)

        if self._subject_id is not None:
            stmt = stmt.where(Subject.id != self._subject_id)

        if existing_subject := await self._session.scalar(stmt):
            raise SubjectNameExistsException(existing_subject.name)

    async def validate(self):
        await self.check_duplicate_subject()


def validate_subject_request(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        bound_args = func_inspect(func, *args, **kwargs)

        request_data = bound_args.arguments.get("request_data")
        if request_data is None:
            raise RequestDataMissingException()

        subject_id: Optional[int] = bound_args.arguments.get("subject_id")

        async with db_manager.AsyncSessionFactory() as session:
            validator = SubjectValidator(session, request_data, subject_id)
            await validator.validate()

        return await func(*args, **kwargs)

    return wrapper
