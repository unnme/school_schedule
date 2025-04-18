from sqlalchemy.ext.asyncio import AsyncSession

from backend.entities.base import ListResponseModel
from backend.entities.subject.schemas import (
    SubjectCreateResponse,
    SubjectPostRequest,
    SubjectResponse,
    SubjectPutRequest,
    SubjectUpdateResponse,
)
from backend.entities.subject.validators import validate_subject_request
from backend.entities.subject.repository import subject_repository
from backend.api.depends import PaginationParamsDep


class SubjectManager:
    @classmethod
    @validate_subject_request
    async def create_subject(cls, session: AsyncSession, request_data: SubjectPostRequest) -> SubjectCreateResponse:
        subject = await subject_repository.create(session, request_data)
        await session.commit()
        return SubjectCreateResponse.model_validate(subject)

    @classmethod
    async def list_subjects(cls, session: AsyncSession, pagination: PaginationParamsDep) -> ListResponseModel:
        subjects = await subject_repository.list_subjects(session, pagination)
        total = await subject_repository.entity_count(session)
        return ListResponseModel[SubjectResponse](
            items=subjects, total=total, limit=pagination.limit, offset=pagination.offset
        )

    @classmethod
    @validate_subject_request
    async def update_subject(
        cls, session: AsyncSession, id: int, request_data: SubjectPutRequest
    ) -> SubjectUpdateResponse:
        subject = await subject_repository.update(session, id, request_data)
        await session.commit()
        return SubjectUpdateResponse.model_validate(subject)

    @classmethod
    async def delete_subject(cls, session: AsyncSession, id: int) -> None:
        await subject_repository.delete(session, id)
        await session.commit()
