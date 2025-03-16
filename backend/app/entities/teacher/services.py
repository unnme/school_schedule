from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depends.repository import teacher_repository
from app.entities.teacher.schemas import (
    TeacherCreateRequest,
    TeacherResponse,
    TeacherUpdateRequest,
    _TeacherCreateResponse,
    _TeacherDeleteResponse,
    _TeacherUpdateResponse,
)
from app.entities.teacher.validators import validate_teacher_request
from app.utils.pagination import PaginationParamsDep


class TeacherManager:
    @classmethod
    @validate_teacher_request
    async def create_teacher(
        cls, session: AsyncSession, request_data: TeacherCreateRequest
    ) -> _TeacherCreateResponse:
        teacher = await teacher_repository.create(session, request_data)
        return _TeacherCreateResponse.model_validate(teacher)

    @classmethod
    async def list_teachers(
        cls, session: AsyncSession, pagination: PaginationParamsDep
    ) -> Sequence[TeacherResponse]:
        return await teacher_repository.list_teachers(session, pagination)

    @classmethod
    @validate_teacher_request
    async def update_teacher(
        cls, session: AsyncSession, teacher_id: int, request_data: TeacherUpdateRequest
    ) -> _TeacherUpdateResponse:
        teacher = await teacher_repository.update(session, teacher_id, request_data)
        return _TeacherUpdateResponse.model_validate(teacher)

    @classmethod
    async def delete_teacher(
        cls, session: AsyncSession, teacher_id: int
    ) -> _TeacherDeleteResponse:
        teacher = await teacher_repository.delete(session, teacher_id)
        return _TeacherDeleteResponse.model_validate(teacher)
