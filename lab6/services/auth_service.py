import uuid
from typing import Optional

from jwt.exceptions import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import (
    hash_pw, verify_pw,
    new_access, new_refresh, parse_token,
)
from repository import user_repository
from schemas.user import Credentials

_valid_refresh: set[str] = set()


async def create_account(db: AsyncSession, data: Credentials) -> Optional[object]:
    if await user_repository.get_by_username(db, data.username):
        return None
    return await user_repository.create(db, {
        "id": str(uuid.uuid4()),
        "username": data.username,
        "hashed_password": hash_pw(data.password),
        "is_active": True,
    })


async def authenticate(db: AsyncSession, username: str, password: str) -> Optional[dict]:
    user = await user_repository.get_by_username(db, username)
    if not user or not verify_pw(password, user.hashed_password) or not user.is_active:
        return None
    access = new_access(user.id, user.username)
    refresh = new_refresh(user.id)
    _valid_refresh.add(refresh)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}


async def rotate(db: AsyncSession, token: str) -> Optional[dict]:
    if token not in _valid_refresh:
        return None
    try:
        payload = parse_token(token)
        if payload.get("kind") != "refresh":
            return None
        user_id = payload["uid"]
    except InvalidTokenError:
        _valid_refresh.discard(token)
        return None

    user = await user_repository.get_by_id(db, user_id)
    if not user or not user.is_active:
        _valid_refresh.discard(token)
        return None

    _valid_refresh.discard(token)
    fresh_access = new_access(user.id, user.username)
    fresh_refresh = new_refresh(user.id)
    _valid_refresh.add(fresh_refresh)
    return {"access_token": fresh_access, "refresh_token": fresh_refresh, "token_type": "bearer"}


def sign_out(token: str) -> None:
    _valid_refresh.discard(token)


def clear_tokens() -> None:
    _valid_refresh.clear()
