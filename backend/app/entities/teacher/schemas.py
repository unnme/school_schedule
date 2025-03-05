import re
from typing import List, Annotated
from fastapi import HTTPException
from pydantic import Field, field_validator

from app.entities.base import CustomBaseModel
from app.entities.relations.schemas import (
    SubjectWithTHoursRequest,
    SubjectWithTHoursResponse,
)


#INFO: BASE


class TeacherBaseSchema(CustomBaseModel):
    last_name: str = Field(
        ..., min_length=2, max_length=30, description="Teacher's last name"
    )
    first_name: str = Field(
        ..., min_length=2, max_length=30, description="Teacher's first name"
    )
    patronymic: str = Field(
        ..., min_length=2, max_length=30, description="Teacher's patronymic"
    )

    @field_validator("last_name", "first_name", "patronymic")
    def validate_name(cls, value: str) -> str:
        if not re.match(r"^[А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?$", value):
            raise HTTPException(
                status_code=400,
                detail="The field must start with a capital letter and may contain a hyphen between words",
            )
        return value


#INFO: REQUEST


class TeacherRequest(TeacherBaseSchema):
    subjects: List[SubjectWithTHoursRequest] = Field(
        default_factory=list,
        description="The teacher must be linked to at least one subject.",
    )

    @field_validator("subjects", mode="before")
    def validate_subjects_length(
        cls, value: List[SubjectWithTHoursRequest]
    ) -> List[SubjectWithTHoursRequest]:
        if not value:
            raise ValueError("The teacher must be linked to at least one subject.")
        return value


#INFO: UPDATErequest


class TeacherUpdateRequest(TeacherRequest):
    is_active: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "Дмитрий",
                "last_name": "Мамин-Сибиряк",
                "patronymic": "Наркисович",
                "is_active": True, #NFO: is important
                "subjects": [
                    {"id": 1, "teaching_hours": 22},
                    {"id": 4, "teaching_hours": 13},
                ],
            }
        }
    }


#INFO: CREATErequest


class TeacherCreateRequest(TeacherRequest):
    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "Дмитрий",
                "last_name": "Мамин-Сибиряк",
                "patronymic": "Наркисович",
                "subjects": [
                    {"id": 1, "teaching_hours": 22},
                    {"id": 4, "teaching_hours": 13},
                ],
            }
        }
    }


#INFO: RESPONSE


class TeacherResponse(TeacherBaseSchema):
    id: int
    is_active: bool = True
    subjects: List[SubjectWithTHoursResponse]


#INFO: UPDATEresponse


class _TeacherUpdateResponse(TeacherResponse):
    pass


class TeacherUpdateResponse(CustomBaseModel):
    message: str
    data: _TeacherUpdateResponse


#INFO: CREATEresponse
class _TeacherCreateResponse(TeacherResponse):
    pass


class TeacherCreateResponse(CustomBaseModel):
    message: str
    data: _TeacherCreateResponse


#INFO: DELETEresponse


class _TeacherDeleteResponse(TeacherBaseSchema):
    id: int


class TeacherDeleteResponse(CustomBaseModel):
    message: str
    data: _TeacherDeleteResponse
