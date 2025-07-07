import os
import torch
from torchvision import transforms
from PIL import Image
import joblib
from core.config import settings

_DEFAULT_MODEL_FILENAME = "image_classifier.pt"
_DEFAULT_LABEL_ENCODER = "animal_label_encoder.joblib"

_model: torch.jit.ScriptModule | None = None
_label_encoder = None


def _load_assets() -> tuple[torch.jit.ScriptModule, joblib]:
    global _model, _label_encoder

    if _model is None:
        model_path = os.path.join(settings.MODEL_DIR, _DEFAULT_MODEL_FILENAME)
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Cannot find model at {model_path}")
        _model = torch.jit.load(model_path, map_location="cpu")
        _model.eval()

    if _label_encoder is None:
        label_encoder_path = os.path.join(settings.ENCODER_DIR, _DEFAULT_LABEL_ENCODER)
        if not os.path.exists(label_encoder_path):
            raise FileNotFoundError(
                f"Cannot find label encoder at {label_encoder_path}"
            )
        _label_encoder = joblib.load(label_encoder_path)

    return _model, _label_encoder


def predict_animal(image_path: str) -> dict:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Cannot find image at {image_path}")

    transform = transforms.Compose(
        [
            transforms.Resize((128, 128)),
            transforms.ToTensor(),
            transforms.ConvertImageDtype(torch.float),
        ]
    )

    model, label_encoder = _load_assets()
    image = Image.open(image_path).convert("RGB")
    image_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(image_tensor)
        prediction = torch.argmax(output, dim=1).item()
    predicted_label = label_encoder.inverse_transform([prediction])[0]
    return {"prediction": str(predicted_label)}
