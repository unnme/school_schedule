from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from backend.entities.base import BaseRepository
from backend.entities.subject.models import Subject
from backend.entities.subject.schemas import SubjectPostRequest, SubjectPutRequest
from backend.utils.pagination import PaginationParamsDep


class SubjectRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(Subject)

    async def create_many(self, session: AsyncSession, request_data_list: List[SubjectPostRequest]):
        async with session.begin():
            subjects = [self.sql_model(name=data.name) for data in request_data_list]
            session.add_all(subjects)

    async def create(self, session: AsyncSession, request_data: SubjectPostRequest) -> Subject:
        subject = self.sql_model(name=request_data.name)
        session.add(subject)
        await session.commit()
        await session.refresh(subject)
        return subject

    async def list_subjects(self, session: AsyncSession, pagination: PaginationParamsDep):
        subjects = await self.list_all(session, pagination, load_strategy="selectin")
        return subjects

    async def update(self, session: AsyncSession, id: int, request_data: SubjectPutRequest) -> Subject:
        subject = await self.get_by_id(session, id, load_strategy="selectin")
        subject.name = request_data.name
        session.add(subject)
        await session.commit()
        await session.refresh(subject)
        return subject

    async def delete(self, session: AsyncSession, id: int) -> None:
        subject = await self.get_by_id(session, id)
        await session.delete(subject)
        await session.commit()


subject_repository = SubjectRepository()
