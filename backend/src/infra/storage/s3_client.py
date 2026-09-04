from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import BinaryIO

import aioboto3
from botocore.exceptions import ClientError, EndpointConnectionError
from src.core.config import settings
from src.core.exceptions import (
    ObjectNotFoundError,
    StorageConnectionError,
    StorageError,
    StorageUploadError,
)
from src.infra.storage.base import StorageBackend
from types_aiobotocore_s3.client import S3Client as AioS3Client


class S3Client(StorageBackend):
    def __init__(self) -> None:
        self.session = aioboto3.Session()
        self.bucket = settings.S3_BUCKET_NAME

    @asynccontextmanager
    async def _client(self) -> AsyncGenerator[AioS3Client]:
        async with self.session.client(
            "s3",
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_KEY,
            region_name=settings.AWS_REGION,
        ) as s3:
            yield s3

    async def put_object(self, key: str, file_obj: BinaryIO) -> None:
        try:
            async with self._client() as s3:
                await s3.put_object(Bucket=self.bucket, Key=key, Body=file_obj)
        except EndpointConnectionError as e:
            raise StorageConnectionError(f"Failed to connect to S3: {e}")
        except ClientError as e:
            raise StorageUploadError(f"Failed to upload object to S3: {e}")

    async def get_object(self, key: str) -> bytes:
        try:
            async with self._client() as s3:
                response = await s3.get_object(Bucket=self.bucket, Key=key)
                return await response["Body"].read()
        except EndpointConnectionError as e:
            raise StorageConnectionError(f"Failed to connect to S3: {e}")
        except ClientError as e:
            error_code = e.response.get("Error", {}).get("Code", "")
            if error_code == "NoSuchKey":
                raise ObjectNotFoundError(key) from e
            raise StorageError(f"Failed to retrieve object from S3: {e}") from e

    async def delete_object(self, key: str) -> None:
        try:
            async with self._client() as s3:
                await s3.delete_object(Bucket=self.bucket, Key=key)
        except EndpointConnectionError as e:
            raise StorageConnectionError(f"Failed to connect to S3: {e}")
        except ClientError as e:
            raise StorageError(f"Failed to delete object from S3: {e}") from e

    async def list_objects(self, prefix: str = "") -> list[str]:
        try:
            async with self._client() as s3:
                response = await s3.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
                contents = response.get("Contents", [])

                return [obj["Key"] for obj in contents if "Key" in obj]
        except EndpointConnectionError as e:
            raise StorageConnectionError(f"Failed to connect to S3: {e}")
        except ClientError as e:
            raise StorageError(f"Failed to list objects in S3: {e}") from e
