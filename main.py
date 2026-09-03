from fastapi import FastAPI

from src.api import router
from src.core.lifespan import lifespan

app = FastAPI(title="DropNest", lifespan=lifespan)
app.include_router(router)
