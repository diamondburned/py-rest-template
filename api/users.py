from fastapi import Depends, APIRouter
from pydantic import BaseModel
from api.assets import assert_asset_hash
from api.sessions import authorize, hash_password
from db.models import *
from db import Database
import db

router = APIRouter(tags=["users"])


class UserResponse(BaseModel):
    id: int
    email: str
    avatar_hash: str | None
    display_name: str | None


@router.get("/users/me")
async def get_self(
    db: Database = Depends(db.use),
    user_id: int = Depends(authorize),
) -> UserResponse:
    """
    This function returns the currently authenticated user.
    """
    user = await db.get_one(User, user_id)
    return UserResponse(**user.model_dump())


class UpdateUserRequest(BaseModel):
    email: Optional[str]
    password: Optional[str]
    avatar_hash: Optional[str] = Field(None, nullable=True)
    display_name: Optional[str] = Field(None, nullable=True)


@router.patch("/users/me")
async def update_self(
    req: UpdateUserRequest,
    db: Database = Depends(db.use),
    user_id: int = Depends(authorize),
) -> UserResponse:
    """
    This function updates the currently authenticated user.
    """
    user = await db.get_one(User, user_id)
    req_dict = req.model_dump(exclude_unset=True)  # for null checking

    if req.email is not None:
        user.email = req.email

    if req.password is not None:
        user.passhash = hash_password(req.password)

    if "avatar_hash" in req_dict:
        if req.avatar_hash is not None:
            await assert_asset_hash(db, req.avatar_hash)
            user.avatar_hash = req.avatar_hash
        else:
            user.avatar_hash = None

    if "display_name" in req_dict:
        if req.display_name is not None:
            user.display_name = req.display_name
        else:
            user.display_name = None

    db.add(user)

    await db.commit()
    await db.refresh(user)

    return UserResponse(**user.model_dump())
