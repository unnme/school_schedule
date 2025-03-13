from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.base import BaseRepository
from app.entities.subject.models import Subject
from app.entities.subject.schemas import SubjectCreateRequest, SubjectUpdateRequest
from app.utils.pagination import PaginationParamsDep


class SubjectRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(Subject)

    async def create_subject(
        self, session: AsyncSession, request_data: SubjectCreateRequest
    ) -> Subject:
        subject = self.sql_model(name=request_data.name)
        session.add(subject)
        await session.commit()
        await session.refresh(subject)
        return subject

    async def list_subjects(
        self, session: AsyncSession, pagination: PaginationParamsDep
    ):
        subjects = await self.list_all(session, pagination, load_strategy="selectin")
        return subjects

    async def update_subject(
        self, session: AsyncSession, subject_id: int, request_data: SubjectUpdateRequest
    ) -> Subject:
        subject = await self.get_by_id(session, subject_id, load_strategy="selectin")

        if request_data.name != subject.name:
            subject.name = request_data.name
            await session.commit()
            await session.refresh(subject)
        return subject

    async def delete_subject(self, session: AsyncSession, subject_id: int) -> Subject:
        subject = await self.get_by_id(session, subject_id)
        deleted_data = {
            key: value
            for key, value in subject.__dict__.items()
            if not key.startswith("_")
        }
        await session.delete(subject)
        await session.commit()
        return Subject(**deleted_data)


subject_repository = SubjectRepository()
