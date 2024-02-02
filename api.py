from fastapi import Depends, APIRouter, HTTPException, Header
from sqlmodel import select
from pydantic import BaseModel
from sessions import (
    authorize,
    hash_password,
    verify_password,
    generate_token,
    new_session,
)
from db.models import *
from db import Database, use_db

router = APIRouter(
    prefix="/api",
    tags=["api"],
)


@router.get("/users/me")
async def get_self(user: User = Depends(authorize)) -> User:
    """
    This function returns the currently authenticated user.
    """
    return user


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(
    req: LoginRequest,
    db: Database = Depends(use_db),
) -> Session:
    """
    This function logs in a user and returns a session token.
    """
    user = (await db.exec(select(User).where(User.username == req.username))).first()
    if user is None or not verify_password(req.password, user.passhash):
        raise HTTPException(status_code=401, detail="Unauthorized")

    session = await new_session(db, user)
    return session


class RegisterRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
async def register(
    req: RegisterRequest,
    db: Database = Depends(use_db),
) -> Session:
    """
    This function registers a new user and returns a session token.
    """
    user = User(
        username=req.username,
        passhash=hash_password(req.password),
    )
    db.add(user)

    await db.commit()

    session = await new_session(db, user)
    return session
