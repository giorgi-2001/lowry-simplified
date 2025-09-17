from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UUID

from ..database import Base
from ..users.models import User

from typing import Annotated
import uuid


uuid_pk = Annotated[UUID, mapped_column(
    UUID(as_uuid=True),
    primary_key=True,
    index=True,
    default=uuid.uuid4
)]

text_not_null = Annotated[str, mapped_column(
    nullable=False
)]

user_id = Annotated[int, mapped_column(
    ForeignKey(User.id, ondelete="CASCADE"),
    nullable=False
)]


class Project(Base):
    id: Mapped[uuid_pk]
    user_id: Mapped[user_id]
    name: Mapped[text_not_null]
    description: Mapped[text_not_null]

    experiments = relationship("Experiment", backref="project")

    def __repr__(self):
        return (
            f"Project(Id={self.id} Name={self.name}) "
            f"Description={self.description}"
        )

    def __str__(self):
        return f"<Project {self.name}>"
