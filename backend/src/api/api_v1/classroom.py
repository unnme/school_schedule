from fastapi import APIRouter

from src.core.depends import AsyncSessionDep
from src.entities.classroom.schemas import (
    ClassroomCreateRequest,
    ClassroomCreateResponse,
    ClassroomDeleteResponse,
    ClassroomResponse,
    ClassroomUpdateRequest,
    ClassroomUpdateResponse,
)
from src.entities.classroom.services import ClassroomManager
from src.utils.pagination import PaginationParamsDep

router = APIRouter(prefix="/classrooms", tags=["Учебные классы"])


@router.post("/", response_model=ClassroomCreateResponse)
async def create_classroom(
    session: AsyncSessionDep, request_data: ClassroomCreateRequest
) -> ClassroomCreateResponse:
    created_classroom = await ClassroomManager.create_classroom(session, request_data)
    return ClassroomCreateResponse(
        message="Учебный класс успешно создан.", data=created_classroom
    )


@router.get("/", response_model=list[ClassroomResponse])
async def list_classrooms(session: AsyncSessionDep, params: PaginationParamsDep):
    classrooms = await ClassroomManager.list_classrooms(session, params)
    return classrooms


@router.put("/{classroom_id}", response_model=ClassroomUpdateResponse)
async def update_classroom(
    session: AsyncSessionDep, request_data: ClassroomUpdateRequest, classroom_id: int
) -> ClassroomUpdateResponse:
    updated_classroom = await ClassroomManager.update_classroom(
        session, classroom_id, request_data
    )
    return ClassroomUpdateResponse(
        message="Учитель успешно обновлен", data=updated_classroom
    )


@router.delete("/{classroom_id}", response_model=ClassroomDeleteResponse)
async def delete_classroom(
    session: AsyncSessionDep, classroom_id: int
) -> ClassroomDeleteResponse:
    deleted_classroom = await ClassroomManager.delete_classroom(session, classroom_id)
    return ClassroomDeleteResponse(
        message="Учитель успешно удален", data=deleted_classroom
    )
