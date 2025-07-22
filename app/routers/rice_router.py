from fastapi import APIRouter, HTTPException, status
from services.feedback_service import store_feedback
from schemas.rice_schema import RiceFeatures, RiceFeedback
from services.rice_service import predict_rice

router = APIRouter()


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
async def rice_feedback(feedback: RiceFeedback) -> dict:
    res = store_feedback(feedback.dict(), "rice")
    if res.get("success"):
        return {"success": True}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to store feedback",
        )
