from typing import Sequence

from fastapi import APIRouter, status

from backend.api.depends import AsyncSessionDep
from backend.entities.lesson.schemas import (
    LessonPostRequest,
    LessonCreateResponse,
    LessonResponse,
)
from backend.entities.lesson.services import LessonManager
from backend.api.depends import PaginationParamsDep

router = APIRouter(prefix="/lessons", tags=["Уроки"])


@router.post("/", response_model=LessonCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_lesson(session: AsyncSessionDep, request_data: LessonPostRequest) -> LessonCreateResponse:
    return await LessonManager.create_lesson(session, request_data)


@router.get("/", response_model=list[LessonResponse])
async def list_lessons(pagination: PaginationParamsDep, session: AsyncSessionDep) -> Sequence[LessonResponse]:
    return await LessonManager.list_lessons(session, pagination)


# @router.put("/{subject_id}", response_model=SubjectUpdateResponse)
# async def update_subject(
#     session: AsyncSessionDep, subject_id: int, request_data: SubjectUpdateRequest
# ) -> SubjectUpdateResponse:
#     updated_subject = await SubjectManager.update_subject(
#         session, subject_id, request_data
#     )
#     return SubjectUpdateResponse(
#         message="Урок успешно обновлен.", data=updated_subject
#     )
#
#
# @router.delete("/{subject_id}", response_model=SubjectDeleteResponse)
# async def delete_subject(
#     session: AsyncSessionDep, subject_id: int
# ) -> SubjectDeleteResponse:
#     deleted_subject = await SubjectManager.delete_subject(session, subject_id)
#     return SubjectDeleteResponse(
#         message="Урок успешно удален.", data=deleted_subject
#     )
