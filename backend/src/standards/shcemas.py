from pydantic import BaseModel
from datetime import datetime


class StandardResponse(BaseModel):
    id: int
    name: str
    description: str
    image: str
    correlation: float
    slope: float
    y_intercept: float
    created_at: datetime
    updated_at: datetime
