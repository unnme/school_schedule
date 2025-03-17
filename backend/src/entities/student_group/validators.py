from collections import Counter
from functools import wraps

from sqlalchemy import select

from src.core.exceptions import (
    DuplicateStudentGroupException,
    DuplicateSubjectIDException,
    InvalidSubjectIDException,
)
from src.entities.base import BaseValidator
from src.entities.subject.models import Subject

from .models import StudentGroup


class StudentGroupReqValidator(BaseValidator):
    def __init__(self, func, *args, **kwargs):
        super().__init__(func, *args, **kwargs)

    async def _check_duplicate_student_group(self):
        stmt = select(StudentGroup).where(
            StudentGroup.name == self.request_data.name,
        )

        if self.id is not None:
            stmt = stmt.where(StudentGroup.id != self.id)

        if existing_student_group := await self.session.scalar(stmt):
            raise DuplicateStudentGroupException(existing_student_group.name)

    async def _check_student_group_subjects_validity(self):
        user_ids = [subj.id for subj in self.request_data.subjects]
        duplicates = [item for item, count in Counter(user_ids).items() if count > 1]
        if duplicates:
            raise DuplicateSubjectIDException(*duplicates)

        stmt = select(Subject.id).where(Subject.id.in_(user_ids))
        db_subject_ids = await self.session.scalars(stmt)

        if wrong_subject_ids := set(user_ids) - set(db_subject_ids):
            raise InvalidSubjectIDException(*wrong_subject_ids)

    async def validate(self) -> None:
        try:
            await self._check_student_group_subjects_validity()
            await self._check_duplicate_student_group()
        finally:
            await self.session.rollback()


def validate_student_group_request(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        await StudentGroupReqValidator(func, *args, **kwargs).validate()
        return await func(*args, **kwargs)

    return wrapper
