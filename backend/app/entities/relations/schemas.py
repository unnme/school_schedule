from pydantic import Field

from app.entities.base import CustomBaseModel


class SubjectWithTHoursRequest(CustomBaseModel):
    id: int = Field(..., description="Subject ID")
    teaching_hours: int = Field(
        ..., ge=0, description="Amount of teaching hours for the subject"
    )


class SubjectWithSHoursRequest(CustomBaseModel):
    id: int = Field(..., description="Subject ID")
    study_hours: int = Field(
        ..., ge=0, description="Amount of study hours for the subject"
    )


class SubjectWithTHoursResponse(CustomBaseModel):
    subject_id: int = Field(..., description="Subject ID")
    teaching_hours: int = Field(
        ..., ge=0, description="Amount of teaching hours for the subject"
    )


class SubjectWithSHoursResponse(CustomBaseModel):
    subject_id: int = Field(..., description="Subject ID")
    study_hours: int = Field(
        ..., ge=0, description="Amount of study hours for the subject"
    )


class TeacherWithHoursResponse(CustomBaseModel):
    teacher_id: int = Field(..., description="Teacher ID")
    teaching_hours: int = Field(..., ge=0, description="Amount of teaching hours")


class StudentGroupWithHoursResponse(CustomBaseModel):
    student_group_id: int = Field(..., description="Student group ID")
    study_hours: int = Field(..., ge=0, description="Amount of study hours")
