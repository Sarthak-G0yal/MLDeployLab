from pydantic import BaseModel, Field


class RiceFeatures(BaseModel):
    Area: float = Field(..., gt=0)
    MajorAxisLength: float = Field(..., gt=0)
    MinorAxisLength: float = Field(..., gt=0)
    Eccentricity: float = Field(..., gt=0)
    ConvexArea: float = Field(..., gt=0)
    EquivDiameter: float = Field(..., gt=0)
    Extent: float = Field(..., gt=0)
    Perimeter: float = Field(..., gt=0)
    Roundness: float = Field(..., gt=0)
    AspectRatio: float = Field(..., gt=0)
