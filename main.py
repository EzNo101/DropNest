from fastapi import FastAPI

from src.core.lifespan import lifespan

app = FastAPI(title="DropNest", lifespan=lifespan)
