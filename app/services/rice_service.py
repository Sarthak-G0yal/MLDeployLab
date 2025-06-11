import os
import torch
import numpy as np
from app.schemas.rice_schema import RiceFeatures
from app.core.config import settings
from typing import Dict

# MAX_VALUES dict contains the maximum values for each feature used for normalization.
_MAX_VALUES: Dict[str, np.float32] = {
    "Area": np.float32(10210),
    "MajorAxisLength": np.float32(183.2114344),
    "MinorAxisLength": np.float32(82.55076212),
    "Eccentricity": np.float32(0.9667736672),
    "ConvexArea": np.float32(11008),
    "EquivDiameter": np.float32(114.0165591),
    "Extent": np.float32(0.8865730584),
    "Perimeter": np.float32(508.511),
    "Roundness": np.float32(0.9047483132),
    "AspectRatio": np.float32(3.911844673),
}

# Loads Models for prediction.
_DEFAULT_MODEL_FILENAME = "rice_classification_model.pt"

_model: torch.jit.ScriptModule | None = None


def _load_model() -> torch.jit.ScriptModule:
    """
    Lazily load the TorchScript model from disk (singleton).
    Raises FileNotFoundError if the file does not exist.
    """
    global _model
    if _model is None:
        model_path = os.path.join(settings.MODEL_DIR, _DEFAULT_MODEL_FILENAME)
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Cannot find model at {model_path}")
        _model = torch.jit.load(model_path, map_location="cpu")
        _model.eval()
    return _model


# Labels for RiceTypes.
_TYPE_OF_RICE = ["Gonen", "Jasmine"]


# Prediction function to run inference.
def predict_rice(data: RiceFeatures) -> dict:
    """
    Normalizes the incoming feature set, runs inference using the pre-loaded rice_classifier,
    and returns the predicted rice variety.
    """
    input_list = []

    # Normalize each feature using _MAX_VALUES
    for feature_name in RiceFeatures.model_fields.keys():
        if feature_name not in _MAX_VALUES:
            raise ValueError(f"Unexpected feature: {feature_name}")

        raw_value = getattr(data, feature_name)
        max_val = _MAX_VALUES[feature_name]

        if max_val == 0:
            raise ValueError(f"Max value for {feature_name} is zero—cannot normalize.")

        normalized = raw_value / max_val
        input_list.append(normalized)

    # Convert input to tensor
    input_tensor = torch.tensor(input_list, dtype=torch.float32)

    rice_classifier = _load_model()
    # Predict using the pre-loaded classifier
    with torch.no_grad():
        pred = rice_classifier(input_tensor)
        pred_idx = round(pred.item())

    # Build response
    try:
        predicted_variety = _TYPE_OF_RICE[pred_idx]
    except IndexError:
        predicted_variety = "Unknown"

    return {"prediction": predicted_variety}
