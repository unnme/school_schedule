import re
from typing import List, Optional, get_type_hints

from fastapi import HTTPException
from pydantic import Field, field_validator

from backend.entities.base import CustomBaseModel
from backend.entities.relations.schemas import (
    SubjectWithTHoursRequest,
    SubjectWithTHoursResponse,
)

# INFO: BASE


class TeacherBaseSchema(CustomBaseModel):
    last_name: str = Field(
        ..., min_length=2, max_length=30, description="Фамилия учителя"
    )
    first_name: str = Field(..., min_length=2, max_length=30, description="Имя учителя")
    patronymic: str = Field(
        ..., min_length=2, max_length=30, description="Отчество учителя"
    )

    @field_validator("last_name", "first_name", "patronymic")
    def validate_name(cls, value: str) -> str:
        if not re.match(r"^[А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?$", value):
            raise HTTPException(
                status_code=400,
                detail="Поле должно начинаться с заглавной буквы и может содержать дефис между словами",
            )
        return value


# INFO: REQUEST


class TeacherRequest(TeacherBaseSchema):
    subjects: List[SubjectWithTHoursRequest] = Field(
        default_factory=list,
        description="Учитель должен быть связан хотя бы с одним предметом.",
    )

    @field_validator("subjects", mode="before")
    def validate_subjects_length(
        cls, value: List[SubjectWithTHoursRequest]
    ) -> List[SubjectWithTHoursRequest]:
        if not value:
            raise HTTPException(
                status_code=400,
                detail="Учитель должен быть связан хотя бы с одним предметом.",
            )
        return value


# INFO: CREATErequest


class TeacherPostRequest(TeacherRequest):
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


# INFO: UPDATErequest

class _TeacherUpdateRequest(TeacherRequest):
    is_active: bool

    model_config = {
        "json_schema_extra": {
            "example": {
                "first_name": "Дмитрий",
                "last_name": "Мамин-Сибиряк",
                "patronymic": "Наркисович",
                "is_active": True,
                "subjects": [
                    {"id": 1, "teaching_hours": 22},
                    {"id": 4, "teaching_hours": 13},
                ],
            }
        }
    }

class TeacherPutRequest(_TeacherUpdateRequest):
    pass

class TeacherPatchRequest(_TeacherUpdateRequest):
    __annotations__ = {k: Optional[v] for k, v in get_type_hints(TeacherRequest).items()}


# INFO: RESPONSE


class TeacherResponse(TeacherBaseSchema):
    id: int
    is_active: bool = True
    subjects: List[SubjectWithTHoursResponse]


# INFO: UPDATEresponse


class TeacherUpdateResponse(TeacherResponse):
    pass


# INFO: CREATEresponse
class TeacherCreateResponse(TeacherResponse):
    pass


