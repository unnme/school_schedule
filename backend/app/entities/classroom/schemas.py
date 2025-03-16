import re
from typing import Annotated, List, Optional

from fastapi import HTTPException
from pydantic import Field, field_validator

from app.entities.base import CustomBaseModel
from app.entities.relations.schemas import SubjectIDRequest, SubjectIDResponse

# INFO: BASE


class ClassroomBaseSchema(CustomBaseModel):
    name: str = Field(
        ..., min_length=1, max_length=5, description="Название классной комнаты."
    )
    capacity: Annotated[
        Optional[int],
        Field(
            gt=0,
            le=50,
            description="Вместимость (чел.) классной комнаты",
        ),
    ] = None

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        if not re.match(r"^(?:[1-9][0-9]{0,2}|1000)(?:-[а-я])?$", value):
            raise HTTPException(
                status_code=400,
                detail="Название классной комнаты должно состоять из цифры (1-1000) или из цифры и строчной буквы через тире.",
            )
        return value


# INFO: REQUEST


class ClassroomRequest(ClassroomBaseSchema):
    subjects: List[SubjectIDRequest] = Field(
        default_factory=list,
        description="Закрепленные за классной комнатой предметы обучения",
    )

    model_config = {
        "json_schema_extra": {
            "example": {"name": "111-а", "capacity": None, "subjects": []}
        }
    }


# INFO: UPDATErequest


class ClassroomUpdateRequest(ClassroomRequest):
    pass


# INFO: CREATErequest


class ClassroomCreateRequest(ClassroomRequest):
    pass


# INFO: RESPONSE


class ClassroomResponse(ClassroomBaseSchema):
    id: int
    subjects: List[SubjectIDResponse]


class ClassroomIDResponse(CustomBaseModel):
    id: int


# INFO: UPDATEresponse


class _ClassroomUpdateResponse(ClassroomResponse):
    pass


class ClassroomUpdateResponse(CustomBaseModel):
    message: str
    data: _ClassroomUpdateResponse


# INFO: CREATEresponse


class _ClassroomCreateResponse(ClassroomResponse):
    pass


class ClassroomCreateResponse(CustomBaseModel):
    message: str
    data: _ClassroomCreateResponse


# INFO: DELETEresponse


class _ClassroomDeleteResponse(ClassroomBaseSchema):
    id: int


class ClassroomDeleteResponse(CustomBaseModel):
    message: str
    data: _ClassroomDeleteResponse
