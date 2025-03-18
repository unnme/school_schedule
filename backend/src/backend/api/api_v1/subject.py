from typing import Sequence

from fastapi import APIRouter

from backend.core.depends import AsyncSessionDep
from backend.entities.subject.schemas import (
    SubjectCreateRequest,
    SubjectCreateResponse,
    SubjectDeleteResponse,
    SubjectResponse,
    SubjectUpdateRequest,
    SubjectUpdateResponse,
)
from backend.entities.subject.services import SubjectManager
from backend.utils.pagination import PaginationParamsDep

router = APIRouter(prefix="/subjects", tags=["Учебные дисциплины"])


@router.post("/", response_model=SubjectCreateResponse)
async def create_subject(
    session: AsyncSessionDep, request_data: SubjectCreateRequest
) -> SubjectCreateResponse:
    created_subject = await SubjectManager.create_subject(session, request_data)
    return SubjectCreateResponse(
        message="Предмет успешно создан.", data=created_subject
    )


@router.get("/", response_model=list[SubjectResponse])
async def list_subjects(
    pagination: PaginationParamsDep, session: AsyncSessionDep
) -> Sequence[SubjectResponse]:
    subjects = await SubjectManager.list_subjects(session, pagination)
    return subjects


@router.put("/{subject_id}", response_model=SubjectUpdateResponse)
async def update_subject(
    session: AsyncSessionDep, subject_id: int, request_data: SubjectUpdateRequest
) -> SubjectUpdateResponse:
    updated_subject = await SubjectManager.update_subject(
        session, subject_id, request_data
    )
    return SubjectUpdateResponse(
        message="Предмет успешно обновлен.", data=updated_subject
    )


@router.delete("/{subject_id}", response_model=SubjectDeleteResponse)
async def delete_subject(
    session: AsyncSessionDep, subject_id: int
) -> SubjectDeleteResponse:
    deleted_subject = await SubjectManager.delete_subject(session, subject_id)
    return SubjectDeleteResponse(
        message="Предмет успешно удален.", data=deleted_subject
    )
