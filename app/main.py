# app/main.py
from fastapi import FastAPI
from app.routers import rice_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
)

app.include_router(rice_router.router, prefix="/api/classify", tags=["rice"])
