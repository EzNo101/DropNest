from abc import ABC, abstractmethod
from typing import BinaryIO


class StorageBackend(ABC):
    @abstractmethod
    async def put_object(self, key: str, file_obj: BinaryIO) -> None:
        """Store an object in the storage backend."""

    @abstractmethod
    async def get_object(self, key: str) -> bytes:
        """Retrieve an object from the storage backend."""

    @abstractmethod
    async def delete_object(self, key: str) -> None:
        """Delete an object from the storage backend."""

    @abstractmethod
    async def list_objects(self, prefix: str = "") -> list[str]:
        """List objects in the storage backend with an optional prefix."""
