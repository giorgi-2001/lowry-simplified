from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import CheckConstraint

from typing import Annotated

from ..database import Base


int_pk = Annotated[int, mapped_column(
    primary_key=True,
    unique=True,
    index=True
)]

username = Annotated[str, mapped_column(
    unique=True, nullable=False, index=True
)]
email = Annotated[str, mapped_column(unique=True, nullable=False)]
password = Annotated[str, mapped_column(nullable=False)]


class User(Base):
    id: Mapped[int_pk]
    username: Mapped[username]
    email: Mapped[email]
    password: Mapped[password]

    standards = relationship("Standard", backref="user")

    __table_args__ = (
        CheckConstraint("LENGTH(username) > 1", name="username_min_length"),
        CheckConstraint("LENGTH(email) > 5", name="email_min_length"),
        CheckConstraint("LENGTH(password) > 8", name="password_min_length"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at)
        }

    def __repr__(self):
        return f"<User id={self.id} {self.username}>"
