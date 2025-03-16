from collections import Counter
from functools import wraps
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import (
    DatabaseConnectionError,
    DuplicateStudentGroupException,
    DuplicateSubjectIDException,
    InvalidSubjectIDException,
    RequestDataMissingException,
)
from app.entities.subject.models import Subject
from app.utils.common_utils import get_bound_arguments

from .models import StudentGroup
from .schemas import StudentGroupRequest


class StudentGroupRequestValidator:
    def __init__(
        self,
        session: AsyncSession,
        request_data: StudentGroupRequest,
        student_group_id=None,
    ) -> None:
        self._session = session
        self._request_data = request_data
        self._student_group_id: Optional[int] = student_group_id

    async def _check_duplicate_student_group(self):
        stmt = select(StudentGroup).where(
            StudentGroup.name == self._request_data.name,
        )

        if self._student_group_id is not None:
            stmt = stmt.where(StudentGroup.id != self._student_group_id)

        if existing_student_group := await self._session.scalar(stmt):
            raise DuplicateStudentGroupException(existing_student_group.name)

    async def _check_student_group_subjects_validity(self):
        user_ids = [subj.id for subj in self._request_data.subjects]
        duplicates = [item for item, count in Counter(user_ids).items() if count > 1]
        if duplicates:
            raise DuplicateSubjectIDException(*duplicates)

        stmt = select(Subject.id).where(Subject.id.in_(user_ids))
        db_subject_ids = await self._session.scalars(stmt)

        if wrong_subject_ids := set(user_ids) - set(db_subject_ids):
            raise InvalidSubjectIDException(*wrong_subject_ids)

    async def validate(self):
        await self._check_student_group_subjects_validity()
        await self._check_duplicate_student_group()


def validate_student_group_request(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        bound_args = get_bound_arguments(func, *args, **kwargs)

        if not (session := bound_args.arguments.get("session")):
            raise DatabaseConnectionError()

        if not (request_data := bound_args.arguments.get("request_data")):
            raise RequestDataMissingException()

        student_group_id: Optional[int] = bound_args.arguments.get("student_group_id")

        validator = StudentGroupRequestValidator(
            session, request_data, student_group_id
        )
        await validator.validate()

        return await func(*args, **kwargs)

    return wrapper
