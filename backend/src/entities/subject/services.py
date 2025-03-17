from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.depends.repository import subject_repository
from src.entities.subject.schemas import (
    SubjectCreateRequest,
    SubjectResponse,
    SubjectUpdateRequest,
    _SubjectCreateResponse,
    _SubjectDeleteResponse,
    _SubjectUpdateResponse,
)
from src.entities.subject.validators import validate_subject_request
from src.utils.pagination import PaginationParamsDep


class SubjectManager:
    @classmethod
    @validate_subject_request
    async def create_subject(
        cls, session: AsyncSession, request_data: SubjectCreateRequest
    ) -> _SubjectCreateResponse:
        subject = await subject_repository.create(session, request_data)
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
        cls, session: AsyncSession, id: int, request_data: SubjectUpdateRequest
    ) -> _SubjectUpdateResponse:
        subject = await subject_repository.update(session, id, request_data)
        return _SubjectUpdateResponse.model_validate(subject)

    @classmethod
    async def delete_subject(
        cls, session: AsyncSession, id: int
    ) -> _SubjectDeleteResponse:
        subject = await subject_repository.delete(session, id)
        return _SubjectDeleteResponse.model_validate(subject)
