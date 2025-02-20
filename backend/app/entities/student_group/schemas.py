import re
from typing import Any, List, Annotated

from pydantic import Field, field_validator

from app.core.base import CustomBaseModel
from app.entities.relations.schemas import (
    SubjectWithHoursRequest,
    SubjectWithHoursResponse,
)


StudentGroupName = Annotated[
    str,
    Field(..., min_length=2, max_length=5, description="Название ученической группы"),
]


class StudentGroupBaseSchema(CustomBaseModel):

    name: StudentGroupName

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        if not re.match(r"^(?:[1-9]|1[0-1])[А-Я]$", value):
            raise ValueError(
                "Название группы должно быть числом от 1 до 11, за которым следует одна заглавная буква."
            )
        return value


class StudentGroupRequest(StudentGroupBaseSchema):
    subjects: List[Any] = Field(
        default_factory=list,
        description="Ученическая группа должна быть связанна хотя бы с одним предметом",
    )

    @field_validator("subjects", mode="before")
    def validate_subjects_length(
        cls, value: List[SubjectWithHoursRequest]
    ) -> List[SubjectWithHoursRequest]:
        if not value:
            raise ValueError(
                "Ученическая группа должна быть связанна хотя бы с одним предметом"
            )
        return value


class StudentGroupUpdateRequest(StudentGroupRequest):

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "11Б",
                "subjects": [{"id": 1, "study_hours": 22}],
            }
        }
    }


class StudentGroupCreateRequest(StudentGroupRequest):

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "11Б",
                "subjects": [
                    {"id": 1, "study_hours": 22},
                    {"id": 4, "study_hours": 13},
                ],
            }
        }
    }


class StudentGroupResponse(StudentGroupBaseSchema):
    id: int
    subjects: List[SubjectWithHoursResponse]


class _StudentGroupUpdateResponse(StudentGroupResponse):
    pass


class _StudentGroupCreateResponse(StudentGroupResponse):
    pass


class StudentGroupUpdateResponse(CustomBaseModel):
    message: str
    data: _StudentGroupUpdateResponse


class StudentGroupCreateResponse(CustomBaseModel):
    message: str
    data: _StudentGroupCreateResponse


class _StudentGroupDeleteResponse(StudentGroupBaseSchema):
    id: int


class StudentGroupDeleteResponse(CustomBaseModel):
    message: str
    data: _StudentGroupDeleteResponse
