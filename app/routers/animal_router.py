from services.animal_service import predict_animal
from fastapi import APIRouter, HTTPException, status
import aiohttp
import uuid
import shutil
from pathlib import Path
from schemas.animal_schema import AnimalFeatures, AnimalFeedback
from dotenv import load_dotenv
import os

load_dotenv()
router = APIRouter()

PATH_TO_FEEDBACK_FOLDER = os.getenv("PATH_TO_FEEDBACK_FOLDER") or "./resources/feedback"
os.makedirs(PATH_TO_FEEDBACK_FOLDER, exist_ok=True)


@router.post("/animal", status_code=status.HTTP_200_OK)
async def classify_animal(payload: AnimalFeatures) -> dict:
    image_url = str(payload.image_url)
    temp_dir = Path(".temp")
    temp_dir.mkdir(exist_ok=True)
    unique_filename = temp_dir / f"{uuid.uuid4().hex}.jpg"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Cannot download image from {image_url}",
                    )
                with open(unique_filename, "wb") as f:
                    f.write(await response.read())

        return predict_animal(str(unique_filename))

    except FileNotFoundError as fnf:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Model file missing: {fnf}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
    finally:
        try:
            shutil.rmtree(temp_dir)
        except Exception:
            pass


@router.post("/animal/feedback", status_code=status.HTTP_200_OK)
async def store_animal_feedback(feedback: AnimalFeedback) -> dict:
    feedback_data = feedback.dict()
    image_url = feedback_data.get("image_url")
    animal = feedback_data.get("animal_class")

    with open(f"{PATH_TO_FEEDBACK_FOLDER}/animal_feedback.csv", "a") as f:
        f.write(f"{image_url},{animal}\n")

    return {"success": True}


@router.get("/animal/schema", status_code=status.HTTP_200_OK)
async def get_animal_schema() -> dict:
    if AnimalFeatures.model_fields:
        return AnimalFeatures.model_json_schema()
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Schema not found"
        )
