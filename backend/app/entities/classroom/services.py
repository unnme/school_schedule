from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.classroom.schemas import (
    ClassroomCreateRequest,
    ClassroomResponse,
    ClassroomUpdateRequest,
    _ClassroomCreateResponse,
    _ClassroomDeleteResponse,
    _ClassroomUpdateResponse,
)
from app.utils.pagination import PaginationParamsDep
from app.api.depends.repository import classroom_repository



class ClassroomManager:
    @classmethod  # TODO: @validate_classroom_request
    async def create_classroom(
        cls, session: AsyncSession, request_data: ClassroomCreateRequest
    ) -> _ClassroomCreateResponse:
        classroom = await classroom_repository.create_classroom(session, request_data)
        return _ClassroomCreateResponse.model_validate(classroom)

    @classmethod
    async def list_classrooms(
        cls, session: AsyncSession, pagination: PaginationParamsDep
    ) -> Sequence[ClassroomResponse]:
        subjects = await classroom_repository.list_classrooms(session, pagination)
        return subjects

    @classmethod  # TODO: @validate_classroom_request
    async def update_classroom(
        cls,
        session: AsyncSession,
        classroom_id: int,
        request_data: ClassroomUpdateRequest,
    ) -> _ClassroomUpdateResponse:
        subject = await classroom_repository.update_classroom(
            session, classroom_id, request_data
        )
        return _ClassroomUpdateResponse.model_validate(subject)

    @classmethod
    async def delete_classroom(
        cls, session: AsyncSession, classroom_id: int
    ) -> _ClassroomDeleteResponse:
        subject = await classroom_repository.delete_classroom(session, classroom_id)
        return _ClassroomDeleteResponse.model_validate(subject)
