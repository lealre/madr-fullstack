from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None


class UserRequestCreate(UserBase):
    password: str


class SuperUserRequestCreate(UserRequestCreate):
    is_active: bool = True
    is_verified: bool = False


class SuperUserRequestUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None
    is_active: bool = True
    is_verified: bool = False


class UserRequestUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    first_name: str | None = None
    last_name: str | None = None


class UserResponse(UserBase):
    id: int
    is_superuser: bool
    is_active: bool
    is_verified: bool
    google_sub: str | None
    model_config = ConfigDict(from_attributes=True)


class UserListResponse(BaseModel):
    users: List[UserResponse]


class PasswordChange(BaseModel):
    password: str
    password_confirmation: str


class GoogleUser(BaseModel):
    sub: int
    email: EmailStr
    email_verified: bool
    given_name: str
    family_name: str
