from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import BinaryIO

import aioboto3
from types_aiobotocore_s3.client import S3Client as AioS3Client

from src.core.config import settings
from src.infra.storage.base import StorageBackend


class S3Client(StorageBackend):
    def __init__(self) -> None:
        self.session = aioboto3.Session()
        self.bucket = settings.S3_BUCKET_NAME

    @asynccontextmanager
    async def _client(self) -> AsyncGenerator[AioS3Client]:
        async with self.session.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION,
            endpoint_url=settings.S3_ENDPOINT_URL,
        ) as s3:
            yield s3

    async def put_object(self, key: str, file_obj: BinaryIO) -> None:
        async with self._client() as s3:
            await s3.put_object(Bucket=self.bucket, Key=key, Body=file_obj)

    async def get_object(self, key: str) -> bytes:
        async with self._client() as s3:
            response = await s3.get_object(Bucket=self.bucket, Key=key)
            return await response["Body"].read()

    async def delete_object(self, key: str) -> None:
        async with self._client() as s3:
            await s3.delete_object(Bucket=self.bucket, Key=key)

    async def list_object(self, prefix: str = "") -> list[str]:
        async with self._client() as s3:
            response = await s3.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
            contents = response.get("Contents", [])

            return [obj["Key"] for obj in contents if "Key" in obj]
