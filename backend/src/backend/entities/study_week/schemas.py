from pydantic import Field

from backend.entities.base import CustomBaseModel

# INFO: BASE


class StudyWeekBaseSchema(CustomBaseModel):
    week_number: int = Field(..., ge=1, le=53)
    study_year: int = Field(
        ...,
        min_length=2,
        max_length=2,
        ge=24,
    )


# INFO: REQUEST


class StudyWeekRequest(StudyWeekBaseSchema):
    # model_config = {"json_schema_extra": {"example": {"week_number": 2, "study_year": 24}}}
    pass


# INFO: CREATErequest


class StudyWeekCreateRequest(StudyWeekRequest):
    pass


# INFO: UPDATErequest


class StudyWeekUpdateRequest(StudyWeekRequest):
    pass


# INFO: RESPONSE


class StudyWeekResponse(StudyWeekBaseSchema):
    id: int

    # model_config = {
    #     "json_schema_extra": {
    #         "example": {
    #             "id": 1,
    #             "name": "Биология",
    #             "teachers": [
    #                 {"teacher_id": 1, "teaching_hours": 12},
    #                 {"teacher_id": 2, "teaching_hours": 32},
    #             ],
    #             "student_groups": [
    #                 {"student_group_id": 1, "study_hours": 17},
    #                 {"student_group_id": 2, "study_hours": 31},
    #             ],
    #             "classrooms": [{"id": 1}, {"id": 2}],
    #         }
    #     }
    # }


# INFO: CREATEresponse


class _StudyWeekCreateResponse(StudyWeekBaseSchema):
    id: int


class StudyWeekCreateResponse(CustomBaseModel):
    message: str
    data: _StudyWeekCreateResponse


# INFO: UPDATEresponse


class _StudyWeekUpdateResponse(StudyWeekResponse):
    pass


class StudyWeekUpdateResponse(CustomBaseModel):
    message: str
    data: _StudyWeekUpdateResponse


# INFO: DELETEresponse


class _StudyWeekDeleteResponse(StudyWeekBaseSchema):
    id: int


class StudyWeekDeleteResponse(CustomBaseModel):
    message: str
    data: _StudyWeekDeleteResponse
