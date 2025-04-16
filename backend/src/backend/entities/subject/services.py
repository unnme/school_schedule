from typing import Any, List, Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.entities.base import CustomBaseModel
from backend.entities.subject.schemas import (
    SubjectCreateResponse,
    SubjectPostRequest,
    SubjectResponse,
    SubjectPutRequest,
    SubjectUpdateResponse,
)
from backend.entities.subject.validators import validate_subject_request
from backend.utils.pagination import PaginationParamsDep
from backend.entities.subject.repository import subject_repository


class ListReturnModel(CustomBaseModel):
    items: List[Any]
    total: int
    limit: int
    offset: int


class SubjectManager:
    @classmethod
    @validate_subject_request
    async def create_subject(cls, session: AsyncSession, request_data: SubjectPostRequest) -> SubjectCreateResponse:
        subject = await subject_repository.create(session, request_data)
        return SubjectCreateResponse.model_validate(subject)

    @classmethod
    async def list_subjects(cls, session: AsyncSession, pagination: PaginationParamsDep) -> Sequence[SubjectResponse]:
        subjects = await subject_repository.list_subjects(session, pagination)
        return subjects

    @classmethod
    async def list_subjects_new(cls, session: AsyncSession, pagination: PaginationParamsDep):
        subjects = await subject_repository.list_subjects(session, pagination)

        count_stmt = select(func.count()).select_from(subject_repository.sql_model)
        total_result = await session.execute(count_stmt)
        total = total_result.scalar()
        return {"items": subjects, "total": total, "limit": pagination.limit, "offset": pagination.offset}

    @classmethod
    @validate_subject_request
    async def update_subject(
        cls, session: AsyncSession, id: int, request_data: SubjectPutRequest
    ) -> SubjectUpdateResponse:
        subject = await subject_repository.update(session, id, request_data)
        return SubjectUpdateResponse.model_validate(subject)

    @classmethod
    async def delete_subject(cls, session: AsyncSession, id: int) -> None:
        await subject_repository.delete(session, id)
