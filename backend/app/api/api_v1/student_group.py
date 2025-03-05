from typing import Sequence
from fastapi import APIRouter

from app.utils.pagination import PaginationParamsDep
from app.core.database import AsyncSessionDep
from app.entities.student_group.services import StudentGroupManager
from app.entities.student_group.schemas import (
    StudentGroupCreateRequest,
    StudentGroupCreateResponse,
    StudentGroupDeleteResponse,
    StudentGroupResponse,
    StudentGroupUpdateRequest,
    StudentGroupUpdateResponse,
)


router = APIRouter(prefix="/student_groups", tags=["Ученические группы"])


@router.post("/", response_model=StudentGroupCreateResponse)
async def create_student_group(
    session: AsyncSessionDep, request_data: StudentGroupCreateRequest
) -> StudentGroupCreateResponse:
    created_student_group = await StudentGroupManager.create_student_group(
        session, request_data
    )
    return StudentGroupCreateResponse(
        message="The student group was successfully created", data=created_student_group
    )


@router.get("/", response_model=list[StudentGroupResponse])
async def list_student_groups(
    session: AsyncSessionDep, params: PaginationParamsDep
) -> Sequence[StudentGroupResponse]:
    return await StudentGroupManager.list_student_groups(
        session, params
    )


@router.put("/{student_group_id}", response_model=StudentGroupUpdateResponse)
async def update_student_group(
    session: AsyncSessionDep,
    request_data: StudentGroupUpdateRequest,
    student_group_id: int,
) -> StudentGroupUpdateResponse:
    updated_student_group = await StudentGroupManager.update_student_group(
        session, request_data, student_group_id
    )
    return StudentGroupUpdateResponse(
        message="The student group was successfully updated", data=updated_student_group
    )


@router.delete("/{student_group_id}", response_model=StudentGroupDeleteResponse)
async def delete_student_group(
    db: AsyncSessionDep, student_group_id: int
) -> StudentGroupDeleteResponse:
    deleted_student_group = await StudentGroupManager.delete_student_group(
        db, student_group_id
    )
    return StudentGroupDeleteResponse(
        message="The student group was successfully deleted", data=deleted_student_group
    )
