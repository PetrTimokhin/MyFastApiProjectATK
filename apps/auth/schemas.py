from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional


# Модели для регистрации и логина
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str


# class TokenData(BaseModel):
#     email: Optional[str] = None
#     scopes: Optional[list[str]] = None


class UserBaseAuth(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3)


class UserAfterRegister(UserBaseAuth):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserRegister(UserBaseAuth):
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)


# class UserResponse(User):
#     id: int
#
#     model_config = ConfigDict(from_attributes=True)


# from pydantic import BaseModel
#
# class User(BaseModel):
#     username: str
#     email: str = None
#     full_name: str = None
#     disabled: bool = None
#
#
# class UserInDB(User):
#     hashed_password: str
