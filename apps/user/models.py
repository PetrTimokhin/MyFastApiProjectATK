from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from DATABASES.db_postgres.base import Base

# from apps.project.models import Project


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    # username: Mapped[str] = mapped_column(String, unique=True)
    username: Mapped[Optional[str]] = mapped_column(String, unique=False, nullable=True)
    password: Mapped[str] = mapped_column(String)

    projects: Mapped[list["Project"]] = relationship(back_populates="person")
