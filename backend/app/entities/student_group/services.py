from sqlalchemy import delete, insert, update, case
from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.relations.models import StudentGroupSubject
from app.entities.student_group.validators import validate_student_group_request
from app.services.base_managers import BaseManager
from app.entities.student_group.models import StudentGroup
from app.entities.student_group.schemas import (
    StudentGroupCreateRequest,
    StudentGroupUpdateRequest,
    _StudentGroupCreateResponse,
    _StudentGroupUpdateResponse,
    _StudentGroupDeleteResponse
)



# ============ МЕНЕДЖЕР УЧЕНИЧЕСКИХ ГРУПП =============
class StudentGroupManager(BaseManager):
    model = StudentGroup

    @classmethod
    @validate_student_group_request
    async def create_student_group(
        cls, db: AsyncSession, request_data: StudentGroupCreateRequest
    ) -> _StudentGroupCreateResponse:
        async with db.begin():
            student_group = StudentGroup(**request_data.model_dump(include={"name"}))
            db.add(student_group)
            await db.flush()
            await cls._update_student_group_subjects(db, request_data, student_group)
        student_group = await cls.get_by_id(db, student_group.id, load_strategy="selectin")

        return _StudentGroupCreateResponse.model_validate(student_group)


    @classmethod
    @validate_student_group_request
    async def update_sutdent_group(
        cls,
        db: AsyncSession,
        request_data: StudentGroupUpdateRequest,
        student_group_id: int,
    ) -> _StudentGroupUpdateResponse:
        async with db.begin():
            student_group = await cls.get_by_id(db, student_group_id, load_strategy="selectin")

            update_data = request_data.model_dump(
                include={"name"}
            )
            for field, value in update_data.items():
                setattr(student_group, field, value)

            await cls._update_student_group_subjects(db, request_data, student_group)
            await db.refresh(student_group)

        return _StudentGroupUpdateResponse.model_validate(student_group)


    @classmethod
    async def delete_sutdent_group(cls, db: AsyncSession, student_group_id: int) -> _StudentGroupDeleteResponse:
        student_group = cls.get_by_id(db, student_group_id)
        deleted_data = {key:value for key, value in student_group.__dict__.items() if not key.startswith("_")}
        await db.delete(student_group)
        await db.commit()
        return _StudentGroupDeleteResponse.model_validate(deleted_data)


    @classmethod
    async def _update_student_group_subjects(
        cls,
        db: AsyncSession,
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

            db.add_all(student_group_subjects)
            await db.flush()

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
                await db.execute(stmt)

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
                await db.execute(stmt)

            if subjects_to_add:
                new_associations = [
                    {
                        "student_group_id": student_group.id,
                        "subject_id": subject_id,
                        "study_hours": request_subj_and_hours[subject_id],
                    }
                    for subject_id in subjects_to_add
                ]
                await db.execute(insert(StudentGroupSubject).values(new_associations))

            await db.flush()




