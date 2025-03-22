from typing import Sequence

from fastapi import APIRouter

from backend.core.depends import AsyncSessionDep
from backend.entities.lesson.schemas import (
    LessonCreateRequest,
    LessonCreateResponse,
    LessonResponse,
)
from backend.entities.lesson.services import LessonManager
from backend.utils.pagination import PaginationParamsDep

router = APIRouter(prefix="/lessons", tags=["Уроки"])


@router.post("/", response_model=LessonCreateResponse)
async def create_lesson(
    session: AsyncSessionDep, request_data: LessonCreateRequest
) -> LessonCreateResponse:
    created_subject = await LessonManager.create_lesson(session, request_data)
    return LessonCreateResponse(message="Урок успешно создан.", data=created_subject)


@router.get("/", response_model=list[LessonResponse])
async def list_lessons(
    pagination: PaginationParamsDep, session: AsyncSessionDep
) -> Sequence[LessonResponse]:
    lessons = await LessonManager.list_lessons(session, pagination)
    return lessons


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
