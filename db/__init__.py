import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.ext.asyncio
import sqlalchemy.ext.asyncio.session
import sqlmodel
import sqlmodel.ext.asyncio.session
from typing import AsyncGenerator


SQLITE_PATH = "database.db"
SQLITE_URL = f"sqlite+aiosqlite:///{SQLITE_PATH}"


Database = sqlmodel.ext.asyncio.session.AsyncSession


@sqlalchemy.event.listens_for(sqlalchemy.engine.Engine, "connect")
def set_sqlite_pragma(conn, _):
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=wal2")
    cursor.close()


_engine: sqlalchemy.ext.asyncio.AsyncEngine | None = None


async def init_db() -> None:
    """
    This function initializes the database engine.
    """
    global _engine
    _engine = sqlalchemy.ext.asyncio.create_async_engine(
        SQLITE_URL,
        echo=True,
        future=True,
        connect_args={"check_same_thread": False},
    )

    async with _engine.begin() as conn:
        await conn.run_sync(sqlmodel.SQLModel.metadata.create_all)


# For async info on SQLModel, see
# https://github.com/tiangolo/sqlmodel/pull/58.
async def use_db() -> AsyncGenerator[Database, None]:
    """
    This function is a context manager that yields a database session.
    Use this in FastAPI route functions to access the database.
    """
    if _engine is None:
        raise Exception("must call db.init() before using the database")

    async with sqlmodel.ext.asyncio.session.AsyncSession(_engine) as session:
        yield session
