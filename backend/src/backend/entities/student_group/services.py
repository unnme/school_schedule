from sqlalchemy.ext.asyncio import AsyncSession

from backend.entities.base import ListResponseModel
from backend.entities.student_group.schemas import (
    StudentGroupPostRequest,
    StudentGroupCreateResponse,
    StudentGroupResponse,
    StudentGroupPutRequest,
    StudentGroupUpdateResponse,
)
from backend.api.depends import PaginationParamsDep

from backend.entities.student_group.repository import student_group_repository
from backend.entities.student_group.validators import validate_student_group_request


class StudentGroupManager:
    @classmethod
    @validate_student_group_request
    async def create_student_group(
        cls, session: AsyncSession, request_data: StudentGroupPostRequest
    ) -> StudentGroupCreateResponse:
        async with session.begin():
            student_group = await student_group_repository.create(session, request_data)
            return StudentGroupCreateResponse.model_validate(student_group)

    @classmethod
    async def list_student_groups(cls, session: AsyncSession, pagination: PaginationParamsDep) -> ListResponseModel:
        student_groups = await student_group_repository.list_student_groups(session, pagination)
        total = await student_group_repository.entity_count(session)
        return ListResponseModel[StudentGroupResponse](
            items=student_groups, total=total, limit=pagination.limit, offset=pagination.offset
        )

    @classmethod
    @validate_student_group_request
    async def update_student_group(
        cls,
        session: AsyncSession,
        id: int,
        request_data: StudentGroupPutRequest,
    ) -> StudentGroupUpdateResponse:
        async with session.begin():
            student_group = await student_group_repository.update(session, id, request_data)
            return StudentGroupUpdateResponse.model_validate(student_group)

    @classmethod
    async def delete_student_group(cls, session: AsyncSession, id: int) -> None:
        await session.delete(await student_group_repository.get_by_id(session, id))
        await session.commit()
