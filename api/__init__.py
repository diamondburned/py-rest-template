from fastapi import APIRouter
from importlib import import_module

root = APIRouter(prefix="/api")
for module in ["assets", "users", "sessions"]:
    router = import_module(f".{module}", __package__)
    root.include_router(router.router)
