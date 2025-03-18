from collections import Counter
from functools import wraps

from sqlalchemy import select

from backend.core.exceptions import (
    DuplicateSubjectIDException,
    DuplicateTeacherException,
    InvalidSubjectIDException,
)
from backend.entities.base import BaseValidator
from backend.entities.subject.models import Subject
from backend.entities.teacher.models import Teacher


class TeacherReqValidator(BaseValidator):
    def __init__(self, func, *args, **kwargs):
        super().__init__(func, *args, **kwargs)

    async def check_duplicate_teacher(self):
        stmt = select(Teacher).where(
            Teacher.last_name == self.request_data.last_name,
            Teacher.first_name == self.request_data.first_name,
            Teacher.patronymic == self.request_data.patronymic,
        )

        if self.id is not None:
            stmt = stmt.where(Teacher.id != self.id)

        if existing_teacher := await self.session.scalar(stmt):
            raise DuplicateTeacherException(existing_teacher.name)

    async def check_teacher_subjects_validity(self):
        user_ids = [subj.id for subj in self.request_data.subjects]
        duplicates = [item for item, count in Counter(user_ids).items() if count > 1]
        if duplicates:
            raise DuplicateSubjectIDException(*duplicates)

        stmt = select(Subject.id).where(Subject.id.in_(user_ids))
        db_subject_ids = await self.session.scalars(stmt)

        if wrong_subject_ids := set(user_ids) - set(db_subject_ids):
            raise InvalidSubjectIDException(*wrong_subject_ids)

    async def validate(self):
        try:
            await self.check_teacher_subjects_validity()
            await self.check_duplicate_teacher()
        finally:
            await self.session.rollback()


def validate_teacher_request(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        await TeacherReqValidator(func, *args, **kwargs).validate()
        return await func(*args, **kwargs)

    return wrapper
