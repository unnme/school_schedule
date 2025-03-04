from pydantic import Field

from app.entities.base import BaseSchema


class SubjectWithTHoursRequest(BaseSchema):
    id: int = Field(..., description="ID предмета")
    teaching_hours: int = Field(
        ..., ge=0, description="Количество часов преподавания для предмета"
    )


class SubjectWithSHoursRequest(BaseSchema):
    id: int = Field(..., description="ID предмета")
    study_hours: int = Field(
        ..., ge=0, description="Количество часов преподавания для предмета"
    )


class SubjectWithTHoursResponse(BaseSchema):
    subject_id: int = Field(..., description="ID предмета")
    teaching_hours: int = Field(
        ..., ge=0, description="Количество часов преподавания для предмета"
    )


class SubjectWithSHoursResponse(BaseSchema):
    subject_id: int = Field(..., description="ID предмета")
    study_hours: int = Field(
        ..., ge=0, description="Количество часов преподавания для предмета"
    )


class TeacherWithHoursResponse(BaseSchema):
    teacher_id: int = Field(..., description="ID преподавателя")
    teaching_hours: int = Field(..., ge=0, description="Количество часов преподавания")


class StudentGroupWithHoursResponse(BaseSchema):
    student_group_id: int = Field(..., description="ID ученического класса")
    study_hours: int = Field(..., ge=0, description="Количество часов обучения")
