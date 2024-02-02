from sqlmodel import Relationship, SQLModel, Field
from datetime import datetime


class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    passhash: str
    display_name: str | None = None


class Session(SQLModel, table=True):
    token: str = Field(primary_key=True)
    username: str = Field(foreign_key="user.username")
    expires_at: datetime = Field(default_factory=datetime.utcnow)
