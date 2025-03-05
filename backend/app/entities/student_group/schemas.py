import re
from typing import List

from fastapi import HTTPException
from pydantic import Field, field_validator

from app.entities.base import CustomBaseModel
from app.entities.relations.schemas import (
    SubjectWithSHoursRequest,
    SubjectWithSHoursResponse,
)


#INFO: BASE


class StudentGroupBaseSchema(CustomBaseModel):
    name: str = Field(
        ..., min_length=2, max_length=5, description="The name of the student group"
    )

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        if not re.match(r"^(?:[1-9]|1[0-1])[А-Я]$", value):
            raise HTTPException(
                status_code=400,
                detail="The group name must consist of a number from 1 to 11, followed by an uppercase letter.",
            )
        return value


#INFO: REQUEST


class StudentGroupRequest(StudentGroupBaseSchema):
    subjects: List[SubjectWithSHoursRequest] = Field(
        default_factory=list,
        description="The student group must be linked to at least one subject",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "11B",
                "subjects": [
                    {"id": 1, "study_hours": 22},
                    {"id": 4, "study_hours": 13},
                ],
            }
        }
    }

    @field_validator("subjects", mode="before")
    def validate_subjects_length(
        cls, value: List[SubjectWithSHoursRequest]
    ) -> List[SubjectWithSHoursRequest]:
        if not value:
            raise HTTPException(
                status_code=400,
                detail="The student group must be linked to at least one subject",
            )
        return value


#INFO: UPDATErequest


class StudentGroupUpdateRequest(StudentGroupRequest):
    pass


#INFO: CREATErequest


class StudentGroupCreateRequest(StudentGroupRequest):
    pass


#INFO: RESPONSE


class StudentGroupResponse(StudentGroupBaseSchema):
    id: int
    subjects: List[SubjectWithSHoursResponse]


#INFO: UPDATEresponse


class _StudentGroupUpdateResponse(StudentGroupResponse):
    pass


class StudentGroupUpdateResponse(CustomBaseModel):
    message: str
    data: _StudentGroupUpdateResponse


#INFO: CREATEresponse


class _StudentGroupCreateResponse(StudentGroupResponse):
    pass


class StudentGroupCreateResponse(CustomBaseModel):
    message: str
    data: _StudentGroupCreateResponse


#INFO: DELETEresponse


class _StudentGroupDeleteResponse(StudentGroupBaseSchema):
    id: int


class StudentGroupDeleteResponse(CustomBaseModel):
    message: str
    data: _StudentGroupDeleteResponse
