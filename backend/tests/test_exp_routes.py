import pytest
import pytest_asyncio
from httpx import AsyncClient

from .test_exp_dao import TestExpDAO
from .test_standard_routes import TestStandardDao
from .test_project_dao import TestProjectDao


@pytest.fixture(scope="module")
def random_uuid():
    return "7f90926d301f4a9ea6768b2c17d4280d"


@pytest.fixture(scope="module")
def exp_data(random_uuid):
    return {
        "name": "Experiment",
        "description": "Experiment",
        "standard_id": 1,
        "project_id": random_uuid
    }


@pytest.fixture
def mock_file():
    content = b"15,20,17"
    corect_format = {"file": ("std.csv", content, "text/csv")}
    wrong_format = {"file": ("std.txt", content, "text/plain")}
    return {
        "correct": corect_format,
        "wrong": wrong_format
    }


@pytest_asyncio.fixture(scope="module")
async def temp_std():
    standard_data = {
        "name": "name",
        "description": "description",
        "image": "img",
        "correlation": 0.9,
        "slope": 2,
        "y_intercept": 0.6,
        "user_id": 1
    }
    standard_id = await TestStandardDao.create_standard(standard_data)
    yield standard_id
    await TestStandardDao.delete_standrd_by_id(standard_id)


@pytest_asyncio.fixture(scope="module")
async def temp_project():
    project_data = {
        "name": "Project",
        "description": "Description",
        "user_id": 1
    }
    project_id = await TestProjectDao.create_project(project_data)
    project_data["user_id"] = 10
    project_id_2 = await TestProjectDao.create_project(project_data)
    yield project_id, project_id_2
    await TestProjectDao.delete_project(project_id)
    await TestProjectDao.delete_project(project_id_2)


@pytest_asyncio.fixture(scope="module", autouse=True)
async def existing_experiment(temp_std, temp_project, exp_data):
    project_id, project_id_2 = temp_project
    exp_data = exp_data.copy()
    exp_data["project_id"] = project_id
    exp_data["standard_id"] = temp_std
    exp_id = await TestExpDAO.create_experiment(exp_data)
    exp_data["project_id"] = project_id_2
    exp_id_2 = await TestExpDAO.create_experiment(exp_data)
    yield exp_id, exp_id_2
    await TestExpDAO.delete_experiment(exp_id)
    await TestExpDAO.delete_experiment(exp_id_2)


@pytest.mark.asyncio
async def test_get_exp_success(
    client: AsyncClient, temp_project, login_user
):
    project_id, _ = temp_project
    response = await client.get(
        "/experiments/", params={"project_id": project_id}
    )
    assert response.status_code == 200
    exp = response.json()[0]
    assert exp["name"] == "Experiment"
    assert exp["description"] == "Experiment"
    assert exp["standard_id"] == 1
    assert exp["project_id"] is not None
    assert exp["csv"] is None
    assert exp["image"] is None


@pytest.mark.asyncio
async def test_get_exp_no_project(
    client: AsyncClient, login_user, random_uuid
):
    response = await client.get(
        "/experiments/", params={"project_id": random_uuid}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == f"Project {random_uuid} does not exists"


@pytest.mark.asyncio
async def test_get_exp_someone_forbiden(
    client: AsyncClient, login_user, temp_project
):
    _, project_id = temp_project
    response = await client.get(
        "/experiments/", params={"project_id": project_id}
    )
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbiden action"


@pytest.mark.asyncio
async def test_delete_exp_no_exp(
    client: AsyncClient, login_user
):
    response = await client.delete("/experiments/125")
    assert response.status_code == 404
    assert response.json()["detail"] == "Experiment 125 does not exists"


@pytest.mark.asyncio
async def test_delete_exp_forbiden(
    client: AsyncClient, login_user, existing_experiment
):
    _, exp_id = existing_experiment
    response = await client.delete(f"/experiments/{exp_id}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbiden action"


@pytest.mark.asyncio
async def test_delete_exp_success(
    client: AsyncClient, login_user
):
    response = await client.delete("/experiments/1")
    assert response.status_code == 200
    assert response.json()["detail"] == "Experiment 1 was deleted"


@pytest.mark.asyncio
@pytest.mark.parametrize("key, replacement", [
    ("name", None),
    ("name", 1),
    ("name", "n"),
    ("description", None),
    ("description", 1),
    ("description", "n"),
    ("standard_id", "something"),
    ("standard_id", None),
    ("project_id", None),
    ("project_id", 125),
])
async def test_create_exp_invalid_data(
    client: AsyncClient, login_user, exp_data, mock_file, key, replacement
):
    exp_data = exp_data.copy()
    exp_data[key] = replacement
    response = await client.post(
        "/experiments/", data=exp_data, files=mock_file["correct"]
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_exp_no_file(
    client: AsyncClient, login_user, exp_data
):
    response = await client.post(
        "/experiments/", data=exp_data
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_exp_wrong_file_type(
    client: AsyncClient, login_user, exp_data, mock_file
):
    response = await client.post(
        "/experiments/", data=exp_data, files=mock_file["wrong"]
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid file type"


@pytest.mark.asyncio
async def test_create_exp_no_std(
    client: AsyncClient, login_user, exp_data, mock_file
):
    exp_data = exp_data.copy()
    exp_data["standard_id"] = 2500
    response = await client.post(
        "/experiments/", data=exp_data, files=mock_file["correct"]
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Standard 2500 does not exists"


@pytest.mark.asyncio
async def test_create_exp_success(
    client: AsyncClient, login_user, exp_data, mock_file
):
    response = await client.post(
        "/experiments/", data=exp_data, files=mock_file["correct"]
    )
    assert response.status_code == 201
    assert response.json()["detail"] == "Experiment 3 was created"
