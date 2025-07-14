CLASSIFIERS = {
    "Animal": {
        "module": "animal_ui",
        "predict": "/api/classify/animal",
        "schema": "/api/classify/animal/schema",
        "feedback": "/api/classify/animal/feedback",
        "classes": ["Dog", "Cat", "Wild"],
    },
    "Rice": {
        "module": "rice_ui",
        "schema": "/api/classify/rice/schema",
        "predict": "/api/classify/rice",
        "classes": ["Jasmine", "Gonen"],
    },
    # Add more classifiers here
}
