import os
from dotenv import load_dotenv


load_dotenv()

PATH_TO_FEEDBACK_FOLDER = os.getenv("PATH_TO_FEEDBACK_FOLDER") or "./resources/feedback"
os.makedirs(PATH_TO_FEEDBACK_FOLDER, exist_ok=True)


def store_feedback(feedback_data: dict, classifier: str) -> dict:
    features = feedback_data.get("features")
    correct_class = feedback_data.get("correct_class")
    features_key = ",".join([f"{k}" for k in features.keys()])
    features_value = ",".join([f"{v}" for v in features.values()])
    file_path = f"{PATH_TO_FEEDBACK_FOLDER}/{classifier}_feedback.csv"
    if not os.path.exists(file_path):
        os.makedirs(PATH_TO_FEEDBACK_FOLDER, exist_ok=True)
        with open(file_path, "a") as f:
            f.write(f"{features_key},class\n")
    with open(file_path, "a") as f:
        f.write(f"{features_value},{correct_class}\n")

    return {"success": True}
