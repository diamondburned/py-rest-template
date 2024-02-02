from fastapi import Depends, APIRouter, HTTPException
from sqlmodel import select
from pydantic import BaseModel
from sessions import authorize, hash_password, verify_password, new_session
from db.models import *
from db import Database
import db

router = APIRouter(
    prefix="/api",
    tags=["api"],
)


class UserResponse(BaseModel):
    username: str
    display_name: str | None


@router.get("/users/me")
async def get_self(
    username: str = Depends(authorize),
    db: Database = Depends(db.use),
) -> UserResponse:
    """
    This function returns the currently authenticated user.
    """
    user = (await db.exec(select(User).where(User.username == username))).one()
    return UserResponse(**user.model_dump())


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(
    req: LoginRequest,
    db: Database = Depends(db.use),
) -> Session:
    """
    This function logs in a user and returns a session token.
    """
    user = (await db.exec(select(User).where(User.username == req.username))).first()
    if user is None or not verify_password(req.password, user.passhash):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return new_session(db, user.username)


class RegisterRequest(BaseModel):
    username: str
    password: str


@router.post("/register")
async def register(
    req: RegisterRequest,
    db: Database = Depends(db.use),
) -> Session:
    """
    This function registers a new user and returns a session token.
    """
    user = User(
        username=req.username,
        passhash=hash_password(req.password),
    )
    db.add(user)
    return new_session(db, user.username)
