from fastapi import APIRouter

from src.api.v1.files import router as files_router

router = APIRouter(prefix="/v1", tags=["v1"])
router.include_router(files_router)
