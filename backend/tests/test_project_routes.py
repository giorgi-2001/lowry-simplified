from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import AsyncClient

from .test_project_dao import TestProjectDao


@pytest_asyncio.fixture
async def new_project():
    project_data = {
        "name": "Project",
        "description": "Description",
        "user_id": 1
    }
    project_id = await TestProjectDao.create_project(project_data=project_data)
    project = await TestProjectDao.get_project_by_id(project_id)
    yield project
    await TestProjectDao.delete_project(project_id)


@pytest_asyncio.fixture
async def others_project():
    project_data = {
        "name": "Project",
        "description": "Description",
        "user_id": 10
    }
    project_id = await TestProjectDao.create_project(project_data=project_data)
    project = await TestProjectDao.get_project_by_id(project_id)
    yield project
    await TestProjectDao.delete_project(project_id)


@pytest.mark.asyncio
async def test_list_projects_no_auth(client: AsyncClient):
    response = await client.get("/projects/")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_list_projects(client: AsyncClient, login_user):
    response = await client.get("/projects/")
    data = response.json()
    assert response.status_code == 200
    assert data is not None


@pytest.mark.asyncio
async def test_get_project_by_id(client: AsyncClient, login_user, new_project):
    response = await client.get(f"/projects/{new_project.id}")
    data = response.json()
    assert response.status_code == 200
    assert data is not None


@pytest.mark.asyncio
async def test_get_project_by_id_not_found(
    client: AsyncClient, login_user, new_project
):
    response = await client.get(f"/projects/{uuid4().hex}")
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Project was not found"


@pytest.mark.asyncio
async def test_get_project_by_id_forbiden(
    client: AsyncClient, login_user, others_project
):
    response = await client.get(f"/projects/{others_project.id}")
    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Forbiden action"


@pytest.mark.asyncio
async def test_create_project(login_user, client: AsyncClient):
    project_data = {
        "name": "name",
        "description": "description",
        "user_id": 1
    }
    response = await client.post("/projects/", json=project_data)
    data = response.json()
    assert response.status_code == 201
    assert data["detail"] is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name, description", [
        ("test", None), (None, "Test"),
        (10, "test"), ("test", 10),
        ("Test", False), (True, "test"),
        ("", "")
    ]
)
async def test_create_project_invalid_values(
    login_user, client: AsyncClient, name, description
):
    project_data = {
        "name": name,
        "description": description,
        "user_id": 1
    }
    response = await client.post("/projects/", json=project_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_project_no_auth(
    client: AsyncClient
):
    project_data = {
        "name": "name",
        "description": "description",
        "user_id": 1
    }
    response = await client.post("/projects/", json=project_data)
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_project(client: AsyncClient, login_user, new_project):
    response = await client.delete(f"/projects/{new_project.id}")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_project_forbiden(
    client: AsyncClient, login_user, others_project
):
    response = await client.delete(f"/projects/{others_project.id}")
    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Forbiden action"


@pytest.mark.asyncio
async def test_delete_project_anauthorized(
    client: AsyncClient, login_user, others_project
):
    client.headers["Authorization"] = "Bearer get-shit"
    response = await client.delete(f"/projects/{others_project.id}")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_project_404(
    client: AsyncClient, login_user, others_project
):
    response = await client.delete(f"/projects/{uuid4().hex}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_project(login_user, client: AsyncClient, new_project):
    project_data = {
        "name": "name2",
        "description": "description2",
        "user_id": 1
    }
    response = await client.put(f"/projects/{new_project.id}", json=project_data)
    data = response.json()
    assert response.status_code == 200
    assert data["detail"] is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name, description", [
        ("test", None), (None, "Test"),
        (10, "test"), ("test", 10),
        ("Test", False), (True, "test"),
        ("", "")
    ]
)
async def test_update_project_invalid_values(
    login_user, client: AsyncClient, name, description, new_project
):
    project_data = {
        "name": name,
        "description": description,
        "user_id": 1
    }
    response = await client.put(f"/projects/{new_project}", json=project_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_project_forbiden(
    client: AsyncClient, login_user, others_project
):
    project_data = {
        "name": "name",
        "description": "description",
        "user_id": 1
    }
    response = await client.put(
        f"/projects/{others_project.id}", json=project_data
    )
    data = response.json()
    assert response.status_code == 403
    assert data["detail"] == "Forbiden action"


@pytest.mark.asyncio
async def test_update_project_anauthorized(
    client: AsyncClient, login_user, others_project
):
    project_data = {
        "name": "name",
        "description": "description",
        "user_id": 1
    }
    client.headers["Authorization"] = "Bearer get-shit"
    response = await client.put(
        f"/projects/{others_project.id}", json=project_data
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_project_404(
    client: AsyncClient, login_user, others_project
):
    project_data = {
        "name": "name",
        "description": "description",
        "user_id": 1
    }
    response = await client.put(
        f"/projects/{uuid4().hex}", json=project_data
    )
    assert response.status_code == 404
