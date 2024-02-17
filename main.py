#!/usr/bin/env python3

from contextlib import asynccontextmanager
from os import path
from fastapi import FastAPI
import db
import api
import sys
import uvicorn
import argparse


@asynccontextmanager
async def with_init_db(_: FastAPI):
    await db.init_db()
    yield


app = FastAPI(lifespan=with_init_db)
app.include_router(api.root)


if __name__ == "__main__":
    prog = sys.argv[0]
    prog = path.basename(prog)

    parser = argparse.ArgumentParser(prog=prog, description="Run the server")
    parser.add_argument("-H", "--host", default="127.0.0.1", help="The host to bind to")
    parser.add_argument("-p", "--port", default=5765, help="Port to bind to", type=int)
    parser.add_argument("--database", default="database.db", help="Path to database")
    parser.add_argument(
        "--echo-sql",
        action="store_true",
        help="Print SQL queries to stdout",
    )

    args = parser.parse_args()
    db.set_sqlite_path(args.database)
    db.set_echo(args.echo_sql)

    uvicorn.run(app, host=args.host, port=args.port)
