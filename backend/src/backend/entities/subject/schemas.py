import re
from typing import List, Optional, get_type_hints

from fastapi import HTTPException
from pydantic import Field, field_validator

from backend.entities.base import CustomBaseModel
from backend.entities.classroom.schemas import ClassroomIDResponse
from backend.entities.relations.schemas import (
    StudentGroupWithHoursResponse,
    TeacherWithHoursResponse,
)

# INFO: BASE


class SubjectBaseSchema(CustomBaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=30,
        description="Название начинается с заглавной буквы, может содержать кириллические буквы и дефис.",
    )

    @field_validator("name")
    @classmethod
    def validate_subject_name(cls, value: str) -> str:
        if not re.fullmatch(
            r"^[А-ЯЁ][а-яё]+(?:[-\s][А-ЯЁа-яё]+)*$|^[А-ЯЁ]+(?:-[А-ЯЁ]+)?$", value
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Название предмета '{value}' содержит недопустимые символы или имеет неправильный формат.",
            )
        return value


# INFO: REQUEST


class SubjectRequest(SubjectBaseSchema):
    model_config = {"json_schema_extra": {"example": {"name": "Биология"}}}


# INFO: CREATErequest


class SubjectPostRequest(SubjectRequest):
    pass


# INFO: UPDATErequest


class SubjectPutRequest(SubjectRequest):
    pass

class SubjectPatchRequest(SubjectRequest):
    __annotations__ = {k: Optional[v] for k, v in get_type_hints(SubjectRequest).items()}

# INFO: RESPONSE


class SubjectResponse(SubjectBaseSchema):
    id: int
    teachers: List[TeacherWithHoursResponse]
    student_groups: List[StudentGroupWithHoursResponse]
    classrooms: List[ClassroomIDResponse]

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Биология",
                "teachers": [
                    {"teacher_id": 1, "teaching_hours": 12},
                    {"teacher_id": 2, "teaching_hours": 32},
                ],
                "student_groups": [
                    {"student_group_id": 1, "study_hours": 17},
                    {"student_group_id": 2, "study_hours": 31},
                ],
                "classrooms": [{"id": 1}, {"id": 2}],
            }
        }
    }


# INFO: CREATEresponse


class SubjectCreateResponse(SubjectBaseSchema):
    id: int


# INFO: UPDATEresponse


class SubjectUpdateResponse(SubjectResponse):
    pass

