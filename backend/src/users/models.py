from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import Annotated

from ..database import Base


int_pk = Annotated[int, mapped_column(
    primary_key=True,
    unique=True,
    index=True
)]

username = Annotated[str, mapped_column(unique=True, nullable=False)]
email = Annotated[str, mapped_column(unique=True, nullable=False)]
password = Annotated[str, mapped_column(nullable=False)]

class User(Base):
    id: Mapped[int_pk]
    username: Mapped[username]
    email: Mapped[email]
    password: Mapped[password]

    # projects = relationship("Project", backref="user")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": str(self.created_at),
            "updated_": str(self.updated_)
        }

    def __repr__(self):
        return self.username