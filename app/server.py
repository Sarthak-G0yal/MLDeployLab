from fastapi import FastAPI
from app.apis import rice_classifier


# animal_image_classifier = torch.jit.load("app/image_classifier.pt", map_location="cpu")

# type_of_rice = ["Gonen", "Jasmine"]
# type_of_images = ["Cat", "Dog","Wild Animal"]

# max_dict = {
#     "Area": np.float32(10210),
#     "MajorAxisLength": np.float32(183.2114344),
#     "MinorAxisLength": np.float32(82.55076212),
#     "Eccentricity": np.float32(0.9667736672),
#     "ConvexArea": np.float32(11008),
#     "EquivDiameter": np.float32(114.0165591),
#     "Extent": np.float32(0.8865730584),
#     "Perimeter": np.float32(508.511),
#     "Roundness": np.float32(0.9047483132),
#     "AspectRation": np.float32(3.911844673),
# }

# features = [
#     "Area",
#     "MajorAxisLength",
#     "MinorAxisLength",
#     "Eccentricity",
#     "ConvexArea",
#     "EquivDiameter",
#     "Extent",
#     "Perimeter",
#     "Roundness",
#     "AspectRation",
# ]


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "An API for PyTorch Models"}


@app.post("/predict")
def get_prediction(data: rice_classifier.RiceFeatures):
    return rice_classifier.predict(data)
