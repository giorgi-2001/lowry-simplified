import pytest
from httpx import AsyncClient


base_url = "http://localhost:8000/api/v1/users"

@pytest.fixture
def user_data():
    return {
        "username": "username",
        "email": "email@email.com",
        "password": "password123"
    }


@pytest.mark.asyncio
async def test_list_users(client: AsyncClient):
    response = await client.get("/users/")
    data = response.json()
    assert response.status_code == 200
    assert data is not None


@pytest.mark.asyncio
async def test_register(client: AsyncClient, user_data):
    response = await client.post("/users/register", json=user_data)
    data = response.json()
    assert response.status_code == 201
    assert data["detail"] == "username was created"


@pytest.mark.asyncio
async def test_register_dublicate(client: AsyncClient, user_data):
    response = await client.post("/users/register", json=user_data)
    data = response.json()
    assert response.status_code == 409
    assert data["detail"] == "username or email already in use"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, email, password", [
        ("", "email@email.com", "password123"),
        ("username", "", "password123"),
        ("username", "email@email.com", ""),
        ("username", "email", "password123"),
        ("username", "email@email", "password123"),
        ("username", "email@email.com", "passw"),
    ]
)
async def test_register_invalid_input(
    client: AsyncClient, username, email, password
):
    user_data = {
        "username": username,
        "email": email,
        "password": password
    }
    response = await client.post("/users/register", json=user_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login(client, user_data):
    response = await client.post("/users/login", json=user_data)
    data = response.json()
    assert response.status_code == 200
    assert response.cookies.get("refresh_token") is not None
    assert data["access_token"] is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, password", [
        ("", "pasword123"),
        ("username", ""),
        ("test", "password123"),
        ("username", "password456"),
    ]
)
async def test_login_invalid_credential(
    client: AsyncClient, user_data, username, password
):
    test_data = {"username": username, "password": password}
    await client.post("/users/register", json=user_data)
    response = await client.post(base_url + "/login", json=test_data)
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Invalid login credentials"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, password", [("username", None), (None, "")]
)
async def test_login_no_credentials(
    client: AsyncClient, username, password
):
    test_data = {"username": username, "password": password}
    response = await client.post("/users/login", json=test_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_refresh(client: AsyncClient, login_user):
    response = await client.get("/users/refresh")
    data = response.json()
    assert response.status_code == 200
    assert data["access_token"] is not None


@pytest.mark.asyncio
async def test_my_data(client: AsyncClient, login_user):
    response = await client.get("/users/me")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] is not None
    assert data.get("password") is None
    assert data["username"] == "random_user"
    assert data["email"] == "random@random.com"
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


@pytest.mark.asyncio
async def test_my_data_with_no_header(client: AsyncClient):
    response = await client.get("/users/me")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, login_user):
    response = await client.delete("/users/")
    data = response.json()
    assert response.status_code == 200
    assert data["detail"] == "random_user was deleted"
    

@pytest.mark.asyncio
async def test_delete_user_with_no_header(client: AsyncClient):
    response = await client.delete("/users/")
    assert response.status_code == 403
