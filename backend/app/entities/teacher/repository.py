from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, delete, update, case

from app.utils.pagination import PaginationParamsDep
from app.entities.teacher.schemas import (
    TeacherCreateRequest,
    TeacherUpdateRequest,
)
from app.entities.teacher.models import Teacher
from app.entities.relations.models import TeacherSubject
from app.entities.base import BaseRepository


class TeacherRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(Teacher)

    async def create_teacher(
        self, session: AsyncSession, request_data: TeacherCreateRequest
    ) -> Teacher:
        async with session.begin():
            teacher = Teacher(
                **request_data.model_dump(
                    include={"last_name", "first_name", "patronymic"}
                )
            )
            session.add(teacher)
            await session.flush()
            await self._update_teacher_subjects(session, request_data, teacher)

        teacher = await self.get_by_id(session, teacher.id, load_strategy="selectin")

        return teacher

    async def list_teachers(
        self, session: AsyncSession, pagination: PaginationParamsDep
    ):
        teachers = await self.list_all(session, pagination, load_strategy="selectin")
        return teachers

    async def update_teacher(
        self, session: AsyncSession, teacher_id: int, request_data: TeacherUpdateRequest
    ) -> Teacher:
        teacher = await self.get_by_id(
            session, teacher_id, load_strategy="selectin"
        )

        teacher.is_active = request_data.is_active

        update_data = request_data.model_dump(
            include={"first_name", "last_name", "patronymic"}
        )
        for field, value in update_data.items():
            setattr(teacher, field, value)

        await self._update_teacher_subjects(session, request_data, teacher)
        await session.refresh(teacher)

        return teacher

    async def delete_teacher(self, session: AsyncSession, teacher_id: int) -> Teacher:
        teacher = await self.get_by_id(session, teacher_id)
        deleted_data = {
            key: value
            for key, value in teacher.__dict__.items()
            if not key.startswith("_")
        }
        await session.delete(teacher)
        await session.commit()
        return Teacher(**deleted_data)

    async def _update_teacher_subjects(
        self,
        session: AsyncSession,
        request_data: TeacherCreateRequest | TeacherUpdateRequest,
        teacher: Teacher,
    ) -> None:
        if isinstance(request_data, TeacherCreateRequest):
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

        elif isinstance(request_data, TeacherUpdateRequest):
            request_subj_and_hours = {
                subj.id: subj.teaching_hours for subj in request_data.subjects
            }
            existing_subjects_hours = {
                subj.subject_id: subj.teaching_hours for subj in teacher.subjects
            }

            subjects_to_remove = (
                existing_subjects_hours.keys() - request_subj_and_hours.keys()
            )
            subjects_to_add = (
                request_subj_and_hours.keys() - existing_subjects_hours.keys()
            )
            subjects_to_update = {
                _id
                for _id in request_subj_and_hours.keys()
                & existing_subjects_hours.keys()
                if request_subj_and_hours[_id] != existing_subjects_hours[_id]
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
