from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime


class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    passhash: str
    avatar_id: int | None = Field(default=None, foreign_key="assets.id")
    display_name: str | None = None


class Assets(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    uploader: str = Field(foreign_key="user.username")
    content_type: str
    content: bytes


class Session(SQLModel, table=True):
    token: str = Field(primary_key=True)
    user: User = Relationship()
    username: str = Field(foreign_key="user.username")
    expires_at: datetime = Field(default_factory=datetime.utcnow)
