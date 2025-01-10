import pytest
import pytest_asyncio
from httpx import AsyncClient
from pathlib import Path

from src.standards.models import Standard
from .database import SessionLocal


@pytest_asyncio.fixture
async def temp_std():
    async def wrapper(user_id: int):
        async with SessionLocal() as session:
            async with session.begin():
                std = Standard(
                    name="name", description="desc", image="img",
                    correlation=0.9, slope=2, y_intercept=0.6,
                    user_id=user_id
                )
                session.add(std)
                await session.commit()
            await session.refresh(std)
            return std
    return wrapper


@pytest.mark.asyncio
async def test_list_all_standards(client: AsyncClient):
    response = await client.get("/standards/")
    assert response.status_code == 200
    data = response.json()
    assert data is not None


@pytest.mark.asyncio
async def test_get_standards_by_username_no_header(client):
    response = await client.get("/standards/my-standards")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_standards_by_username(client, login_user):
    response = await client.get("/standards/my-standards")
    data = response.json()
    assert response.status_code == 200
    assert data is not None


@pytest.mark.asyncio
async def test_upload_file_no_auth(client: AsyncClient):
    response = await client.post("/standards/")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_upload_file(client: AsyncClient, login_user):
    path = (
        Path(__file__).parent.joinpath("media")
        .joinpath("standard.csv").resolve()
    ) 
    form_data = {
        "name": "Plot",
        "description": "description"
    }
    with open(path, "rb") as file:
        content = file.read()
        files = {"file": ("std.csv", content, "text/csv")}
        response = await client.post("/standards/", data=form_data, files=files)
        assert response.status_code == 201
        assert response.json()["task_id"] is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name, description, file_name, file_content, content_type, status_code", [
        ("name", "description", "file.csv", None, "text/csv", 400),
        ("name", "description", "file.txt", b"text", "text/csv", 400),
        ("name", "description", "file.txt", b"text", "text/plain", 400),
        (None, "description", "file.csv", b"text", "text/csv", 422),
        ("name", None, "file.csv", b"text", "text/csv", 422),

    ]
)
async def test_file_upload_errors(
    client: AsyncClient, login_user, name, description,
    file_name, file_content, content_type, status_code
):
    files = {"file": (file_name, file_content, content_type)}
    form_data = {"name": name, "description": description}
    response = await client.post("/standards/", data=form_data, files=files)
    assert response.status_code == status_code


@pytest.mark.asyncio
async def test_delete_standard_no_auth(client):
    response = await client.delete(f"/standards/{1}")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_standard_not_found(client, login_user):
    response = await client.delete(f"/standards/{5}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Standard was not found"


@pytest.mark.asyncio
async def test_delete_standard_forbiden(
    client: AsyncClient, login_user, temp_std
):
    std = await temp_std(user_id=15)
    response = await client.delete(f"/standards/{std.id}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Forbidden Action"


@pytest.mark.asyncio
async def test_delete_standard(
    client: AsyncClient, login_user, temp_std
):  
    std = await temp_std(user_id=1)
    response = await client.delete(f"/standards/{std.id}")
    assert response.status_code == 200
    assert response.json()["detail"] == f"Standard {std.id} was deleted"