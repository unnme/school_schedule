from sqlalchemy.ext.asyncio import AsyncSession

from backend.entities.base import ListResponseModel
from backend.entities.lesson.repository import lesson_repository

from backend.entities.lesson.schemas import (
    LessonPostRequest,
    LessonCreateResponse,
    LessonResponse,
)
from backend.api.depends import PaginationParamsDep


class LessonManager:
    @classmethod
    async def create_lesson(cls, session: AsyncSession, request_data: LessonPostRequest) -> LessonCreateResponse:
        lesson = await lesson_repository.create(session, request_data)
        return LessonCreateResponse.model_validate(lesson)

    @classmethod
    async def list_lessons(cls, session: AsyncSession, pagination: PaginationParamsDep) -> ListResponseModel:
        subjects = await lesson_repository.list_lessons(session, pagination)
        total = await lesson_repository.entity_count(session)
        return ListResponseModel[LessonResponse](
            items=subjects, total=total, limit=pagination.limit, offset=pagination.offset
        )
