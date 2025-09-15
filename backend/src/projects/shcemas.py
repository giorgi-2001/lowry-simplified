from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class ProjectData(BaseModel):
    name: str = Field(..., max_length=40, min_length=2)
    description: str = Field(..., min_length=4)


class ProjectResponse(ProjectData):
    id: UUID
    user_id: int
    created_at: datetime
