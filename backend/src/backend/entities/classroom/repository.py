from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from backend.entities.base import BaseRepository
from backend.entities.classroom.models import Classroom
from backend.entities.classroom.schemas import (
    ClassroomPostRequest,
    ClassroomPutRequest,
)
from backend.utils.pagination import PaginationParamsDep


class ClassroomRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(Classroom)

    async def _set_name(self, classroom, request_data):
        if request_data.name != classroom.name:
            classroom.name = request_data.name
        pass

    async def _set_capacity(self, classroom, request_data):
        if request_data.capacity is not None and request_data.capacity != classroom.capacity:
            classroom.capacity = request_data.capacity

    async def create_many(self, session: AsyncSession, request_data_list: List[ClassroomPostRequest]):
        async with session.begin():
            classrooms = [self.sql_model(name=data.name, capacity=data.capacity) for data in request_data_list]
            session.add_all(classrooms)

    async def create(self, session: AsyncSession, request_data: ClassroomPostRequest) -> Classroom:
        classroom = self.sql_model(name=request_data.name, capacity=request_data.capacity)
        session.add(classroom)
        await session.commit()

        classroom = await self.get_by_id(session, classroom.id, load_strategy="selectin")
        return classroom

    async def list_classrooms(self, session: AsyncSession, pagination: PaginationParamsDep):
        classrooms = await self.list_all(session, pagination, load_strategy="selectin")
        return classrooms

    async def update(
        self,
        session: AsyncSession,
        id: int,
        request_data: ClassroomPutRequest,
    ) -> Classroom:
        classroom = await self.get_by_id(session, id, load_strategy="selectin")

        await self._set_name(classroom, request_data)
        await self._set_capacity(classroom, request_data)

        await session.commit()
        await session.refresh(classroom)
        return classroom


classroom_repository = ClassroomRepository()
