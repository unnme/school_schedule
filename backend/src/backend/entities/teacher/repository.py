from typing import List, Optional

from sqlalchemy import case, delete, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from backend.api.depends import PaginationParamsDep

from backend.entities.base import BaseRepository
from backend.entities.relations.models import TeacherSubject
from backend.entities.teacher.models import Teacher
from backend.entities.teacher.schemas import (
    TeacherPostRequest,
    TeacherRequest,
    TeacherPutRequest,
)


class TeacherRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(Teacher)

    async def create(
        self, session: AsyncSession, request_data: TeacherPostRequest
    ) -> Teacher:
        teacher: Teacher = self._set_name(request_data)
        session.add(teacher)
        await session.flush()
        await self._update_teacher_subjects(session, request_data, teacher)

        teacher = await self.get_by_id(session, teacher.id, load_strategy="selectin")
        return teacher

    async def create_many(
        self, session: AsyncSession, request_data_list: List[TeacherPostRequest]
    ):
        async with session.begin():
            teachers = [self._set_name(data) for data in request_data_list]
            session.add_all(teachers)
            await session.flush()

            for teacher, request_data in zip(teachers, request_data_list):
                await self._update_teacher_subjects(session, request_data, teacher)

    async def list_teachers(
        self, session: AsyncSession, pagination: PaginationParamsDep
    ):
        teachers = await self.list_all(session, pagination, load_strategy="selectin")
        return teachers

    async def update(
        self, session: AsyncSession, id: int, request_data: TeacherPutRequest
    ) -> Teacher:
        teacher = await self.get_by_id(session, id, load_strategy="selectin")

        self._set_name(request_data, teacher)
        self._set_active_flag(request_data, teacher)

        await self._update_teacher_subjects(session, request_data, teacher)
        await session.refresh(teacher)
        return teacher

    async def delete(self, session: AsyncSession, id: int) -> None:
        await session.delete(await self.get_by_id(session, id))

    def _set_name(
        self, request_data: TeacherRequest, teacher: Optional[Teacher] = None
    ) -> Teacher:
        if teacher is None:
            teacher = Teacher(
                **request_data.model_dump(
                    include={"last_name", "first_name", "patronymic"}
                )
            )
        else:
            full_name = request_data.model_dump(
                include={"first_name", "last_name", "patronymic"}
            )
            for field, value in full_name.items():
                setattr(teacher, field, value)
        return teacher

    def _set_active_flag(self, request_data, teacher) -> None:
        teacher.is_active = request_data.is_active

    async def _update_teacher_subjects(
        self,
        session: AsyncSession,
        request_data: TeacherPostRequest | TeacherPutRequest,
        teacher: Teacher,
    ) -> None:
        if isinstance(request_data, TeacherPostRequest):
            teacher_subjects = [
                TeacherSubject(
                    teacher_id=teacher.id,
                    subject_id=subj.id,
                    teaching_hours=subj.teaching_hours,
                )
                for subj in request_data.subjects
            ]
            session.add_all(teacher_subjects)
            await session.flush()

        elif isinstance(request_data, TeacherPutRequest):
            request_subj_and_hours: dict = {
                subj.id: subj.teaching_hours for subj in request_data.subjects
            }
            existing_subjects_hours: dict = {
                subj.subject_id: subj.teaching_hours for subj in teacher.subjects
            }

            subjects_to_remove: set = (
                existing_subjects_hours.keys() - request_subj_and_hours.keys()
            )
            subjects_to_add: set = (
                request_subj_and_hours.keys() - existing_subjects_hours.keys()
            )

            subjects_to_update: set = {
                id
                for id in request_subj_and_hours.keys() & existing_subjects_hours.keys()
                if request_subj_and_hours[id] != existing_subjects_hours[id]
            }

            if subjects_to_remove:
                stmt = delete(TeacherSubject).where(
                    (TeacherSubject.teacher_id == teacher.id)
                    & (TeacherSubject.subject_id.in_(subjects_to_remove))
                )
                await session.execute(stmt)

            if subjects_to_update:
                stmt = (
                    update(TeacherSubject)
                    .where(
                        (TeacherSubject.teacher_id == teacher.id)
                        & (TeacherSubject.subject_id.in_(subjects_to_update))
                    )
                    .values(
                        teaching_hours=case(
                            *[
                                (
                                    TeacherSubject.subject_id == _id,
                                    request_subj_and_hours[_id],
                                )
                                for _id in subjects_to_update
                            ],
                            else_=TeacherSubject.teaching_hours,
                        ),
                    )
                )
                await session.execute(stmt)

            if subjects_to_add:
                new_associations = [
                    {
                        "teacher_id": teacher.id,
                        "subject_id": subject_id,
                        "teaching_hours": request_subj_and_hours[subject_id],
                    }
                    for subject_id in subjects_to_add
                ]
                await session.execute(insert(TeacherSubject).values(new_associations))

            await session.flush()


teacher_repository = TeacherRepository()
