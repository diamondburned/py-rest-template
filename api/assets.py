from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form
from fastapi.responses import StreamingResponse
from sqlmodel import select
from pydantic import BaseModel
from db import Database
from db.models import *
from typing import Optional
from api.sessions import authorize
import io
import db
import base64
import hashlib


router = APIRouter(tags=["assets"])


@router.get(
    "/assets/{asset_hash}",
    responses={
        200: {
            "content": {
                "application/octet-stream": {},
                "application/json": None,
            },
            "description": "Return the bytes of the asset in body",
        }
    },
)
async def get_asset(
    asset_hash: str,
    db: Database = Depends(db.use),
    _: int = Depends(authorize),
) -> StreamingResponse:
    """
    This function returns an asset by hash.
    """

    asset = (await db.exec(select(Asset).where(Asset.hash == asset_hash))).first()
    if asset is None:
        raise HTTPException(status_code=404, detail="Not found")

    stream = io.BytesIO(asset.data)
    return StreamingResponse(stream, media_type=asset.content_type)


class GetAssetMetadataResponse(BaseModel):
    content_type: str
    alt: str | None = None


@router.get("/assets/{asset_hash}/metadata")
async def get_asset_metadata(
    asset_hash: str,
    db: Database = Depends(db.use),
    _: int = Depends(authorize),
) -> GetAssetMetadataResponse:
    """
    This function returns metadata for an asset by hash.
    """

    asset = (await db.exec(select(Asset).where(Asset.hash == asset_hash))).first()
    if asset is None:
        raise HTTPException(status_code=404, detail="Not found")

    return GetAssetMetadataResponse(**asset.model_dump())


class UploadFileResponse(BaseModel):
    hash: str
    content_type: str
    alt: str | None = None


@router.post("/assets")
async def upload_asset(
    file: UploadFile,
    alt: Optional[str] = Form(default=None),
    db: Database = Depends(db.use),
    _: int = Depends(authorize),
) -> UploadFileResponse:
    """
    Uploads an asset and returns its hash.
    """
    UPLOAD_LIMIT = 1024 * 1024 * 5  # 5 MB

    if file.content_type is None:
        raise HTTPException(status_code=400, detail="Content-Type header is required")

    if file.size is None or file.size > UPLOAD_LIMIT:
        raise HTTPException(status_code=400, detail="File is too large")

    data = await file.read()
    hash = hash_bytes(data)
    content_type = file.content_type

    asset = Asset(
        hash=hash,
        data=data,
        content_type=content_type,
        alt=alt if alt else None,
    )
    db.add(asset)

    return UploadFileResponse(**asset.model_dump())


async def assert_asset_hash(db: Database, hash: str):
    asset = (await db.exec(select(Asset.hash).where(Asset.hash == hash))).first()
    if asset is None:
        raise HTTPException(status_code=400, detail="Asset hash does not exist")


def hash_bytes(data: bytes) -> str:
    return base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode("utf-8")
