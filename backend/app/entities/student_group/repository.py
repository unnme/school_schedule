from sqlalchemy import delete, insert, update, case
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.base import BaseRepository
from app.entities.relations.models import StudentGroupSubject
from app.entities.student_group.models import StudentGroup
from app.entities.student_group.schemas import (
    StudentGroupCreateRequest,
    StudentGroupUpdateRequest,
)
from app.utils.pagination import PaginationParamsDep


class StudentGroupRepository(BaseRepository):
    def __init__(self) -> None:
        super().__init__(StudentGroup)

    async def create_student_group(
        self, session: AsyncSession, request_data: StudentGroupCreateRequest
    ) -> StudentGroup:
        async with session.begin():
            student_group = StudentGroup(**request_data.model_dump(include={"name"}))
            session.add(student_group)
            await session.flush()
            await self._update_student_group_subjects(
                session, request_data, student_group
            )
        student_group = await self.get_by_id(
            session, student_group.id, load_strategy="selectin"
        )

        return student_group

    async def list_student_groups(
        self, session: AsyncSession, pagination: PaginationParamsDep
    ):
        student_groups = await self.list_all(
            session, pagination, load_strategy="selectin"
        )
        return student_groups

    async def update_sutdent_group(
        self,
        session: AsyncSession,
        request_data: StudentGroupUpdateRequest,
        student_group_id: int,
    ) -> StudentGroup:
        async with session.begin():
            student_group = await self.get_by_id(
                session, student_group_id, load_strategy="selectin"
            )

            update_data = request_data.model_dump(include={"name"})
            for field, value in update_data.items():
                setattr(student_group, field, value)

            await self._update_student_group_subjects(
                session, request_data, student_group
            )
            await session.refresh(student_group)

        return student_group

    async def delete_student_group(
        self, session: AsyncSession, student_group_id: int
    ) -> StudentGroup:
        student_group = self.get_by_id(session, student_group_id)
        deleted_data = {
            key: value
            for key, value in student_group.__dict__.items()
            if not key.startswith("_")
        }
        await session.delete(student_group)
        await session.commit()
        return StudentGroup(**deleted_data)

    async def _update_student_group_subjects(
        self,
        session: AsyncSession,
        request_data: StudentGroupCreateRequest | StudentGroupUpdateRequest,
        student_group: StudentGroup,
    ) -> None:
        if isinstance(request_data, StudentGroupCreateRequest):
            student_group_subjects = [
                StudentGroupSubject(
                    student_group_id=student_group.id,
                    subject_id=subj.id,
                    study_hours=subj.study_hours,
                )
                for subj in request_data.subjects
            ]

            session.add_all(student_group_subjects)
            await session.flush()

        elif isinstance(request_data, StudentGroupUpdateRequest):
            request_subj_and_hours = {
                subj.id: subj.study_hours for subj in request_data.subjects
            }
            existing_subjects_hours = {
                subj.subject_id: subj.study_hours for subj in student_group.subjects
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
                stmt = delete(StudentGroupSubject).where(
                    (StudentGroupSubject.student_group_id == student_group.id)
                    & (StudentGroupSubject.subject_id.in_(subjects_to_remove))
                )
                await session.execute(stmt)

            if subjects_to_update:
                stmt = (
                    update(StudentGroupSubject)
                    .where(
                        (StudentGroupSubject.student_group_id == student_group.id)
                        & (StudentGroupSubject.subject_id.in_(subjects_to_update))
                    )
                    .values(
                        study_hours=case(
                            *[
                                (
                                    StudentGroupSubject.subject_id == _id,
                                    request_subj_and_hours[_id],
                                )
                                for _id in subjects_to_update
                            ],
                            else_=StudentGroupSubject.study_hours,
                        ),
                    )
                )
                await session.execute(stmt)

            if subjects_to_add:
                new_associations = [
                    {
                        "student_group_id": student_group.id,
                        "subject_id": subject_id,
                        "study_hours": request_subj_and_hours[subject_id],
                    }
                    for subject_id in subjects_to_add
                ]
                await session.execute(
                    insert(StudentGroupSubject).values(new_associations)
                )

            await session.flush()


student_group_repository = StudentGroupRepository()
