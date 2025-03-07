from fastapi import APIRouter

from app.entities.teacher.services import TeacherManager
from app.core.depends import AsyncSessionDep
from app.utils.pagination import PaginationParamsDep
from app.entities.teacher.schemas import (
    TeacherCreateRequest,
    TeacherCreateResponse,
    TeacherDeleteResponse,
    TeacherResponse,
    TeacherUpdateRequest,
    TeacherUpdateResponse,
)


router = APIRouter(prefix="/teachers", tags=["Учителя"])


@router.post("/", response_model=TeacherCreateResponse)
async def create_teacher(
    session: AsyncSessionDep, request_data: TeacherCreateRequest
) -> TeacherCreateResponse:
    created_teacher = await TeacherManager.create_teacher(session, request_data)
    return TeacherCreateResponse(
        message="Учитель успешно создан.", data=created_teacher
    )


@router.get("/", response_model=list[TeacherResponse])
async def list_teachers(session: AsyncSessionDep, params: PaginationParamsDep):
    teachers = await TeacherManager.list_teachers(session, params)
    return teachers


@router.put("/{teacher_id}", response_model=TeacherUpdateResponse)
async def update_teacher(
    session: AsyncSessionDep, teacher_id: int, request_data: TeacherUpdateRequest
) -> TeacherUpdateResponse:
    updated_teacher = await TeacherManager.update_teacher(
        session, teacher_id, request_data
    )
    return TeacherUpdateResponse(
        message="Учитель успешно обновлен", data=updated_teacher
    )


@router.delete("/{teacher_id}", response_model=TeacherDeleteResponse)
async def delete_teacher(
    session: AsyncSessionDep, teacher_id: int
) -> TeacherDeleteResponse:
    deleted_teacher = await TeacherManager.delete_teacher(session, teacher_id)
    return TeacherDeleteResponse(
        message="Учитель успешно удален", data=deleted_teacher
    )
