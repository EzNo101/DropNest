import mimetypes

from fastapi import APIRouter, HTTPException, Response, UploadFile

from core.dependecies import StorageBackendDependency

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload", response_model=dict[str, str], status_code=200)
async def upload_file(file: UploadFile, storage: StorageBackendDependency):
    if file.filename is None:
        raise HTTPException(status_code=400, detail="No file provided")
    await storage.put_object(file.filename, file.file)
    return {"filename": file.filename}


@router.get("/{key:path}", status_code=200)
async def download_file(key: str, storage: StorageBackendDependency):
    content = await storage.get_object(key)
    media_type, _ = mimetypes.guess_type(key)
    return Response(
        content=content,
        media_type=media_type or "application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={key.split('/')[-1]}"},
    )


# TODO: Implement delete_file and list_files endpoints
