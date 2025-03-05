import re
from typing import List

from pydantic import Field, field_validator

from app.entities.base import CustomBaseModel
from app.entities.relations.schemas import (
    StudentGroupWithHoursResponse,
    TeacherWithHoursResponse,
)


#INFO: BASE


class SubjectBaseSchema(CustomBaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=30,
        description="The name starts with a capital letter, may contain Cyrillic letters and a hyphen.",
    )

    @field_validator("name")
    @classmethod
    def validate_subject_name(cls, value: str) -> str:
        if not re.fullmatch(
            r"^[А-ЯЁ][а-яё]+(?:[-\s][А-ЯЁа-яё]+)*$|^[А-ЯЁ]+(?:-[А-ЯЁ]+)?$", value
        ):
            raise ValueError(
                f"The subject name '{value}' contains invalid characters or has an incorrect format."
            )
        return value


#INFO: REQUEST


class SubjectRequest(SubjectBaseSchema):
    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Biology"
            }
        }
    }

#INFO: CREATErequest


class SubjectCreateRequest(SubjectRequest):
    pass


#INFO: UPDATErequest


class SubjectUpdateRequest(SubjectRequest):
    pass


#INFO: RESPONSE


class SubjectResponse(SubjectBaseSchema):
    id: int
    teachers: List[TeacherWithHoursResponse]
    student_groups: List[StudentGroupWithHoursResponse]


#INFO: CREATEresponse


class _SubjectCreateResponse(SubjectBaseSchema):
    id: int


class SubjectCreateResponse(CustomBaseModel):
    message: str
    data: _SubjectCreateResponse


#INFO: UPDATEresponse


class _SubjectUpdateResponse(SubjectResponse):
    pass


class SubjectUpdateResponse(CustomBaseModel):
    message: str
    data: _SubjectUpdateResponse


#INFO: DELETEresponse


class _SubjectDeleteResponse(SubjectBaseSchema):
    id: int


class SubjectDeleteResponse(CustomBaseModel):
    message: str
    data: _SubjectDeleteResponse
