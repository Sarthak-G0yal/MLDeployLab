import torch
from pydantic import BaseModel
import numpy as np


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
    AspectRation: float


max_dict = {
    "Area": np.float32(10210),
    "MajorAxisLength": np.float32(183.2114344),
    "MinorAxisLength": np.float32(82.55076212),
    "Eccentricity": np.float32(0.9667736672),
    "ConvexArea": np.float32(11008),
    "EquivDiameter": np.float32(114.0165591),
    "Extent": np.float32(0.8865730584),
    "Perimeter": np.float32(508.511),
    "Roundness": np.float32(0.9047483132),
    "AspectRation": np.float32(3.911844673),
}

PATH_TO_MODEL = "app/resources/models/rice_classification_model.pt"

rice_classifier = torch.jit.load(PATH_TO_MODEL, map_location="cpu")


type_of_rice = ["Gonen", "Jasmine"]


def predict(data: RiceFeatures):
    input_list = []

    for feature in RiceFeatures.__fields__.keys():
        value = getattr(data, feature)
        normalized = value / max_dict[feature]
        input_list.append(normalized)

    input_tensor = torch.tensor(input_list, dtype=torch.float32)
    pred = rice_classifier(input_tensor)

    return {"prediction": type_of_rice[round(pred.item())]}
