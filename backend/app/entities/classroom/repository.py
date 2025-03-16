from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.base import BaseRepository
from app.entities.classroom.models import Classroom
from app.entities.classroom.schemas import (
    ClassroomCreateRequest,
    ClassroomUpdateRequest,
)
from app.utils.pagination import PaginationParamsDep


class ClassroomRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(Classroom)

    async def create(
        self, session: AsyncSession, request_data: ClassroomCreateRequest
    ) -> Classroom:
        classroom = self.sql_model(name=request_data.name)
        session.add(classroom)
        await session.commit()
        await session.refresh(classroom)
        return classroom

    async def list_classrooms(
        self, session: AsyncSession, pagination: PaginationParamsDep
    ):
        classrooms = await self.list_all(session, pagination, load_strategy="selectin")
        return classrooms

    async def update(
        self,
        session: AsyncSession,
        id: int,
        request_data: ClassroomUpdateRequest,
    ) -> Classroom:
        # TODO: обновлять все остальное!
        classroom = await self.get_by_id(session, id, load_strategy="selectin")

        if request_data.name != classroom.name:
            classroom.name = request_data.name
            await session.commit()
            await session.refresh(classroom)
        return classroom

    async def delete(self, session: AsyncSession, id: int) -> Classroom:
        classroom = await self.get_by_id(session, id)
        deleted_data = {
            key: value
            for key, value in classroom.__dict__.items()
            if not key.startswith("_")
        }
        await session.delete(classroom)
        await session.commit()
        return Classroom(**deleted_data)
