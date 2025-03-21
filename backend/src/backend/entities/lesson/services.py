from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.depends.repository import lesson_repository
from backend.entities.lesson.schemas import (
    LessonCreateRequest,
    LessonResponse,
    _LessonCreateResponse,
)
from backend.utils.pagination import PaginationParamsDep


class LessonManager:
    @classmethod
    async def create_lesson(
        cls, session: AsyncSession, request_data: LessonCreateRequest
    ) -> _LessonCreateResponse:
        lesson = await lesson_repository.create(session, request_data)
        return _LessonCreateResponse.model_validate(lesson)

    @classmethod
    async def list_lessons(
        cls, session: AsyncSession, pagination: PaginationParamsDep
    ) -> Sequence[LessonResponse]:
        lessons = await lesson_repository.list_lessons(session, pagination)
        return lessons

    # @classmethod
    # @validate_subject_request
    # async def update_subject(
    #     cls, session: AsyncSession, id: int, request_data: SubjectUpdateRequest
    # ) -> _SubjectUpdateResponse:
    #     subject = await subject_repository.update(session, id, request_data)
    #     return _SubjectUpdateResponse.model_validate(subject)
    #
    # @classmethod
    # async def delete_subject(
    #     cls, session: AsyncSession, id: int
    # ) -> _SubjectDeleteResponse:
    #     subject = await subject_repository.delete(session, id)
    #     return _SubjectDeleteResponse.model_validate(subject)
