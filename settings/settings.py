import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    #-------jwt----------
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 120  # минут

    #-------database______
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    #------test---------
    TESTING: bool = False
    TEST_DB_NAME: str = "test_db"


    @property
    def db_address(self) -> str:
        if self.TESTING:
            db_name = self.TEST_DB_NAME
        else:
            db_name = self.DB_NAME
        return (f'postgresql+asyncpg://'
                f'{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{db_name}')

    model_config = SettingsConfigDict(
        extra="allow",
        env_file_encoding="utf-8",
        env_file=os.path.abspath(
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                ".env"))
    )


settings = Settings()
