import pytest
from sqlalchemy.exc import SQLAlchemyError


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "name, description, image, correlation, slope, y_intercept, valid",
    [
        ("name", "description", "image", 0.9, 1.2, 0.2, True),  # Valid
        (None, "description", "image", 0.9, 1.2, 0.2, False),  # no name
        ("name", None, "image", 0.9, 1.2, 0.2, False),  # no description
        ("name", "description", None, 0.9, 1.2, 0.2, True),  # no image
        ("name", "description", "image", None, 1.2, 0.2, False),  # no corr
        ("name", "description", "image", 0.9, None, 0.2, False),  # no slope
        ("name", "description", "image", 0.9, 1.2, None, False),  # no intercept
        ("name", "description", "image", "string", 1.2, 0.2, False),  # wrong data types
        ("name", "description", "image", 0.9, "string", 0.2, False),  # wrong data types
        ("name", "description", "image", 0.9, 1.2, "string", False),  # wrong data types
    ]
)
async def test_standard_creation(
    standard_factory, name, description, image,
    correlation, slope, y_intercept, valid
):
    if valid:
        std = await standard_factory(
            name=name, description=description, image=image,
            correlation=correlation, slope=slope,
            y_intercept=y_intercept
        )
        assert std.name == name
        assert std.description == description
        assert std.image == image
        assert std.correlation == correlation
        assert std.slope == slope
        assert std.y_intercept == y_intercept
        assert std.id is not None
        assert std.user_id is not None
        assert std.created_at is not None
        assert std.updated_at is not None
        assert repr(std) == f"<Standard {std.name} | a={std.y_intercept} b={std.slope}>"
    else:
        with pytest.raises(SQLAlchemyError):
            await standard_factory(
                name=name, description=description, image=image,
                correlation=correlation, slope=slope,
                y_intercept=y_intercept
            )


@pytest.mark.asyncio
async def test_standard_creation_without_user(
    standard_factory
):
    with pytest.raises(SQLAlchemyError):
        await standard_factory(
            name="name", description="description", image="image",
            correlation=0.9, slope=2,
            y_intercept=2.5, user_id=None
        )
