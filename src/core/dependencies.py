from __future__ import annotations

from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from src.infra.storage.base import StorageBackend
from src.infra.storage.s3_client import S3Client


@lru_cache
def get_storage_backend() -> StorageBackend:
    return S3Client()


StorageBackendDependency = Annotated[StorageBackend, Depends(get_storage_backend)]
