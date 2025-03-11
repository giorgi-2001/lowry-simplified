from pydantic import BaseModel, Field
from uuid import UUID


class ProjectData(BaseModel):
    name: str = Field(..., max_length=40, min_length=2)
    description: str = Field(..., min_length=4)
    user_id: int


class ProjectResponse(ProjectData):
    id: UUID
