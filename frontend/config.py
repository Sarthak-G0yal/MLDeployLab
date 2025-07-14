CLASSIFIERS = {
    "Animal": {
        "module": "animal_ui",
        "predict": "/api/classify/animal",
        "schema": "/api/classify/animal/schema",
        "feedback": "/api/classify/animal/feedback",
        "classes": ["Dog", "Cat", "Wild"],
        "description": "Animal Face Image Classifier is a classifier that can predict the type of animal from an image of a face.The classes are Dog, Cat, and Wild.",
        "title": "Animal Face Image Classifier",
    },
    "Rice": {
        "module": "rice_ui",
        "schema": "/api/classify/rice/schema",
        "predict": "/api/classify/rice",
        "classes": ["Jasmine", "Gonen"],
        "description": "Rice Grain Type Classifier is a classifier that can predict the type of rice from geometric and shape-based features. The classes are Jasmine and Gonen.",
        "title": "Rice Grain Type Classifier",
    },
    # Add more classifiers here
}
