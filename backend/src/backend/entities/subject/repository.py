from typing import List, Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession

from backend.entities.base import BaseRepository
from backend.entities.subject.models import Subject
from backend.entities.subject.schemas import SubjectPatchRequest, SubjectPostRequest, SubjectPutRequest
from backend.utils.pagination import PaginationParamsDep


class SubjectRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(Subject)

    async def create_many(
        self, session: AsyncSession, request_data_list: List[SubjectPostRequest]
    ):
        subjects = [
            self.sql_model(name=data.name) for data in request_data_list
        ]
        session.add_all(subjects)

    def create(
        self, session: AsyncSession, request_data: SubjectPostRequest
    ) -> Subject:
        subject = self.sql_model(name=request_data.name)
        session.add(subject)
        return subject

    async def list_subjects(
        self, session: AsyncSession, pagination: PaginationParamsDep
    ):
        subjects = await self.list_all(session, pagination, load_strategy="selectin")
        return subjects

    async def update(
        self, session: AsyncSession, id: int, request_data: SubjectPutRequest
    ) -> Subject:
        subject = await self.get_by_id(session, id, load_strategy="selectin")
        subject.name = request_data.name
        session.add(subject)
        return subject

    async def update_subject_fields(
        self, session: AsyncSession, id: int, request_data: SubjectPatchRequest
    ) -> Subject:
        subject = await self.update_fields(session, id, request_data)
        session.add(subject)
        return subject
