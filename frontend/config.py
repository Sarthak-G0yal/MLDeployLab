CLASSIFIERS = {
    "Rice": {
        "module": "rice_ui",
        "model": "rice",
        "schema": "/api/classify/rice/schema",
        "predict": "/api/classify/rice",
        "feedback": "/api/classify/rice/feedback",
        "classes": ["Jasmine", "Gonen"],
        "description": "Rice Grain Type Classifier is a classifier that can predict the type of rice from geometric and shape-based features. The classes are Jasmine and Gonen.",
        "title": "Rice Grain Type Classifier",
    },
    "Animal": {
        "module": "animal_ui",
        "model": "animal",
        "schema": "/api/classify/animal/schema",
        "predict": "/api/classify/animal",
        "feedback": "/api/classify/animal/feedback",
        "classes": ["Dog", "Cat", "Wild"],
        "description": "Animal Face Image Classifier is a classifier that can predict the type of animal from an image of a face.The classes are Dog, Cat, and Wild.",
        "title": "Animal Face Image Classifier",
    },
    # Add more classifiers here
}
