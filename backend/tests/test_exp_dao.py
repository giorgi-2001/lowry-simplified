import uuid
import pytest
import pytest_asyncio
from src.experiments.dao import ExperimentDAO
from .database import SessionLocal


class TestExpDAO(ExperimentDAO):
    session_maker = SessionLocal


@pytest.fixture
def exp_data():
    return {
        "name": "Experiment",
        "description": "Experiment",
        "standard_id": 1,
        "project_id": "5a99122e-524c-4f9a-bcf9-011e0dedff75"
    }


@pytest_asyncio.fixture
async def setup_experiment(exp_data):
    return await TestExpDAO.create_experiment(exp_data)


@pytest_asyncio.fixture
async def existing_exp_id(setup_experiment):
    yield setup_experiment
    await TestExpDAO.delete_experiment(setup_experiment)


@pytest.mark.asyncio
async def test_get_exp_by_id(existing_exp_id):
    experiment = await TestExpDAO.get_experiments_by_id(existing_exp_id)
    assert experiment.name == "Experiment"
    assert experiment.description == "Experiment"
    assert experiment.standard_id == 1
    assert experiment.id == 1
    assert experiment.csv is None
    assert experiment.image is None
    assert isinstance(experiment.project_id, uuid.UUID)


@pytest.mark.asyncio
async def test_update_csv(existing_exp_id):
    experiment = await TestExpDAO.update_file(
        experiment_id=existing_exp_id, file_name="new_name",
        file_type="csv"
    )
    assert experiment.csv == "new_name"


@pytest.mark.asyncio
async def test_update_img(existing_exp_id):
    experiment = await TestExpDAO.update_file(
        experiment_id=existing_exp_id, file_name="new_name",
        file_type="img"
    )
    assert experiment.image == "new_name"


@pytest.mark.asyncio
async def test_update_wrong_file_type(existing_exp_id):
    with pytest.raises(ValueError) as e:
        await TestExpDAO.update_file(
            experiment_id=existing_exp_id, file_name="new_name",
            file_type="json"
        )
    assert str(e.value) == "Unsupported file type was provided"
