from typing import Sequence
from fastapi import APIRouter

from app.core.dependencies import AsyncSessionDep, PaginationParams
from app.entities.subject.services import SubjectManager
from app.entities.subject.schemas import (
    SubjectCreateRequest,
    SubjectCreateResponse,
    SubjectDeleteResponse,
    SubjectResponse,
    SubjectUpdateRequest,
    SubjectUpdateResponse,
)


router = APIRouter(prefix="/subjects", tags=["Учебные дисциплины"])


@router.post("/", response_model=SubjectCreateResponse)
async def create_subject(
    session: AsyncSessionDep, request_data: SubjectCreateRequest
) -> SubjectCreateResponse:
    created_subject = await SubjectManager.create_subject(session, request_data)
    return SubjectCreateResponse(message="Предмет успешно создан", data=created_subject)


@router.get("/", response_model=list[SubjectResponse])
async def get_subjects(
    params: PaginationParams, session: AsyncSessionDep
) -> Sequence[SubjectResponse]:
    return await SubjectManager.list_all(session, params, load_stategy="selectin")


@router.put("/{subject_id}", response_model=SubjectUpdateResponse)
async def update_subject(
    session: AsyncSessionDep, subject_id: int, request_data: SubjectUpdateRequest
) -> SubjectUpdateResponse:
    updated_subject = await SubjectManager.update_subject(
        session, subject_id, request_data
    )
    return SubjectUpdateResponse(
        message="Предмет успешно изменен", data=updated_subject
    )


@router.delete("/{subject_id}", response_model=SubjectDeleteResponse)
async def delite_subject(
    session: AsyncSessionDep, subject_id: int
) -> SubjectDeleteResponse:
    deleted_subject = await SubjectManager.delete_subject(session, subject_id)
    return SubjectDeleteResponse(message="Предмет успешно удален", data=deleted_subject)
