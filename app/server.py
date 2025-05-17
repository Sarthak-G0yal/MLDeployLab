import numpy as np
import torch
from fastapi import FastAPI
from pydantic import BaseModel

device = "cpu"
print(f"Using {device} for running the model.")

model = torch.jit.load("app/model_scripted.pt",map_location="cpu")

type_of_rice = ["Gonen", "Jasmine"]

class RiceData(BaseModel):
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

features = [
    "Area",
    "MajorAxisLength",
    "MinorAxisLength",
    "Eccentricity",
    "ConvexArea",
    "EquivDiameter",
    "Extent",
    "Perimeter",
    "Roundness",
    "AspectRation",
]


app = FastAPI()


@app.get("/")
def reed_root():
    return {"message": "Rice Model API"}


@app.post("/predict")
def predict(data: RiceData):
    input_list = []

    for feature in features:
        value = getattr(data, feature)
        normalized = value / max_dict[feature]
        input_list.append(normalized)

    input_tensor = torch.tensor(input_list, dtype=torch.float32).to(device)
    pred = model(input_tensor)

    return {"prediction": type_of_rice[round(pred.item())]}


'''
{
  "Area": 2872,
  "MajorAxisLength": 74.69188071,
  "MinorAxisLength": 51.40045446,
  "Eccentricity": 0.7255527468,
  "ConvexArea": 3015,
  "EquivDiameter": 60.47101762,
  "Extent": 0.7130089374,
  "Perimeter": 208.317,
  "Roundness": 0.8316582009,
  "AspectRation": 1.453136582
}

'''