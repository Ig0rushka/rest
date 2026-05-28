from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import Credentials, UserView
from schemas.token import LoginRequest, TokenResponse, RefreshRequest
from services import auth_service
from database import get_db
from core.rate_limiter import enforce_limit

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserView, status_code=201)
async def register(data: Credentials, db: AsyncSession = Depends(get_db)):
    user = await auth_service.create_account(db, data)
    if user is None:
        raise HTTPException(status_code=409, detail="Username already taken")
    return user


@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db),
    _rl: None = Depends(enforce_limit),
):
    tokens = await auth_service.authenticate(db, data.username, data.password)
    if tokens is None:
        raise HTTPException(status_code=401, detail="Wrong username or password")
    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh(data: RefreshRequest, db: AsyncSession = Depends(get_db)):
    tokens = await auth_service.rotate(db, data.refresh_token)
    if tokens is None:
        raise HTTPException(status_code=401, detail="Token is invalid or has expired")
    return tokens


@router.post("/logout")
async def logout(data: RefreshRequest):
    auth_service.sign_out(data.refresh_token)
    return {"message": "Logged out"}
