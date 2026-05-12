"""Модуль для pydantic схем пользователя User"""
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class User(BaseModel):
    email: EmailStr


class UserCreate(User):
    password: str


class UserUpdate(User):
    username: Optional[str] = Field(..., min_length=3)
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserResponse(User):
    id: int

    model_config = ConfigDict(from_attributes=True)
