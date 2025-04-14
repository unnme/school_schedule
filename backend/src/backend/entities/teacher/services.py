from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from backend.entities.teacher.schemas import (
    TeacherCreateResponse,
    TeacherPostRequest,
    TeacherPutRequest,
    TeacherResponse,
    TeacherUpdateResponse,
)
from backend.entities.teacher.validators import validate_teacher_request
from backend.utils.pagination import PaginationParamsDep
from backend.entities.teacher.repository import teacher_repository


class TeacherManager:
    @classmethod
    @validate_teacher_request
    async def create_teacher(cls, session: AsyncSession, request_data: TeacherPostRequest) -> TeacherCreateResponse:
        async with session.begin():
            teacher = await teacher_repository.create(session, request_data)
        return TeacherCreateResponse.model_validate(teacher)

    @classmethod
    async def list_teachers(cls, session: AsyncSession, pagination: PaginationParamsDep) -> Sequence[TeacherResponse]:
        return await teacher_repository.list_teachers(session, pagination)

    @classmethod
    @validate_teacher_request
    async def update_teacher(
        cls, session: AsyncSession, id: int, request_data: TeacherPutRequest
    ) -> TeacherUpdateResponse:
        async with session.begin():
            teacher = await teacher_repository.update(session, id, request_data)
        return TeacherUpdateResponse.model_validate(teacher)

    @classmethod
    async def delete_teacher(cls, session: AsyncSession, id: int) -> None:
        await session.delete(await teacher_repository.get_by_id(session, id))
        await session.commit()
