# app/main.py
from fastapi import FastAPI
from app.routers import rice_router

app = FastAPI(
    title="Rice Classifier Service",
)

app.include_router(rice_router.router, prefix="/api/rice", tags=["rice"])
