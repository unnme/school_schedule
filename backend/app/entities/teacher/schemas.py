import re
from typing import List, Annotated
from pydantic import Field, field_validator

from app.entities.base import CustomBaseModel
from app.entities.relations.schemas import (
    SubjectWithHoursRequest,
    SubjectWithHoursResponse,
)

LastName = Annotated[
    str, Field(..., min_length=2, max_length=30, description="Фамилия преподавателя")
]
FirstName = Annotated[
    str, Field(..., min_length=2, max_length=30, description="Имя преподавателя")
]
Patronymic = Annotated[
    str, Field(..., min_length=2, max_length=30, description="Отчество преподавателя")
]


class TeacherBaseSchema(CustomBaseModel):
    last_name: LastName
    first_name: FirstName
    patronymic: Patronymic

    @field_validator("last_name", "first_name", "patronymic")
    def validate_name(cls, value: str) -> str:
        if not re.match(r"^[А-ЯЁ][а-яё]+(-[А-ЯЁ][а-яё]+)?$", value):
            raise ValueError(
                "Поле должно начинаться с заглавной буквы и может содержать дефис между словами."
            )
        return value


class TeacherRequest(TeacherBaseSchema):
    subjects: List[SubjectWithHoursRequest] = Field(
        default_factory=list,
        description="Преподаватель должен быть связан хотя бы с одним предметом.",
    )

    @field_validator("subjects", mode="before")
    def validate_subjects_length(
        cls, value: List[SubjectWithHoursRequest]
    ) -> List[SubjectWithHoursRequest]:
        if not value:
            raise ValueError(
                "Преподаватель должен быть связан хотя бы с одним предметом."
            )
        return value


class TeacherUpdateRequest(TeacherRequest):
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


class TeacherResponse(TeacherBaseSchema):
    id: int
    is_active: bool = True
    subjects: List[SubjectWithHoursResponse]


class _TeacherUpdateResponse(TeacherResponse):
    pass


class _TeacherCreateResponse(TeacherResponse):
    pass


class TeacherUpdateResponse(CustomBaseModel):
    message: str
    data: _TeacherUpdateResponse


class TeacherCreateResponse(CustomBaseModel):
    message: str
    data: _TeacherCreateResponse


class _TeacherDeleteResponse(TeacherBaseSchema):
    id: int


class TeacherDeleteResponse(CustomBaseModel):
    message: str
    data: _TeacherDeleteResponse
