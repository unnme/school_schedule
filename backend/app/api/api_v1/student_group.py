from typing import Sequence
from fastapi import APIRouter

from app.core.dependencies import AsyncSessionDep, PaginationParams
from app.entities.student_group.services import StudentGroupManager
from app.entities.student_group.schemas import (
    StudentGroupCreateRequest,
    StudentGroupCreateResponse,
    StudentGroupDeleteResponse,
    StudentGroupResponse,
    StudentGroupUpdateRequest,
    StudentGroupUpdateResponse,
)


router = APIRouter(prefix="/student_groups")


@router.post("/", response_model=StudentGroupCreateResponse)
async def create_sudent_group(
    session: AsyncSessionDep, request_data: StudentGroupCreateRequest
) -> StudentGroupCreateResponse:
    created_student_group = await StudentGroupManager.create_student_group(
        session, request_data
    )
    return StudentGroupCreateResponse(
        message="Группа учеников успешно создана", data=created_student_group
    )


@router.get("/", response_model=list[StudentGroupResponse])
async def get_sudent_groups(
    session: AsyncSessionDep, params: PaginationParams
) -> Sequence[StudentGroupResponse]:
    return await StudentGroupManager.list_all(session, params, load_stategy="selectin")


@router.put("/{student_group_id}", response_model=StudentGroupUpdateResponse)
async def update_sutdent_group(
    session: AsyncSessionDep,
    request_data: StudentGroupUpdateRequest,
    student_group_id: int,
) -> StudentGroupUpdateResponse:
    udated_student_group = await StudentGroupManager.update_sutdent_group(
        session, request_data, student_group_id
    )
    return StudentGroupUpdateResponse(
        message="Группа учеников успешно обновлёна", data=udated_student_group
    )


@router.delete("/{student_group_id}", response_model=StudentGroupDeleteResponse)
async def delete_student_group(
    db: AsyncSessionDep, student_group_id: int
) -> StudentGroupDeleteResponse:
    deleted_student_group = await StudentGroupManager.delete_sutdent_group(
        db, student_group_id
    )
    return StudentGroupDeleteResponse(
        message="Группа учеников успешно удалена", data=deleted_student_group
    )
