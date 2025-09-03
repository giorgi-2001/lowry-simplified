import pytest
from sqlalchemy.exc import SQLAlchemyError


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name, description, user_id", [
        ("project", "some description", 1),
        ("project", "some description", 5),
        ("project", "some description", "name"),  # this is cringe but whatever
        ("project", "some description", 5.25),
    ]
)
async def test_project_creation(
    project_factory, name, description, user_id
):
    project = await project_factory(
        name=name, description=description, user_id=user_id
    )
    assert project.name == name
    assert project.description == description
    assert project.user_id == user_id
    assert project.id is not None
    assert project.created_at is not None
    assert project.updated_at is not None
    assert repr(project) == (
        f"Project(Id={project.id} Name={project.name}) "
        f"Description={project.description}"
    )
    assert str(project) == f"<Project {project.name}>"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name, description, user_id", [
        (None, "some description", 1),
        ("project", None, 5),
        ("project", "some description", None),
    ]
)
async def test_project_creation_invalid_data(
    project_factory, name, description, user_id
):
    with pytest.raises(SQLAlchemyError):
        await project_factory(
            name=name, description=description, user_id=user_id
        )
