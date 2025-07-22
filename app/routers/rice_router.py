from fastapi import APIRouter, HTTPException, status
from schemas.rice_schema import RiceFeatures, RiceFeedback
from services.rice_service import predict_rice
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

PATH_TO_FEEDBACK_FOLDER = os.getenv("PATH_TO_FEEDBACK_FOLDER") or "./resources/feedback"
os.makedirs(PATH_TO_FEEDBACK_FOLDER, exist_ok=True)


@router.get("/rice/schema", status_code=status.HTTP_200_OK)
async def get_rice_schema() -> dict:
    if RiceFeatures.model_fields:
        return RiceFeatures.model_json_schema()
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Schema not found"
        )


@router.post("/rice", status_code=status.HTTP_200_OK)
async def classify_rice(payload: RiceFeatures):
    """
    Accepts a JSON body matching RiceFeatures, returns:
      {
        "prediction": "...",
        "confidence": 0.xx    # optional, if model returns a probability
      }
    """
    try:
        return predict_rice(payload)
    except ValueError as ve:
        # malformed input, missing feature, or normalization issue
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(ve)
        )
    except FileNotFoundError as fnf:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Model file missing: {fnf}",
        )
    except Exception as e:
        # any other unexpected error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/rice/feedback", status_code=status.HTTP_200_OK)
async def store_rice_feedback(feedback: RiceFeedback) -> dict:
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
