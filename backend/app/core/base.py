from pydantic import BaseModel


class CustomBaseModel(BaseModel):
    class Config:
        from_attributes = True


class PaginationParamsModel(BaseModel):
    offset: int
    limit: int
    order_by: str | None
    desc: bool
