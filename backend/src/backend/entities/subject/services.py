from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from backend.entities.mixins import CommitRefreshMixin
from backend.entities.subject.schemas import (
    SubjectCreateResponse,
    SubjectPatchRequest,
    SubjectPostRequest,
    SubjectResponse,
    SubjectPutRequest,
    SubjectUpdateResponse,
)
from backend.entities.subject.validators import validate_subject_request
from backend.utils.pagination import PaginationParamsDep
from backend.api.depends.repository import subject_repository


class SubjectManager(CommitRefreshMixin):
    @classmethod
    @validate_subject_request
    async def create_subject(
        cls, session: AsyncSession, request_data: SubjectPostRequest
    ) -> SubjectCreateResponse:
        subject = subject_repository.create(session, request_data)
        await cls.commit_refresh(session, subject)

        return SubjectCreateResponse.model_validate(subject)

    @classmethod
    async def list_subjects(
        cls, session: AsyncSession, pagination: PaginationParamsDep
    ) -> Sequence[SubjectResponse]:
        subjects = await subject_repository.list_subjects(session, pagination)
        return subjects

    @classmethod
    @validate_subject_request
    async def update_subject(
        cls, session: AsyncSession, id: int, request_data: SubjectPutRequest
    ) -> SubjectUpdateResponse:
        subject = await subject_repository.update(session, id, request_data)
        await cls.commit_refresh(session, subject)

        return SubjectUpdateResponse.model_validate(subject)

    @classmethod
    # @validate_subject_request
    async def update_subject_fields(
        cls, session: AsyncSession, id: int, request_data: SubjectPatchRequest
    ) -> SubjectUpdateResponse: 
        subject = await subject_repository.update_subject_fields(session, id, request_data)
        await cls.commit_refresh(session, subject)
        return SubjectUpdateResponse.model_validate(subject)

    @classmethod
    async def delete_subject(
        cls, session: AsyncSession, id: int
    ) -> None:
        await session.delete(
            await subject_repository.get_by_id(session, id)
        )
        await session.commit()
