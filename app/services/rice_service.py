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
    Normalizes the incoming feature set, runs inference, and returns a JSON-serializable dict.
    """
    # Validate that all keys in data exist in _MAX_VALUES
    for field_name in data.__fields__.keys():
        if field_name not in _MAX_VALUES:
            raise ValueError(f"Unexpected feature: {field_name}")

    # Build a normalized input vector in the same order as RiceFeatures.__fields__.keys()
    input_list = []
    for feature_name in RiceFeatures.__fields__.keys():
        raw_value = getattr(data, feature_name)
        max_val = _MAX_VALUES[feature_name]
        if max_val == 0:
            raise ValueError(f"Max value for {feature_name} is zero—cannot normalize.")
        normalized = raw_value / max_val
        input_list.append(normalized)

    # Convert to a 1D Tensor of shape (num_features,)
    input_tensor = torch.tensor(input_list, dtype=torch.float32)

    # Inference
    model = _load_model()
    with torch.no_grad():
        # If the model expects (batch_size, num_features), unsqueeze to (1, num_features)
        if input_tensor.ndim == 1:
            input_tensor = input_tensor.unsqueeze(0)
        logits = model(
            input_tensor
        )  # shape: (1, num_classes) or (1,) if script returns a scalar
        # If your TorchScript returns a single float (index), handle accordingly:
        #   pred_idx = int(torch.round(logits).item())  # if the model’s forward already returns a “class index”
        # Otherwise, if it returns raw logits or a 1D tensor, apply softmax:
        if logits.ndim > 0:
            # e.g. logits shape (1, 2) for 2-class output
            probs = torch.softmax(logits, dim=1).cpu().tolist()[0]
            pred_idx = int(max(range(len(probs)), key=lambda i: probs[i]))
            confidence = float(probs[pred_idx])
        else:
            # e.g. if the model script returns a single scalar to be rounded
            pred_idx = int(torch.round(logits).item())
            confidence = None  # or leave out if model doesn’t give prob

    # Build response
    try:
        predicted_variety = _TYPE_OF_RICE[pred_idx]
    except IndexError:
        predicted_variety = "Unknown"

    response = {"prediction": predicted_variety}
    if confidence is not None:
        response["confidence"] = confidence

    return response
