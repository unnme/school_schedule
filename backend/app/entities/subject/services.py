from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.subject.schemas import (
    SubjectCreateRequest,
    SubjectResponse,
    SubjectUpdateRequest,
    _SubjectCreateResponse,
    _SubjectDeleteResponse,
    _SubjectUpdateResponse,
)
from app.entities.subject.validators import validate_subject_request
from app.utils.pagination import PaginationParamsDep

from app.api.depends.repository import subject_repository


class SubjectManager:
    @classmethod
    @validate_subject_request
    async def create_subject(
        cls, session: AsyncSession, request_data: SubjectCreateRequest
    ) -> _SubjectCreateResponse:
        subject = await subject_repository.create_subject(session, request_data)
        return _SubjectCreateResponse.model_validate(subject)

    @classmethod
    async def list_subjects(
        cls, session: AsyncSession, pagination: PaginationParamsDep
    ) -> Sequence[SubjectResponse]:
        subjects = await subject_repository.list_subjects(session, pagination)
        return subjects

    @classmethod
    @validate_subject_request
    async def update_subject(
        cls, session: AsyncSession, subject_id: int, request_data: SubjectUpdateRequest
    ) -> _SubjectUpdateResponse:
        subject = await subject_repository.update_subject(
            session, subject_id, request_data
        )
        return _SubjectUpdateResponse.model_validate(subject)

    @classmethod
    async def delete_subject(
        cls, session: AsyncSession, subject_id: int
    ) -> _SubjectDeleteResponse:
        subject = await subject_repository.delete_subject(session, subject_id)
        return _SubjectDeleteResponse.model_validate(subject)
