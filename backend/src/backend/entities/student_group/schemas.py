import re
from typing import Annotated, List, Optional

from fastapi import HTTPException
from pydantic import Field, field_validator

from backend.entities.base import CustomBaseModel
from backend.entities.relations.schemas import (
    SubjectWithSHoursRequest,
    SubjectWithSHoursResponse,
)

# INFO: BASE


class StudentGroupBaseSchema(CustomBaseModel):
    name: str = Field(..., min_length=2, max_length=5, description="Название группы студентов.")

    capacity: Annotated[
        Optional[int],
        Field(
            ge=1,
            le=50,
            description="Максимальное количество студентов в группе.",
        ),
    ] = None

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        if not re.match(r"^(?:[1-9]|1[0-1])-[А-Я]$", value):
            raise HTTPException(
                status_code=400,
                detail="Название группы должно содержать число от 1 до 11, за которым следует тире с заглавной буквой русского алфавита.",
            )
        return value


# INFO: REQUEST


class StudentGroupRequest(StudentGroupBaseSchema):
    subjects: List[SubjectWithSHoursRequest] = Field(
        default_factory=list,
        description="Группа студентов должна быть связана хотя бы с одним предметом.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "11-Г",
                "capacity": 33,
                "subjects": [
                    {"id": 1, "study_hours": 22},
                    {"id": 4, "study_hours": 13},
                ],
            }
        }
    }

    @field_validator("subjects", mode="before")
    def validate_subjects_length(cls, value: List[SubjectWithSHoursRequest]) -> List[SubjectWithSHoursRequest]:
        if not value:
            raise HTTPException(
                status_code=400,
                detail="Группа студентов должна быть связана хотя бы с одним предметом.",
            )
        return value


# INFO: UPDATErequest


class StudentGroupPutRequest(StudentGroupRequest):
    pass


# INFO: CREATErequest


class StudentGroupPostRequest(StudentGroupRequest):
    pass


# INFO: RESPONSE


class StudentGroupResponse(StudentGroupBaseSchema):
    id: int
    subjects: List[SubjectWithSHoursResponse]

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "11-Г",
                "capacity": 33,
                "subjects": [
                    {"id": 1, "study_hours": 22},
                    {"id": 2, "study_hours": 0},
                    {"id": 3, "study_hours": 13},
                ],
            }
        }
    }


# INFO: UPDATEresponse


class StudentGroupUpdateResponse(StudentGroupResponse):
    pass


# INFO: CREATEresponse


class StudentGroupCreateResponse(StudentGroupResponse):
    pass
