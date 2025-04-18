from functools import wraps

from sqlalchemy import select

from backend.core.exceptions import DuplicateSubjectNameException
from backend.entities.base import BaseValidator
from backend.entities.subject.models import Subject


class SubjectValidator(BaseValidator):
    def __init__(self, func, *args, **kwargs):
        super().__init__(func, *args, **kwargs)

    async def check_duplicate_subject(self):
        stmt = select(Subject).where(Subject.name == self.request_data.name)

        if self.id is not None:
            stmt = stmt.where(Subject.id != self.id)

        if existing_subject := await self.session.scalar(stmt):
            raise DuplicateSubjectNameException(existing_subject.name)

    async def validate(self) -> None:
        try:
            await self.check_duplicate_subject()
        finally:
            await self.session.rollback()


def validate_subject_request(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        await SubjectValidator(func, *args, **kwargs).validate()

        return await func(*args, **kwargs)

    return wrapper
