from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infra.storage.s3_client import S3Client


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    storage = S3Client()
    try:
        await storage.list_objects()  # Test S3 connection
    except Exception as e:  # noqa: BLE001
        raise RuntimeError(f"Failed to connect to S3: {e}")
    yield
    # Perform any shutdown tasks here
