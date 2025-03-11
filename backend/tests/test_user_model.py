import pytest
from sqlalchemy.exc import SQLAlchemyError


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, email, password, valid", [
        ("TestUser", "test@test.com", "testuser123", True),
        ("", "test@test.com", "testuser123", False),
        ("TestUser", "", "testuser123", False),
        ("TestUser", "test@test.com", "", False),
        ("TestUser", "test@test.com", None, False),
        ("TestUser", None, "", False),
        (None, "test@test.com", "", False),
        ("TestUser", "test@test.com", "test", False),
    ]
)
async def test_user_creation(
    user_factory, username, email, password, valid
):
    if valid:
        user = await user_factory(username, email, password)
        assert user.id == 1
        assert user.username == username
        assert user.email == email
        assert user.password == password
        assert user.created_at is not None
        assert user.updated_at is not None
    else:
        with pytest.raises(SQLAlchemyError):
            await user_factory(username, email, password)


@pytest.mark.asyncio
async def test_dublicate_usernames(user_factory):
    await user_factory("TestUser", "test@test.com", "testuser123")

    with pytest.raises(SQLAlchemyError):
        await user_factory("TestUser", "test24@test.com", "testuser123")


@pytest.mark.asyncio
async def test_dublicate_emails(user_factory):
    await user_factory("TestUser", "test@test.com", "testuser123")

    with pytest.raises(SQLAlchemyError):
        await user_factory("TestUser123", "test@test.com", "testuser123")


@pytest.mark.asyncio
async def test_repr_method(user_factory):
    user = await user_factory("TestUser", "test@test.com", "testuser123")
    assert repr(user) == "<User id=1 TestUser>"


@pytest.mark.asyncio
async def test_to_dict_method(user_factory):
    user = await user_factory("TestUser", "test@test.com", "testuser123")
    user_data = user.to_dict()
    assert user_data["username"] == "TestUser"
    assert user_data["email"] == "test@test.com"
    assert user_data["created_at"] is not None
    assert user_data["updated_at"] is not None
