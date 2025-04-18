from datetime import date

from pydantic import Field

from backend.entities.base import CustomBaseModel

# INFO: BASE


class LessonBaseSchema(CustomBaseModel):
    lesson_date: date
    school_shift: int = Field(..., ge=1, le=3)
    lesson_number: int = Field(..., ge=0, le=8)

    classroom: int
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
                "classroom": 1,
                "subject": 1,
                "teacher": 1,
                "student_group": 1,
            }
        }
    }


# INFO: CREATErequest


class LessonPostRequest(LessonRequest):
    pass


# INFO: UPDATErequest


class LessonPutRequest(LessonRequest):
    pass


# INFO: RESPONSE


class LessonResponse(LessonBaseSchema):
    id: int
    lesson_day: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 2,
                "lesson_number": 2,
                "lesson_date": "2025-03-19",
                "school_shift": 1,
                "classroom": 1,
                "subject": 1,
                "teacher": 1,
                "student_group": 1,
            }
        }
    }


# INFO: CREATEresponse


class LessonCreateResponse(LessonResponse):
    pass


# INFO: UPDATEresponse


class LessonUpdateResponse(LessonResponse):
    pass
