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


@router.get("/animal/schema", status_code=status.HTTP_200_OK)
async def get_animal_schema() -> dict:
    if AnimalFeatures.model_fields:
        return AnimalFeatures.model_json_schema()
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Schema not found"
        )


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
    features = feedback_data.get("features")
    correct_class = feedback_data.get("correct_class")
    features_key = ",".join([f"{k}" for k in features.keys()])
    features_value = ",".join([f"{v}" for v in features.values()])
    file_path = f"{PATH_TO_FEEDBACK_FOLDER}/animal_feedback.csv"
    if not os.path.exists(file_path):
        os.makedirs(PATH_TO_FEEDBACK_FOLDER, exist_ok=True)
        with open(file_path, "a") as f:
            f.write(f"{features_key},class\n")
    with open(file_path, "a") as f:
        f.write(f"{features_value},{correct_class}\n")

    return {"success": True}
