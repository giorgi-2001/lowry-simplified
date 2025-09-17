from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UUID
from ..database import Base
from ..standards.models import Standard, int_pk, text, img
from ..projects.models import Project

from typing import Annotated


project_id = Annotated[
    UUID, mapped_column(ForeignKey(Project.id), nullable=False)
]

standard_id = Annotated[
    int, mapped_column(ForeignKey(Standard.id), nullable=False)
]


class Experiment(Base):
    id: Mapped[int_pk]
    project_id: Mapped[project_id]
    standard_id: Mapped[standard_id]
    name: Mapped[text]
    description: Mapped[text]
    image: Mapped[img]
    csv: Mapped[img]

    standard = relationship(Standard)

    def __repr__(self):
        return f"<Experiment {self.name}>"
