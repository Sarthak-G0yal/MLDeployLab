# app/main.py
from fastapi import FastAPI
from routers import rice_router, animal_router
from core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
)

app.include_router(rice_router.router, prefix="/api/classify", tags=["rice"])
app.include_router(animal_router.router, prefix="/api/classify", tags=["animal"])


@app.get("/")
async def root():
    return {
        "project": "MLDeployLab",
        "description": "End-to-end ML deployment workflow using FastAPI, Docker, and Streamlit.",
        "backend": "FastAPI application for model inference",
        "frontend": "Streamlit interface for testing and feedback",
        "models": ["Rice Type Classifier", "Animal Image Classifier"],
        "status": "Running",
        "message": "The MD BACKEND",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
