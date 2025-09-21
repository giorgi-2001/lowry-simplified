import uuid
import datetime
from pydantic import BaseModel, Field


class ExpData(BaseModel):
    project_id: uuid.UUID
    standard_id: int
    name: str = Field(..., max_length=40, min_length=2)
    description: str = Field(..., min_length=4)


class ExpResponse(ExpData):
    id: int
    image: str | None
    csv: str | None
    created_at: datetime.datetime
