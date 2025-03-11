from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Response,
    Request
)
from sqlalchemy.exc import SQLAlchemyError

from .users_dao import UserDao
from .shcemas import UserData, UserLoginData, UserResponse, Token
from .utils import hash_password, verify_password
from .auth import (
    create_token,
    validate_refresh_token,
    user_dependency,
    CREDENTIAL_EXEPTION
)

from typing import Annotated, List


router = APIRouter(prefix="/users", tags=["Users and Auth"])


db_dependency = Annotated[UserDao, Depends(UserDao)]


@router.get("/")
async def get_users(db: db_dependency) -> List[UserResponse]:
    return await db.list_all_users()


@router.post("/register", status_code=201)
async def register_user(userdata: UserData, db: db_dependency) -> dict:
    try:
        userdata = userdata.model_dump()
        userdata["password"] = hash_password(userdata["password"])
        username = await db.register_user(userdata)
        return {"detail": f"{username} was created"}
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="username or email already in use"
        )


@router.post("/login")
async def login_user(
    userdata: UserLoginData,
    db: db_dependency,
    response: Response
) -> Token:
    user = await db.get_user_by_username(userdata.username)

    if not user or not verify_password(user.password, userdata.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid login credentials"
        )

    token_content = {"sub": user.username}

    access_token = create_token(token_content, type="access")
    refresh_token = create_token(token_content, type="refresh")

    response.set_cookie("refresh_token", refresh_token)

    return Token(access_token=access_token, token_type="Bearer")


@router.get("/refresh")
async def refresh(
    request: Request, db: db_dependency
) -> Token:
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise CREDENTIAL_EXEPTION

    username = validate_refresh_token(refresh_token)

    user = await db.get_user_by_username(username)

    if not user:
        raise CREDENTIAL_EXEPTION

    token_content = {"sub": username}
    access_token = create_token(token_content, type="access")
    return Token(access_token=access_token, token_type="Bearer")


@router.post("/logout")
async def logout(request: Request, response: Response) -> dict:
    response.delete_cookie("refresh_token")
    return {"detail": "Loged out"}


@router.get("/me")
async def get_current_user(user: user_dependency) -> UserResponse:
    return user


@router.delete("/")
async def delete_user(user: user_dependency, db: db_dependency) -> dict:
    username = await db.delete_user(user.id)

    if not username:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user"
        )

    return {"detail": f"{username} was deleted"}
