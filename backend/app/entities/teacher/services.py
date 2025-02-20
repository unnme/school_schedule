from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, delete, update, case

from app.entities.teacher.schemas import _TeacherDeleteResponse, TeacherCreateRequest, _TeacherCreateResponse, TeacherUpdateRequest, _TeacherUpdateResponse
from app.entities.teacher.validators import validate_teacher_request
from app.entities.teacher.models import Teacher
from app.entities.relations.models import TeacherSubject
from app.services.base_managers import BaseManager

# ============ МЕНЕДЖЕР ПРЕПОДАВАТЕЛЕЙ =============
class TeacherManager(BaseManager):
    model = Teacher

    @classmethod
    @validate_teacher_request
    async def create_teacher(
        cls, db: AsyncSession, request_data: TeacherCreateRequest
    ) -> _TeacherCreateResponse:
        async with db.begin():
            teacher = Teacher(
                **request_data.model_dump(
                    include={"last_name", "first_name", "patronymic"}
                )
            )
            db.add(teacher)
            await db.flush()

            await cls._update_teacher_subjects(db, request_data, teacher)

        teacher = await cls.get_by_id(db, teacher.id, load_strategy="selectin")

        return _TeacherCreateResponse.model_validate(teacher)

    @classmethod
    @validate_teacher_request
    async def update_teacher(
        cls, db: AsyncSession, request_data: TeacherUpdateRequest, teacher_id: int
    ) -> _TeacherUpdateResponse:
        async with db.begin():
            teacher = await cls.get_by_id(db, teacher_id, load_strategy="selectin")

            teacher.is_active = request_data.is_active

            update_data = request_data.model_dump(
                include={"first_name", "last_name", "patronymic"}
            )
            for field, value in update_data.items():
                setattr(teacher, field, value)

            await cls._update_teacher_subjects(db, request_data, teacher)

            await db.refresh(teacher)

        return _TeacherUpdateResponse.model_validate(teacher)

    @classmethod
    async def delete_teacher(cls, db: AsyncSession, teacher_id: int) -> _TeacherDeleteResponse:
        teacher = await cls.get_by_id(db, teacher_id)
        deleted_data = {
            key: value for key, value in teacher.__dict__.items()if not key.startswith("_")
        }
        await db.delete(teacher)
        await db.commit()
        return _TeacherDeleteResponse.model_validate(deleted_data)

    @classmethod
    async def _update_teacher_subjects(
        cls,
        db: AsyncSession,
        request_data: TeacherUpdateRequest | TeacherCreateRequest,
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

            db.add_all(teacher_subjects)
            await db.flush()

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
                await db.execute(stmt)

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
                await db.execute(stmt)

            if subjects_to_add:
                new_associations = [
                    {
                        "teacher_id": teacher.id,
                        "subject_id": subject_id,
                        "teaching_hours": request_subj_and_hours[subject_id],
                    }
                    for subject_id in subjects_to_add
                ]
                await db.execute(insert(TeacherSubject).values(new_associations))

            await db.flush()

