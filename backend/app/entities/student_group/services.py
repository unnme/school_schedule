from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.pagination import PaginationParamsDep
from app.entities.student_group.validators import validate_student_group_request
from app.entities.student_group.schemas import (
    StudentGroupCreateRequest,
    StudentGroupResponse,
    StudentGroupUpdateRequest,
    _StudentGroupCreateResponse,
    _StudentGroupUpdateResponse,
    _StudentGroupDeleteResponse,
)
from .repository import student_group_repository


class StudentGroupManager:
    @classmethod
    @validate_student_group_request
    async def create_student_group(
        cls, session: AsyncSession, request_data: StudentGroupCreateRequest
    ) -> _StudentGroupCreateResponse:
        student_group = await student_group_repository.create_student_group(
            session, request_data
        )
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
        request_data: StudentGroupUpdateRequest,
        student_group_id: int,
    ) -> _StudentGroupUpdateResponse:
        async with session.begin():
            student_group = await student_group_repository.update_sutdent_group(
                session, request_data, student_group_id
            )
            return _StudentGroupUpdateResponse.model_validate(student_group)

    @classmethod
    async def delete_student_group(
        cls, session: AsyncSession, student_group_id: int
    ) -> _StudentGroupDeleteResponse:
        student_group = await student_group_repository.delete_student_group(
            session, student_group_id
        )
        return _StudentGroupDeleteResponse.model_validate(student_group)
