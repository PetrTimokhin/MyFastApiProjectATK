"""База Данных"""""
from typing import Dict

from apps.user.schemas import User
from settings.settings import settings


class IdCounterUser:
    """Хранит и инкрементирует последнее ID для пользователей в БД."""
    __current_id: int = 0

    @classmethod
    def _get_next_id(cls) -> int:
        cls.__current_id += 1
        return cls.__current_id


class DescriptorDB:
    def __init__(self):
        self.__storage = {}

    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:  # обращение через класс cls
            return self
        raise AttributeError("Прямой доступ к 'db' запрещён. "
                             "Используйте get_store() или set_store_data().")

    def __set__(self, instance, value):
        raise AttributeError("Прямой доступ к 'db' запрещён.")

    # служебные методы
    def _get(self):
        return self.__storage

    def _set(self, value: Dict):
        self.__storage = value


class DataBaseStore:
    _instance = None
    db = DescriptorDB()

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_store(self):
        return type(self).db._get()

    def set_store(self, value: Dict[int, User]):
        type(self).db._set(value)


class ContextManagerDB:
    """Контекстный менеджер БД """
    def __init__(self):
        self.settings = settings

    def __enter__(self) -> DataBaseStore:
        # print(f"[DB CONNECT] присоединение к {self.settings.db_address}")
        print("[DB CONNECT] соединение с БД установлено!")
        return DataBaseStore()

    def __exit__(self, exc_type, exc, tb):
        # print(f"[DB DISCONNECT] отсоединение от {self.settings.db_address}")
        print("[DB DISCONNECT] соединение с БД закрыто!")

# Контекстный менеджер для инициализации (полезно для реальных БД)
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Здесь могла бы быть инициализация БД
#     print("Application startup...")
#     yield  # yield db например
#     print("Application shutdown...")

# # проверка работы модуля
# if __name__ == '__main__':
#     s1 = DealsStore()
#     s2 = DealsStore()
#
#     print(s1 is s2)           # True
