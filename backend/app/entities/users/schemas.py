import uuid

from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass


# # Shared properties
# class UserBase:
#     email: EmailStr
#     is_active: bool = True
#     is_superuser: bool = False
#     full_name: str | None
#
#
# # Properties to receive via API on creation
# class UserCreate(UserBase):
#     password: str
#
#
# class UserRegister:
#     email: EmailStr
#     password: str
#     full_name: str | None
#
#
# # Properties to receive via API on update, all are optional
# class UserUpdate(UserBase):
#     email: EmailStr | None = None
#     password: str | None = None
#
#
# class UserUpdateMe:
#     full_name: str | None = None
#     email: EmailStr | None = None
#
#
# class UpdatePassword:
#     current_password: str
#     new_password: str
#
#
# # Properties to return via API, id is always required
# class UserPublic(UserBase):
#     id: uuid.UUID
#
#
# # Item model
# class ItemBase:
#     title: str
#     description: str | None
#
#
# class ItemCreate(ItemBase):
#     pass
#
#
# class ItemUpdate(ItemBase):
#     title: str | None
#
#
# # Generic message
# class Message:
#     message: str
#
#
# # JSON payload containing access token
# class Token:
#     access_token: str
#     token_type: str = "bearer"
#
#
# # Contents of JWT token
# class TokenPayload:
#     sub: str | None = None
#
#
# class NewPassword:
#     token: str
#     new_password: str
