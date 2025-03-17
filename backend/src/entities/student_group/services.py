from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.depends.repository import student_group_repository
from src.entities.student_group.schemas import (
    StudentGroupCreateRequest,
    StudentGroupResponse,
    StudentGroupUpdateRequest,
    _StudentGroupCreateResponse,
    _StudentGroupDeleteResponse,
    _StudentGroupUpdateResponse,
)
from src.entities.student_group.validators import validate_student_group_request
from src.utils.pagination import PaginationParamsDep


class StudentGroupManager:
    @classmethod
    @validate_student_group_request
    async def create_student_group(
        cls, session: AsyncSession, request_data: StudentGroupCreateRequest
    ) -> _StudentGroupCreateResponse:
        student_group = await student_group_repository.create(session, request_data)
        return _StudentGroupCreateResponse.model_validate(student_group)

    @classmethod
    async def list_student_groups(
        cls, session: AsyncSession, pagination: PaginationParamsDep
    ) -> Sequence[StudentGroupResponse]:
        return await student_group_repository.list_student_groups(session, pagination)

    @classmethod
    @validate_student_group_request
    async def update_student_group(
        cls,
        session: AsyncSession,
        id: int,
        request_data: StudentGroupUpdateRequest,
    ) -> _StudentGroupUpdateResponse:
        async with session.begin():
            student_group = await student_group_repository.update(
                session, id, request_data
            )
            return _StudentGroupUpdateResponse.model_validate(student_group)

    @classmethod
    async def delete_student_group(
        cls, session: AsyncSession, id: int
    ) -> _StudentGroupDeleteResponse:
        student_group = await student_group_repository.delete(session, id)
        return _StudentGroupDeleteResponse.model_validate(student_group)
