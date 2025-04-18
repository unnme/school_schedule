from sqlalchemy.ext.asyncio import AsyncSession

from backend.entities.base import ListResponseModel
from backend.entities.classroom.schemas import (
    ClassroomCreateResponse,
    ClassroomPostRequest,
    ClassroomPutRequest,
    ClassroomResponse,
    ClassroomUpdateResponse,
)
from backend.entities.classroom.repository import classroom_repository
from backend.api.depends import PaginationParamsDep


class ClassroomManager:
    @classmethod  # TODO: @validate_classroom_request
    async def create_classroom(
        cls, session: AsyncSession, request_data: ClassroomPostRequest
    ) -> ClassroomCreateResponse:
        classroom = await classroom_repository.create(session, request_data)
        await session.commit()
        return ClassroomCreateResponse.model_validate(classroom)

    @classmethod
    async def list_classrooms(cls, session: AsyncSession, pagination: PaginationParamsDep) -> ListResponseModel:
        classrooms = await classroom_repository.list_classrooms(session, pagination)
        total = await classroom_repository.entity_count(session)
        return ListResponseModel[ClassroomResponse](
            items=classrooms, total=total, limit=pagination.limit, offset=pagination.offset
        )

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
        await classroom_repository.delete(session, id)
        await session.commit()
