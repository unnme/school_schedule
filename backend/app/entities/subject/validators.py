from functools import wraps
from typing import Optional
from sqlalchemy import select

from app.core.database import session_manager
from app.core.exceptions import (
    DuplicateSubjectNameException,
    RequestDataMissingException,
)
from app.utils.common_utils import func_inspect
from app.entities.subject.models import Subject


class SubjectValidator:
    def __init__(self, session, **kwargs):
        self._session = session
        self._request_data = kwargs.get("request_data")
        self._subject_id = kwargs.get("subject_id")

    async def check_duplicate_subject(self):
        stmt = select(Subject).where(Subject.name == self._request_data.name)

        if self._subject_id is not None:
            stmt = stmt.where(Subject.id != self._subject_id)

        if existing_subject := await self._session.scalar(stmt):
            raise DuplicateSubjectNameException(existing_subject.name)

    async def validate(self):
        await self.check_duplicate_subject()


def validate_subject_request(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        bound_args = func_inspect(func, *args, **kwargs)

        if not (request_data := bound_args.arguments.get("request_data")):
            raise RequestDataMissingException()

        subject_id: Optional[int] = bound_args.arguments.get("subject_id")

        async for session in session_manager.get_async_session():
            validator = SubjectValidator(
                session, request_data=request_data, subject_id=subject_id
            )
            await validator.validate()

        return await func(*args, **kwargs)

    return wrapper
