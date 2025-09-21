from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from ..database import Base
from ..users.models import User
from typing import Annotated


int_pk = Annotated[int, mapped_column(
    primary_key=True,
    unique=True,
    index=True
)]

text = Annotated[str, mapped_column(nullable=False)]
img = Annotated[str, mapped_column(nullable=True)]
float_not_null = Annotated[float, mapped_column(nullable=False)]
user_id = Annotated[int, mapped_column(
    ForeignKey(User.id, ondelete="CASCADE"), nullable=False, index=True
)]


class Standard(Base):
    id: Mapped[int_pk]
    name: Mapped[text]
    description: Mapped[text]
    image: Mapped[img]
    correlation: Mapped[float_not_null]
    slope: Mapped[float_not_null]
    y_intercept: Mapped[float_not_null]

    user_id: Mapped[user_id]

    def __repr__(self):
        return f"<Standard {self.name} | a={self.y_intercept} b={self.slope}>"
