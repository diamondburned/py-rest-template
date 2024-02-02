from fastapi import HTTPException
import sqlalchemy
import sqlalchemy.engine
import sqlalchemy.exc
import sqlalchemy.ext.asyncio
import sqlalchemy.ext.asyncio.session
import sqlmodel
import sqlmodel.ext.asyncio.session
from typing import AsyncGenerator


Database = sqlmodel.ext.asyncio.session.AsyncSession


sqlitePath = "database.db"


def sqlite_url() -> str:
    return f"sqlite+aiosqlite:///{sqlitePath}"


def set_sqlite_path(path: str) -> None:
    global sqlitePath
    sqlitePath = path


_engine: sqlalchemy.ext.asyncio.AsyncEngine | None = None


async def init_db() -> None:
    """
    This function initializes the database engine.
    """
    global _engine
    _engine = sqlalchemy.ext.asyncio.create_async_engine(sqlite_url(), echo=True)

    async with _engine.begin() as conn:
        await conn.run_sync(sqlmodel.SQLModel.metadata.create_all)


@sqlalchemy.event.listens_for(sqlalchemy.engine.Engine, "connect")
def set_sqlite_pragma(conn, _):
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=wal2")
    cursor.close()


# For async info on SQLModel, see
# https://github.com/tiangolo/sqlmodel/pull/58.
async def use() -> AsyncGenerator[Database, None]:
    """
    This function is a context manager that yields a database session.
    Use this in FastAPI route functions to access the database.
    """
    if _engine is None:
        raise Exception("must call db.init() before using the database")

    async with sqlmodel.ext.asyncio.session.AsyncSession(_engine) as session:
        try:
            yield session
            await session.commit()
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(status_code=409, detail="Conflict")
        except:
            await session.rollback()
            raise
