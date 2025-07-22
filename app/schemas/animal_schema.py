from pydantic import BaseModel, HttpUrl


class AnimalFeatures(BaseModel):
    image_url: HttpUrl


class AnimalFeedback(BaseModel):
    features: AnimalFeatures
    correct_class: str
