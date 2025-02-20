from collections import Counter
from functools import wraps
from inspect import BoundArguments
from typing import Optional

from sqlalchemy import select

from app.core.database import db_manager
from app.core.exceptions import (
    DuplicateSubjectException,
    DuplicateTeacherException,
    InvalidSubjectIDException,
    RequestDataMissingException,
)
from app.utils.inspect import func_inspect
from app.entities.subject.models import Subject
from app.entities.teacher.models import Teacher


class TeacherValidator:
    def __init__(self, session, request_data, teacher_id: Optional[int] = None):

        self._session = session
        self._request_data = request_data
        self._teacher_id = teacher_id

    async def check_duplicate_teacher(self):
        stmt = select(Teacher).where(
            Teacher.last_name == self._request_data.last_name,
            Teacher.first_name == self._request_data.first_name,
            Teacher.patronymic == self._request_data.patronymic,
        )

        if self._teacher_id is not None:
            stmt = stmt.where(Teacher.id != self._teacher_id)

        if existing_teacher := await self._session.scalar(stmt):
            raise DuplicateTeacherException(existing_teacher)

    async def check_teacher_subjects_validity(self):
        user_ids = [subj.id for subj in self._request_data.subjects]
        duplicates = [item for item, count in Counter(user_ids).items() if count > 1]
        if duplicates:
            raise DuplicateSubjectException(*duplicates)

        stmt = select(Subject.id).where(Subject.id.in_(user_ids))
        db_subject_ids = await self._session.scalars(stmt)

        if wrong_subject_ids := set(user_ids) - set(db_subject_ids):
            raise InvalidSubjectIDException(*wrong_subject_ids)

    async def validate(self):
        await self.check_teacher_subjects_validity()
        await self.check_duplicate_teacher()


def validate_teacher_request(func):
    @wraps(func)
    async def inner(*args, **kwargs):
        bound_args: BoundArguments = func_inspect(func, *args, **kwargs)

        request_data = bound_args.arguments.get("request_data")
        if request_data is None:
            raise RequestDataMissingException()

        teacher_id = bound_args.arguments.get("teacher_id")

        async with db_manager.AsyncSessionFactory() as session:
            validator = TeacherValidator(session, request_data, teacher_id)
            await validator.validate()

        return await func(*args, **kwargs)

    return inner
