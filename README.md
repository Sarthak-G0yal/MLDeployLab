# MLDeployLab

This repository demonstrates the end-to-end workflow of building, deploying, and serving machine learning models using FastAPI, Docker, and Streamlit. MLDeployLab covers the complete lifecycle of ML model deployment—from training to serving predictions through RESTful APIs to capturing feedback for automated retraining.

## Project Structure

```
.
├── app                          # Backend FastAPI application
│   ├── core                    # App configuration (e.g., config.py)
│   ├── resources               # Trained models and encoders
│   │   ├── encoders            # Serialized encoders (e.g., .joblib files)
│   │   └── models              # PyTorch model files (.pt)
│   ├── routers                 # FastAPI route definitions
│   ├── schemas                 # Pydantic schemas for request/response validation
│   ├── services                # Business/inference logic
│   ├── main.py                 # FastAPI app entry point
│   ├── Dockerfile              # Backend Dockerfile
│   ├── requirements.txt        # Python dependencies
│   └── pyproject.toml          # Project metadata and tooling config                     
├── frontend                    # Streamlit frontend application
│   ├── classifiers             # UI components for classifiers
│   ├── config.py               # Frontend configuration
│   ├── get_schema.py           # Schema fetch utility
│   ├── main.py                 # Streamlit app entry point
│   ├── Dockerfile              # Frontend Dockerfile
│   ├── requirements.txt        # Python dependencies
│   └── pyproject.toml          # Project metadata and tooling config
├── notebooks                   # Jupyter notebooks for model training
│   ├── AnimalClassifier.ipynb  # Training notebook for animal classifier
│   └── RiceClassifier.ipynb    # Training notebook for rice classifier
└── docker-compose.yaml         # Multi-service Docker configuration

````

## Backend

The backend is implemented with FastAPI and exposes RESTful endpoints for model inference. It is containerized with Docker and deployed on Render using the included `Dockerfile`.

**Deployment:**  
https://mldeploylab-app.onrender.com/

> The backend may enter a sleep state after periods of inactivity; it will resume automatically within a few minutes.

## Frontend

The frontend is built with Streamlit to provide an interactive interface for testing models and submitting feedback. It is containerized with Docker and deployed on Render using the included `Dockerfile`.

**Live Demo:**  
https://mldeploylab-frontend.onrender.com/

> The frontend may enter a sleep state after periods of inactivity; it will resume automatically within a few minutes.

## Local Development

To run both backend and frontend locally, ensure that Docker and Docker Compose are installed. From the project root:

```bash
docker-compose up --build
````

* Backend API: `http://localhost:8000`
* Streamlit UI: `http://localhost:8501`

## Available Models

### Rice Type Classifier

Classifies rice grain types based on geometric and shape-based features.

**Sample Input**

```json
{
  "Area": 2872,
  "MajorAxisLength": 74.69,
  "MinorAxisLength": 51.40,
  "Eccentricity": 0.73,
  "ConvexArea": 3015,
  "EquivDiameter": 60.47,
  "Extent": 0.71,
  "Perimeter": 208.31,
  "Roundness": 0.83,
  "AspectRatio": 1.45
}
```

**Classes**

- Jasmine
- Gonen 

**Dataset**  
Rice Type Classification on Kaggle: https://www.kaggle.com/datasets/mssmartypants/rice-type-classification


### Animal Image Classifier

Classifies animals from an image URL. The API accepts a JSON payload with an image URL, downloads the image, and returns the predicted label.

**Sample Input**

```json
{
  "image_url": "https://example.com/path/to/image.jpg"
}
```

**Classes**

- Cat  
- Dog  
- Wild  

**Dataset**  
Animal Faces on Kaggle: https://www.kaggle.com/datasets/andrewmvd/animal-faces

## Feedback and Contributions

Contributions, suggestions, and feedback are welcome. Please open an issue or submit a pull request for improvements, bug reports, or feature requests.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

Sarthak Goyal
[sarthak.goyal.3505@gmail.com](mailto:sarthak.goyal.3505@gmail.com)

