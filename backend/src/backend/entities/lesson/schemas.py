from typing import Optional

from pydantic import Field
from sqlalchemy import Date

from backend.entities.base import CustomBaseModel

# INFO: BASE


class LessonBaseSchema(CustomBaseModel):
    lesson_number: int
    lesson_date: Date
    school_shift: int = Field(..., ge=1, le=3)

    class_profile: Optional[int] = None

    subject: int
    teacher: int
    student_group: int


# INFO: REQUEST


class LessonRequest(LessonBaseSchema):
    model_config = {
        "json_schema_extra": {
            "example": {
                "lesson_number": 2,
                "lesson_date": "2025-03-19",
                "school_shift": 1,
                "class_profile": None,
                "subject": 1,
                "teacher": 2,
                "student_group": 2,
            }
        }
    }


# INFO: CREATErequest


class LessonCreateRequest(LessonRequest):
    pass


# INFO: UPDATErequest


class LessonUpdateRequest(LessonRequest):
    pass


# INFO: RESPONSE


class LessonResponse(LessonBaseSchema):
    id: int


# INFO: CREATEresponse


class _LessonCreateResponse(LessonBaseSchema):
    id: int


class LessonCreateResponse(CustomBaseModel):
    message: str
    data: _LessonCreateResponse


# INFO: UPDATEresponse


class _LessonUpdateResponse(LessonResponse):
    pass


class LessonUpdateResponse(CustomBaseModel):
    message: str
    data: _LessonUpdateResponse


# INFO: DELETEresponse


class _LessonDeleteResponse(LessonBaseSchema):
    id: int


class LessonDeleteResponse(CustomBaseModel):
    message: str
    data: _LessonDeleteResponse
