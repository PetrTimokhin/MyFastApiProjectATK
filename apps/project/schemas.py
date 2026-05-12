from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class ProjectStatus(str, Enum):
    new = "new"
    in_progress = "in_progress"
    completed = "completed"


class ProjectCreate(BaseModel):
    title: str
    description: Optional[str]
    person_id: int


class ProjectUpdate(BaseModel):
    title: Optional[str]
    status: Optional[ProjectStatus]
    start_time: Optional[datetime]
    complete_time: Optional[datetime]
    description: Optional[str]


class ProjectResponse(BaseModel):
    id: int
    title: str
    status: ProjectStatus
    create_time: datetime
    start_time: Optional[datetime]
    complete_time: Optional[datetime]
    description: Optional[str]
    person_id: int

    class ConfigDict:
        from_attributes = True
