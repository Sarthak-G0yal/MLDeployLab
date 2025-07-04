# app/main.py
from fastapi import FastAPI
from routers import rice_router
from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
)

app.include_router(rice_router.router, prefix="/api/classify", tags=["rice"])

@app.get('/')
async def root():
    return {"message": "The MD BACKEND"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)