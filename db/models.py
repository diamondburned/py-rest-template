from typing import Optional
from sqlmodel import Field  # type: ignore
from sqlmodel import SQLModel
from datetime import datetime
from utils.id import generate_id


class User(SQLModel, table=True):
    id: int = Field(default_factory=generate_id, primary_key=True)
    email: str = Field(unique=True)
    passhash: str
    avatar_hash: Optional[str] = Field(default=None, foreign_key="asset.hash")
    display_name: str | None = None


class Session(SQLModel, table=True):
    token: str = Field(primary_key=True)
    user_id: Optional[int] = Field(foreign_key="user.id")
    expires_at: datetime = Field(default_factory=datetime.utcnow)


class Asset(SQLModel, table=True):
    """
    An asset is any arbitrary binary data that can be stored in the database.
    It is identified by the base64-encoded SHA-256 hash of the data.
    Content types are supplied by the server.
    """

    hash: str = Field(primary_key=True)
    data: bytes
    created_at: datetime = Field(default_factory=datetime.utcnow)
    content_type: str
    alt: str | None = Field(default=None)
