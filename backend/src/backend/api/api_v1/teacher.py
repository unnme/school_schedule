from fastapi import APIRouter, status

from backend.api.depends import AsyncSessionDep
from backend.entities.teacher.schemas import (
    TeacherPostRequest,
    TeacherCreateResponse,
    TeacherResponse,
    TeacherUpdateResponse,
    TeacherPutRequest,
)
from backend.entities.teacher.services import TeacherManager
from backend.utils.pagination import PaginationParamsDep

router = APIRouter(prefix="/teachers", tags=["Учителя"])


@router.post("/", response_model=TeacherCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_teacher(session: AsyncSessionDep, request_data: TeacherPostRequest) -> TeacherCreateResponse:
    return await TeacherManager.create_teacher(session, request_data)


@router.get("/", response_model=list[TeacherResponse])
async def list_teachers(session: AsyncSessionDep, params: PaginationParamsDep):
    return await TeacherManager.list_teachers(session, params)


# TODO: router.patch


@router.put("/{teacher_id}", response_model=TeacherUpdateResponse)
async def update_teacher(
    session: AsyncSessionDep, teacher_id: int, request_data: TeacherPutRequest
) -> TeacherUpdateResponse:
    return await TeacherManager.update_teacher(session, teacher_id, request_data)


@router.delete("/{teacher_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_teacher(session: AsyncSessionDep, teacher_id: int) -> None:
    await TeacherManager.delete_teacher(session, teacher_id)
