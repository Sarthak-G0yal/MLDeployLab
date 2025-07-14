from pydantic import BaseModel, HttpUrl


class AnimalFeatures(BaseModel):
    image_url: HttpUrl


class AnimalFeedback(BaseModel):
    image_url: HttpUrl
    animal_class: str
