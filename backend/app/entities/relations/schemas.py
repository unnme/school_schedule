from pydantic import Field

from app.core.base import CustomBaseModel


class SubjectWithHoursRequest(CustomBaseModel):
    id: int = Field(..., description="ID предмета")
    teaching_hours: int = Field(
        ..., ge=0, description="Количество часов преподавания для предмета"
    )


class TeacherWithHoursResponse(CustomBaseModel):
    teacher_id: int = Field(..., description="ID преподавателя")
    teaching_hours: int = Field(..., ge=0, description="Количество часов преподавания")


class SubjectWithHoursResponse(CustomBaseModel):
    subject_id: int = Field(..., description="ID предмета")
    teaching_hours: int = Field(
        ..., ge=0, description="Количество часов преподавания для предмета"
    )


class StudentGroupWithHoursResponse(CustomBaseModel):
    student_group_id: int = Field(..., description="ID ученического класса")
    study_hours: int = Field(..., ge=0, description="Количество часов обучения")
