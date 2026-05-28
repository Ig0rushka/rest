from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError

from core.security import parse_token

_bearer = HTTPBearer(auto_error=False)


def maybe_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer),
) -> Optional[dict]:
    if credentials is None:
        return None
    try:
        payload = parse_token(credentials.credentials)
        if payload.get("kind") != "access":
            return None
        return {"id": payload["uid"], "username": payload["username"]}
    except InvalidTokenError:
        return None


def current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer),
) -> dict:
    if credentials is None:
        raise HTTPException(status_code=401, detail="Authorization required")
    try:
        payload = parse_token(credentials.credentials)
        if payload.get("kind") != "access":
            raise HTTPException(status_code=401, detail="Invalid token type")
        return {"id": payload["uid"], "username": payload["username"]}
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
