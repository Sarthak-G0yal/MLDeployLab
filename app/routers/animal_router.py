from services.animal_service import predict_animal
from fastapi import APIRouter, HTTPException, status
import aiohttp
import uuid
import shutil
from pathlib import Path

router = APIRouter()


@router.post("/animal", status_code=status.HTTP_200_OK)
async def classify_animal(URL: str):
    temp_dir = Path(".temp")
    temp_dir.mkdir(exist_ok=True)
    unique_filename = temp_dir / f"{uuid.uuid4().hex}.jpg"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(URL) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"Cannot download image from {URL}",
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
