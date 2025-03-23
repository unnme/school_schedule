from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.depends.repository import classroom_repository, subject_repository
from backend.core.logging_config import get_logger
from backend.entities.classroom.schemas import ClassroomCreateRequest
from backend.entities.subject.schemas import SubjectCreateRequest



logger = get_logger(__name__)


class MassInit:

    @classmethod
    async def init_classrooms(cls, session: AsyncSession, classroom_names: List[str]):
        request_data_list = [
            ClassroomCreateRequest(name=name) for name in classroom_names 
        ]

        await classroom_repository.create_many(session, request_data_list)
            
    @classmethod
    async def init_subjects(cls, session: AsyncSession, subject_names: List[str]):
        request_data_list = [
            SubjectCreateRequest(name=name) for name in subject_names
        ]
        await subject_repository.create_many(session, request_data_list)
