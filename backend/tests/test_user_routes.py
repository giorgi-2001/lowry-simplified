import pytest
from fastapi.testclient import TestClient


base_url = "http://localhost:8000/api/v1/users"

@pytest.fixture
def user_data():
    return {
        "username": "username",
        "email": "email@email.com",
        "password": "password123"
    }


@pytest.mark.asyncio
async def test_list_users(client: TestClient):
    response = client.get(base_url)
    data = response.json()
    assert response.status_code == 200
    assert data is not None


@pytest.mark.asyncio
async def test_register(client: TestClient, user_data):
    response = client.post(base_url, json=user_data)
    data = response.json()
    assert response.status_code == 201
    assert data["detail"] == "username was created"


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
async def test_register(
    client: TestClient, username, email, password
):
    user_data = {
        "username": username,
        "email": email,
        "password": password
    }
    response = client.post(base_url, json=user_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login(client: TestClient, user_data):
    client.post(base_url, json=user_data)
    response = client.post(base_url + "/login", json=user_data)
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
    client: TestClient, user_data, username, password
):
    test_data = {"username": username, "password": password}
    client.post(base_url, json=user_data)
    response = client.post(base_url + "/login", json=test_data)
    data = response.json()
    assert response.status_code == 404
    assert data["detail"] == "Invalid login credentials"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, password", [("username", None), (None, "")]
)
async def test_login_no_credentials(
    client: TestClient, user_data, username, password
):
    test_data = {"username": username, "password": password}
    client.post(base_url, json=user_data)
    response = client.post(base_url + "/login", json=test_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_refresh(client: TestClient, user_data):
    client.post(base_url, json=user_data)
    client.post(base_url + "/login", json=user_data)
    response = client.get(base_url + "/refresh")
    data = response.json()
    assert response.status_code == 200
    assert data["access_token"] is not None


@pytest.mark.asyncio
async def test_my_data(client: TestClient, user_data):
    client.post(base_url, json=user_data)
    login_response = client.post(base_url + "/login", json=user_data)
    token = login_response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"

    response = client.get(base_url + "/me")
    data = response.json()
    assert response.status_code == 200
    assert data["id"] == 1
    assert data["username"] == "username"
    assert data["email"] == "email@email.com"
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


@pytest.mark.asyncio
async def test_my_data_with_no_header(client: TestClient):
    response = client.get(base_url + "/me")
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_user(client: TestClient, user_data):
    client.post(base_url, json=user_data)
    login_response = client.post(base_url + "/login", json=user_data)
    token = login_response.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"

    response = client.delete(base_url)
    data = response.json()
    assert response.status_code == 200
    assert data["detail"] == "username was deleted"
    

@pytest.mark.asyncio
async def test_delete_user_with_no_header(client: TestClient):
    response = client.delete(base_url)
    assert response.status_code == 403
