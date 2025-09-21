import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

import uuid

from src.experiments.models import Experiment


project_id = uuid.uuid4()


@pytest_asyncio.fixture
async def experiment_factory(session: AsyncSession):
    async def make_experiment(
        project_id: str = project_id,
        standard_id: int = 1,
        name: str = "experiment",
        description: str = "new experiment",
        image: str | None = None,
        csv: str | None = None
    ):
        new_exp = Experiment(
            project_id=project_id,
            standard_id=standard_id,
            name=name,
            description=description,
            image=image,
            csv=csv
        )

        session.add(new_exp)
        await session.flush()
        return new_exp
    return make_experiment


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "project_id, standard_id, name, description, img, csv", [
        (project_id, 1, "exp", "new exp", "img", "csv"),
        (project_id, 1, "exp", "new exp", None, "csv"),
        (project_id, 1, "exp", "new exp", "img", None),
    ]
)
async def test_exp_model_success(
    experiment_factory, project_id, standard_id,
    name, description, img, csv,
):
    exp = await experiment_factory(
        project_id, standard_id, name, description, img, csv
    )
    assert exp.id is not None
    assert exp.name == name
    assert exp.description == description
    assert exp.project_id == project_id
    assert exp.standard_id == standard_id
    assert exp.image == img
    assert exp.csv == csv


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "project_id, standard_id, name, description, img, csv", [
        (None, 1, "exp", "new exp", "img", "csv"),
        (project_id, None, "exp", "new exp", "img", "csv"),
        (project_id, 1, None, "new exp", "img", "csv"),
        (project_id, 1, "exp", None, "img", "csv"),
    ]
)
async def test_exp_model_fail(
    experiment_factory, project_id, standard_id,
    name, description, img, csv,
):
    with pytest.raises(SQLAlchemyError):
        await experiment_factory(
            project_id, standard_id, name, description, img, csv
        )
