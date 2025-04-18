from fastapi import APIRouter, status

from backend.api.depends import AsyncSessionDep
from backend.entities.base import ListResponseModel
from backend.entities.lesson.schemas import (
    LessonPostRequest,
    LessonCreateResponse,
)
from backend.entities.lesson.services import LessonManager
from backend.api.depends import PaginationParamsDep

router = APIRouter(prefix="/lessons", tags=["Уроки"])


@router.post("/", response_model=LessonCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_lesson(session: AsyncSessionDep, request_data: LessonPostRequest) -> LessonCreateResponse:
    return await LessonManager.create_lesson(session, request_data)


@router.get("/", response_model=ListResponseModel)
async def list_lessons(pagination: PaginationParamsDep, session: AsyncSessionDep) -> ListResponseModel:
    return await LessonManager.list_lessons(session, pagination)
