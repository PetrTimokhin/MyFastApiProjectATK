"""Модели SQLAlchemy для взаимодействия с БД PostgreSQL"""

import enum
from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from DATABASES.db_postgres.base import Base


class ProjectStatus(str, enum.Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String, unique=True)
    status: Mapped[ProjectStatus] = mapped_column(Enum(ProjectStatus))

    create_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    start_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    complete_time: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    description: Mapped[str | None] = mapped_column(Text)

    person_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    person: Mapped["User"] = relationship(back_populates="projects")
