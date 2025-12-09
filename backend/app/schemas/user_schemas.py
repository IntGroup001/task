from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict, field_serializer

from app.utils.enums import UserRoleEnum


class UserBase(BaseModel):
    email: EmailStr
    username: str
    role: UserRoleEnum


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    role: UserRoleEnum = UserRoleEnum.user


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None
    role: UserRoleEnum | None = None
    is_active: bool | None = None


class UserUpdatePassword(BaseModel):
    password: str


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    is_active: bool

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info):
        return str(id)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    refresh_token: str
