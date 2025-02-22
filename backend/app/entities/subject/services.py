from sqlalchemy.ext.asyncio import AsyncSession

from app.entities.subject.schemas import SubjectCreateRequest, SubjectUpdateRequest, _SubjectCreateResponse, _SubjectUpdateResponse, _SubjectDeleteResponse
from app.entities.subject.models import Subject
from app.entities.subject.validators import validate_subject_request
from app.services.base_managers import BaseManager


# ============= МЕНЕДЖЕР ПРЕДМЕТОВ ==============
class SubjectManager(BaseManager):
    model = Subject

    @classmethod
    @validate_subject_request
    async def create_subject(
        cls, db: AsyncSession, request_data: SubjectCreateRequest
    ) -> _SubjectCreateResponse:
        new_subject = Subject(name=request_data.name)
        db.add(new_subject)
        await db.commit()
        await db.refresh(new_subject)
        return _SubjectCreateResponse.model_validate(new_subject)

    @classmethod
    @validate_subject_request
    async def update_subject(
        cls, db: AsyncSession, subject_id: int, request_data: SubjectUpdateRequest
    ) -> _SubjectUpdateResponse:
        subject = await cls.get_by_id(db, subject_id, load_strategy="selectin")

        if request_data.name != subject.name:
            subject.name = request_data.name
            await db.commit()
            await db.refresh(subject)
        return _SubjectUpdateResponse.model_validate(subject)

    @classmethod
    async def delete_subject(cls, db: AsyncSession, subject_id: int) -> _SubjectDeleteResponse:
        subject = await cls.get_by_id(db, subject_id)
        deleted_data = {
            key: value
            for key, value in subject.__dict__.items()
            if not key.startswith("_")
        }
        await db.delete(subject)
        await db.commit()
        return _SubjectDeleteResponse.model_validate(deleted_data)



