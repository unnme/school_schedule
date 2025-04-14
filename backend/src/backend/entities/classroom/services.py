from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from backend.entities.classroom.schemas import (
    ClassroomCreateResponse,
    ClassroomPostRequest,
    ClassroomPutRequest,
    ClassroomResponse,
    ClassroomUpdateResponse,
)
from backend.utils.pagination import PaginationParamsDep
from backend.entities.classroom.repository import classroom_repository


class ClassroomManager:
    @classmethod  # TODO: @validate_classroom_request
    async def create_classroom(
        cls, session: AsyncSession, request_data: ClassroomPostRequest
    ) -> ClassroomCreateResponse:
        classroom = await classroom_repository.create(session, request_data)
        return ClassroomCreateResponse.model_validate(classroom)

    @classmethod
    async def list_classrooms(
        cls, session: AsyncSession, pagination: PaginationParamsDep
    ) -> Sequence[ClassroomResponse]:
        return await classroom_repository.list_classrooms(session, pagination)

    @classmethod  # TODO: @validate_classroom_request
    async def update_classroom(
        cls,
        session: AsyncSession,
        id: int,
        request_data: ClassroomPutRequest,
    ) -> ClassroomUpdateResponse:
        subject = await classroom_repository.update(session, id, request_data)
        return ClassroomUpdateResponse.model_validate(subject)

    @classmethod
    async def delete_classroom(cls, session: AsyncSession, id: int) -> None:
        await session.delete(await classroom_repository.get_by_id(session, id))
