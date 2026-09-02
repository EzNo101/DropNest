class StorageError(Exception):
    """Base class for storage-related exceptions."""


class ObjectNotFoundError(StorageError):
    """Raised when an object is not found in the storage backend."""

    def __init__(self, key: str) -> None:
        self.key = key
        super().__init__(f"Object not found: {key}")


class StorageConnectionError(StorageError):
    """Raised when there is a connection issue with the storage backend."""


class StorageUploadError(StorageError):
    """Raised when there is an error during file upload to the storage backend."""
