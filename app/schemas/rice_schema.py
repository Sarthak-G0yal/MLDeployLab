from pydantic import BaseModel


class RiceFeatures(BaseModel):
    Area: float
    MajorAxisLength: float
    MinorAxisLength: float
    Eccentricity: float
    ConvexArea: float
    EquivDiameter: float
    Extent: float
    Perimeter: float
    Roundness: float
    AspectRatio: float
