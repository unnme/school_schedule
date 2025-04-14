from sqlalchemy.ext.asyncio import AsyncSession

from backend.entities.base import BaseRepository
from backend.entities.lesson.models import Lesson
from backend.entities.lesson.schemas import LessonCreateRequest, LessonUpdateRequest
from backend.utils.pagination import PaginationParamsDep


class LessonRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(Lesson)

    async def create(self, session: AsyncSession, request_data: LessonCreateRequest) -> Lesson:
        lesson = self.sql_model(**request_data.model_dump())
        session.add(lesson)
        await session.commit()
        await session.refresh(lesson)
        return lesson

    async def list_lessons(self, session: AsyncSession, pagination: PaginationParamsDep):
        lessons = await self.list_all(session, pagination, load_strategy="selectin")
        return lessons

    # async def update(
    #     self, session: AsyncSession, id: int, request_data: LessonUpdateRequest
    # ) -> Lesson:
    #     lesson = await self.get_by_id(session, id, load_strategy="selectin")
    #
    #     if request_data.name != lesson.name:
    #         lesson.name = request_data.name
    #         await session.commit()
    #         await session.refresh(lesson)
    #     return lesson
    #
    # async def delete(self, session: AsyncSession, id: int) -> Lesson:
    #     lesson = await self.get_by_id(session, id)
    #     deleted_data = {
    #         key: value
    #         for key, value in lesson.__dict__.items()
    #         if not key.startswith("_")
    #     }
    #     await session.delete(lesson)
    #     await session.commit()
    #     return Lesson(**deleted_data)
