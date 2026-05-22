"""Модуль для pydantic схем пользователя User"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    email: EmailStr


# class UserCreate(User):
#     password: str


class UserCreate(UserBase):
    password: str
    username: Optional[str] = None


class UserAfterCreate(BaseModel):
    email: EmailStr
    id: int


class UserUpdate(UserBase):
    username: Optional[str] = Field(..., min_length=3)
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserAfterRegister(UserBase):
    id: int | None

    model_config = ConfigDict(from_attributes=True)


class UserForRegister(UserBase):
    password: str = Field(..., min_length=4)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
