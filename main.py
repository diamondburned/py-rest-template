#!/usr/bin/env python3

from contextlib import asynccontextmanager
from fastapi import FastAPI
import db
import api
import uvicorn
import argparse


@asynccontextmanager
async def with_init_db(_: FastAPI):
    await db.init_db()
    yield


app = FastAPI(lifespan=with_init_db)
app.include_router(api.router)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="py-rest-template")
    parser.add_argument("-H", "--host", default="127.0.0.1", help="The host to bind to")
    parser.add_argument("-p", "--port", default=5765, help="The port to bind to")
    parser.add_argument("--database", default="database.db", help="Path to database")

    args = parser.parse_args()
    db.set_sqlite_path(args.database)

    uvicorn.run(app, host=args.host, port=args.port)
