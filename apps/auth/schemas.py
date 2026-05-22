from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm


# Модели для регистрации и логина
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str


# class TokenData(BaseModel):
#     email: Optional[str] = None
#     scopes: Optional[list[str]] = None


# Эти все модели ушли в user
# class UserBaseAuth(BaseModel):
#     email: EmailStr = Field(..., min_length=3)


# class UserAfterRegister(UserBaseAuth):
#     id: int | None
#
#     model_config = ConfigDict(from_attributes=True)

#
# class UserForRegister(UserBaseAuth):
#     password: str = Field(..., min_length=6)
#
#
# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str = Field(..., min_length=6)
#
#
# class UserAfterLogin(BaseModel):
#     email: EmailStr
#     id: int


# # Создаем нашу кастомную форму
# class SimpleLoginForm(OAuth2PasswordRequestForm):
#     # Мы явно переопределяем поля, которые хотим разрешить.
#     # Поскольку username и password уже есть в базовом классе,
#     # мы можем оставить их, но убрать опциональные поля:
#
#     scope: Optional[str] = Field(None,
#                                  exclude=True)  # Исключаем из сериализации/ожидания
#     client_id: Optional[str] = Field(None, exclude=True)
#     client_secret: Optional[str] = Field(None, exclude=True)
#
#     # ВАЖНО: Если вы хотите убедиться, что клиент не присылает НИЧЕГО лишнего,
#     # нужно использовать model_config (или Config в старых версиях Pydantic)
#     model_config = {
#         "extra": "forbid"
#         # Запрещает принимать любые поля, не объявленные явно
#     }


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
