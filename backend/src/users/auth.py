from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException, status, Security
import jwt
import dotenv

from .users_dao import UserDao
from .models import User
from ..redis_client import RedisClient

from datetime import datetime, timedelta, timezone
from typing import Annotated
import os
import uuid


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


def create_access_token(data: dict):
    to_encode = data.copy()

    expire_access_token = datetime.now(timezone.utc) + timedelta(minutes=10)

    to_encode.update({"expire": str(expire_access_token)})

    access_token = jwt.encode(
        payload=to_encode,
        key=ACCESS_TOKEN_SECRET_KEY,
        algorithm=ALGORITHM,
    )

    return access_token


def create_refresh_token(username: str):
    session_id = str(uuid.uuid4())

    to_encode = {
        "session_id": session_id,
        "username": username
    }

    refresh_token = jwt.encode(
        payload=to_encode,
        key=REFRESH_TOKEN_SECRET_KEY,
        algorithm=ALGORITHM,
    )

    RedisClient.set_item_to_cache(
        key=session_id, value=username, exp=timedelta(days=5)
    )

    return refresh_token


def validate_refresh_token(token: str):
    try:
        payload = jwt.decode(
            jwt=token,
            key=REFRESH_TOKEN_SECRET_KEY,
            algorithms=[ALGORITHM]
        )
    except jwt.InvalidTokenError:
        raise CREDENTIAL_EXEPTION

    session_id = payload.get("session_id")
    username = payload.get("username")

    if not session_id or not username:
        raise CREDENTIAL_EXEPTION

    stored_username = RedisClient.get_item_from_cachce(key=session_id)

    if not stored_username or stored_username != username:
        raise CREDENTIAL_EXEPTION

    return username, session_id


def close_session(session_id):
    RedisClient.remove_item(key=session_id)


async def get_authenticated_user(db: db_dependecny, credentials: auth_dependency):
    token = credentials.credentials

    try:
        payload = jwt.decode(
            jwt=token,
            key=ACCESS_TOKEN_SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        expiration_date = datetime.fromisoformat(payload["expire"])
        is_expired = expiration_date < datetime.now(timezone.utc)

        if is_expired:
            raise CREDENTIAL_EXEPTION

        username = payload["sub"]
    except (KeyError, jwt.InvalidTokenError):
        raise CREDENTIAL_EXEPTION
    
    user = await db.get_user_by_username(username)
    print(user)

    if not user:
        raise CREDENTIAL_EXEPTION
    
    return user


user_dependency = Annotated[User, Depends(get_authenticated_user)]