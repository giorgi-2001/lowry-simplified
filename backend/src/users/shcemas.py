from pydantic import BaseModel, Field, field_validator

from typing import Annotated
from datetime import datetime
import re


class UserData(BaseModel):
    username: Annotated[str, Field(..., min_length=2, max_length=60)]
    email: Annotated[str, Field(..., min_length=5, max_length=60)]
    password: Annotated[str, Field(..., min_length=8, max_length=60)]

    @field_validator("email")
    def validate_email(cls, email):
        regex = r"^(?!.*\.\.)[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(regex, email):
            raise ValueError("Invalid email")
        return email
    

class UserLoginData(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    updated_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str

