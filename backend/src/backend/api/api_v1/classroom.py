from fastapi import APIRouter, status

from backend.api.depends import AsyncSessionDep
from backend.entities.classroom.schemas import (
    ClassroomPostRequest,
    ClassroomCreateResponse,
    ClassroomResponse,
    ClassroomPutRequest,
    ClassroomUpdateResponse,
)
from backend.entities.classroom.services import ClassroomManager
from backend.utils.pagination import PaginationParamsDep

router = APIRouter(prefix="/classrooms", tags=["Учебные классы"])


@router.post("/", response_model=ClassroomCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_classroom(session: AsyncSessionDep, request_data: ClassroomPostRequest) -> ClassroomCreateResponse:
    return await ClassroomManager.create_classroom(session, request_data)


@router.get("/", response_model=list[ClassroomResponse])
async def list_classrooms(session: AsyncSessionDep, params: PaginationParamsDep):
    return await ClassroomManager.list_classrooms(session, params)


@router.put("/{classroom_id}", response_model=ClassroomUpdateResponse)
async def update_classroom(
    session: AsyncSessionDep, request_data: ClassroomPutRequest, classroom_id: int
) -> ClassroomUpdateResponse:
    return await ClassroomManager.update_classroom(session, classroom_id, request_data)


@router.delete("/{classroom_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_classroom(session: AsyncSessionDep, classroom_id: int) -> None:
    await ClassroomManager.delete_classroom(session, classroom_id)
