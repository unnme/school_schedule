from pydantic import Field

from app.entities.base import CustomBaseModel


class SubjectWithTHoursRequest(CustomBaseModel):
    id: int = Field(..., description="ID предмета")
    teaching_hours: int = Field(
        ..., ge=0, description="Количество часов преподавания для предмета"
    )

class SubjectWithSHoursRequest(CustomBaseModel):
    id: int = Field(..., description="ID предмета")
    study_hours: int = Field(
        ..., ge=0, description="Количество часов преподавания для предмета"
    )

class SubjectWithTHoursResponse(CustomBaseModel):
    subject_id: int = Field(..., description="ID предмета")
    teaching_hours: int = Field(
        ..., ge=0, description="Количество часов преподавания для предмета"
    )

class SubjectWithSHoursResponse(CustomBaseModel):
    subject_id: int = Field(..., description="ID предмета")
    study_hours: int = Field(
        ..., ge=0, description="Количество часов преподавания для предмета"
    )

class TeacherWithHoursResponse(CustomBaseModel):
    teacher_id: int = Field(..., description="ID преподавателя")
    teaching_hours: int = Field(..., ge=0, description="Количество часов преподавания")


class StudentGroupWithHoursResponse(CustomBaseModel):
    student_group_id: int = Field(..., description="ID ученического класса")
    study_hours: int = Field(..., ge=0, description="Количество часов обучения")
