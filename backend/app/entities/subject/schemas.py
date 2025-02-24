import re
from typing import List

from pydantic import ConfigDict, Field, field_validator

from app.core.base import CustomBaseModel
from app.entities.relations.schemas import (
    StudentGroupWithHoursResponse,
    TeacherWithHoursResponse,
)


class SubjectBaseSchema(CustomBaseModel):
    name: str = Field(
        ...,
        description="Название начинается с заглавной буквы, может содержать кириллицу и дефис.",
    )

    model_config = ConfigDict(json_schema_extra={"example": {"name": "Биология"}})

    @field_validator("name")
    @classmethod
    def validate_subject_name(cls, value: str) -> str:
        if not re.fullmatch(
            r"^[А-ЯЁ][а-яё]+(?:[-\s][А-ЯЁа-яё]+)*$|^[А-ЯЁ]+(?:-[А-ЯЁ]+)?$", value
        ):
            raise ValueError(
                f"Название предмета '{value}' содержит недопустимые символы или имеет неверный формат."
            )
        return value


# REQUEST


class SubjectRequest(SubjectBaseSchema):
    pass


# createREQUEST


class SubjectCreateRequest(SubjectRequest):
    pass


# updateREQUEST


class SubjectUpdateRequest(SubjectRequest):
    pass


# RESPONSE


class SubjectResponse(SubjectBaseSchema):
    id: int
    teachers: List[TeacherWithHoursResponse]
    student_groups: List[StudentGroupWithHoursResponse]


# createRESPONSE


class _SubjectCreateResponse(SubjectBaseSchema):
    id: int


class SubjectCreateResponse(CustomBaseModel):
    message: str
    data: _SubjectCreateResponse


# updateRESPONSE


class _SubjectUpdateResponse(SubjectResponse):
    pass


class SubjectUpdateResponse(CustomBaseModel):
    message: str
    data: _SubjectUpdateResponse


# deleteRESPONSE


class _SubjectDeleteResponse(SubjectBaseSchema):
    id: int


class SubjectDeleteResponse(CustomBaseModel):
    message: str
    data: _SubjectDeleteResponse
