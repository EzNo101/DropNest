import mimetypes

from fastapi import APIRouter, HTTPException, Response, UploadFile
from src.core.dependencies import StorageBackendDependency

router = APIRouter(prefix="/files", tags=["files"])


@router.get("/", status_code=200, response_model=list[str])
async def list_files(storage: StorageBackendDependency, prefix: str = ""):
    return await storage.list_objects(prefix)


@router.post("/upload", response_model=dict[str, str], status_code=200)
async def upload_file(file: UploadFile, storage: StorageBackendDependency):
    if file.filename is None:
        raise HTTPException(status_code=400, detail="No file provided")
    await storage.put_object(file.filename, file.file)
    return {"filename": file.filename}


@router.get("/{key:path}", status_code=200)
async def download_file(key: str, storage: StorageBackendDependency) -> Response:
    content = await storage.get_object(key)
    media_type, _ = mimetypes.guess_type(key)
    return Response(
        content=content,
        media_type=media_type or "application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={key.split('/')[-1]}"},
    )


@router.delete("/{key:path}", response_model=None, status_code=204)
async def delete_file(key: str, storage: StorageBackendDependency):
    await storage.delete_object(key)
