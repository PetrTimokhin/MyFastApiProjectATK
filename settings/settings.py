import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 120  # минут

    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USER: str = 'myDataBase1'
    DB_PASS: str = '12345'
    DB_NAME: str = 'postgres'

    @property
    def db_address(self) -> str:
        return (f'postgresql+asyncpg://'
                f'{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}/{self.DB_NAME}')

    model_config = SettingsConfigDict(
        extra="allow",
        env_file_encoding="utf-8",
        # env_file=os.path.abspath(os.path.join(BASE_DIR, ".env")),
        env_file=os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                ".env"))
    )


settings = Settings()
