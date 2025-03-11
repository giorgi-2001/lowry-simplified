from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException, status, Security
import jwt
import dotenv

from .users_dao import UserDao
from .models import User

from datetime import datetime, timedelta, timezone
from typing import Annotated
import os


dotenv.load_dotenv()


ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_SECRET_KEY = os.environ.get("ACCESS_TOKEN_SECRET_KEY")
REFRESH_TOKEN_SECRET_KEY = os.environ.get("REFRESH_TOKEN_SECRET_KEY")

CREDENTIAL_EXEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


security = HTTPBearer(scheme_name="Bearer Token")

auth_dependency = Annotated[HTTPAuthorizationCredentials, Security(security)]
db_dependecny = Annotated[UserDao, Depends(UserDao)]


def create_token(data: dict, type: str):
    to_encode = data.copy()

    if type == "access":
        expire = datetime.now(timezone.utc) + timedelta(minutes=10)
        secret_key = ACCESS_TOKEN_SECRET_KEY
    elif type == "refresh":
        expire = datetime.now(timezone.utc) + timedelta(days=5)
        secret_key = REFRESH_TOKEN_SECRET_KEY

    to_encode.update({"expire": expire.isoformat()})

    token = jwt.encode(
        payload=to_encode,
        key=secret_key,
        algorithm=ALGORITHM,
    )

    return token


def validate_refresh_token(token: str):
    try:
        payload = jwt.decode(
            jwt=token,
            key=REFRESH_TOKEN_SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except jwt.InvalidTokenError:
        raise CREDENTIAL_EXEPTION

    username = payload.get("sub")
    expire = payload.get("expire")

    if not username or not expire:
        raise CREDENTIAL_EXEPTION

    exp_date = datetime.fromisoformat(expire)

    if exp_date < datetime.now(timezone.utc):
        raise CREDENTIAL_EXEPTION

    return username


async def get_authenticated_user(db: db_dependecny, credentials: auth_dependency):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            jwt=token,
            key=ACCESS_TOKEN_SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        exp_date = datetime.fromisoformat(payload["expire"])
        is_expired = exp_date < datetime.now(timezone.utc)

        if is_expired:
            raise CREDENTIAL_EXEPTION

        username = payload["sub"]
    except (KeyError, jwt.InvalidTokenError):
        raise CREDENTIAL_EXEPTION

    user = await db.get_user_by_username(username)

    if not user:
        raise CREDENTIAL_EXEPTION

    return user


user_dependency = Annotated[User, Depends(get_authenticated_user)]
