from pydantic import BaseModel, Field
from datetime import datetime


class StandardData(BaseModel):
    name: str = Field(min_length=4, max_length=40)
    description: str = Field(min_length=4)


class StandardResponse(StandardData):
    id: int
    image: str
    correlation: float
    slope: float
    y_intercept: float
    created_at: datetime
    updated_at: datetime