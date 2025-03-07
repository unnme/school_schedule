from pydantic import Field

from app.entities.base import CustomBaseModel

#INFO: REQUEST

class SubjectIDRequest(CustomBaseModel):
    id: int = Field(..., description="ID предмета")


class SubjectWithTHoursRequest(CustomBaseModel):
    id: int = Field(..., description="ID предмета")
    teaching_hours: int = Field(
        ..., ge=0, description="Количество часов преподавания"
    )


class SubjectWithSHoursRequest(CustomBaseModel):
    id: int = Field(..., description="ID предмета")
    study_hours: int = Field(
        ..., ge=0, description="Количество часов обучения"
    )

#INFO: RESPONSE

class SubjectIDResponse(CustomBaseModel):
    id: int = Field(..., description="ID предмета")

class TeacherWithHoursResponse(CustomBaseModel):
    teacher_id: int = Field(..., description="ID преподавателя")
    teaching_hours: int = Field(..., ge=0, description="Количество часов преподавания")


class StudentGroupWithHoursResponse(CustomBaseModel):
    student_group_id: int = Field(..., description="ID ученического класса")
    study_hours: int = Field(..., ge=0, description="Количество часов обучения")


class SubjectWithTHoursResponse(CustomBaseModel):
    subject_id: int = Field(..., description="ID предмета")
    teaching_hours: int = Field(
        ..., ge=0, description="Количество часов преподавания"
    )


class SubjectWithSHoursResponse(CustomBaseModel):
    subject_id: int = Field(..., description="ID предмета")
    study_hours: int = Field(
        ..., ge=0, description="Количество часов обучения"
    )



