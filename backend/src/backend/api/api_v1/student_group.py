from typing import Sequence

from fastapi import APIRouter, status

from backend.api.depends import AsyncSessionDep
from backend.entities.student_group.schemas import (
    StudentGroupPostRequest,
    StudentGroupCreateResponse,
    StudentGroupResponse,
    StudentGroupPutRequest,
    StudentGroupUpdateResponse,
)
from backend.entities.student_group.services import StudentGroupManager
from backend.utils.pagination import PaginationParamsDep

router = APIRouter(prefix="/student_groups", tags=["Ученические группы"])


@router.post("/", response_model=StudentGroupCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_student_group(
    session: AsyncSessionDep, request_data: StudentGroupPostRequest
) -> StudentGroupCreateResponse:
    return await StudentGroupManager.create_student_group(session, request_data)


@router.get("/", response_model=list[StudentGroupResponse])
async def list_student_groups(session: AsyncSessionDep, params: PaginationParamsDep) -> Sequence[StudentGroupResponse]:
    return await StudentGroupManager.list_student_groups(session, params)


@router.put("/{student_group_id}", response_model=StudentGroupUpdateResponse)
async def update_student_group(
    session: AsyncSessionDep,
    request_data: StudentGroupPutRequest,
    student_group_id: int,
) -> StudentGroupUpdateResponse:
    return await StudentGroupManager.update_student_group(session, student_group_id, request_data)


@router.delete("/{student_group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student_group(db: AsyncSessionDep, student_group_id: int) -> None:
    await StudentGroupManager.delete_student_group(db, student_group_id)
