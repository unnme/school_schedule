from typing import Sequence

from fastapi import APIRouter, status

from backend.entities.subject.services import SubjectManager
from backend.utils.pagination import PaginationParamsDep
from backend.api.depends import AsyncSessionDep
from backend.entities.subject.schemas import (
    SubjectCreateResponse,
    SubjectPostRequest,
    SubjectUpdateResponse,
    SubjectResponse,
    SubjectPutRequest,
)


router = APIRouter(prefix="/subjects", tags=["Учебные дисциплины"])


@router.post("/", response_model=SubjectCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_subject(session: AsyncSessionDep, request_data: SubjectPostRequest) -> SubjectCreateResponse:
    return await SubjectManager.create_subject(session, request_data)


@router.get("/", response_model=list[SubjectResponse])
async def list_subjects(pagination: PaginationParamsDep, session: AsyncSessionDep) -> Sequence[SubjectResponse]:
    return await SubjectManager.list_subjects(session, pagination)


@router.put("/{subject_id}", response_model=SubjectUpdateResponse)
async def update_subject(
    session: AsyncSessionDep, subject_id: int, request_data: SubjectPutRequest
) -> SubjectUpdateResponse:
    return await SubjectManager.update_subject(session, subject_id, request_data)


@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject(session: AsyncSessionDep, subject_id: int) -> None:
    await SubjectManager.delete_subject(session, subject_id)
