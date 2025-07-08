# MLDeployLab

This repository demonstrates the end-to-end workflow of building, deploying, and serving machine learning models using FastAPI, Docker, and Streamlit. The primary goal of MLDeployLab is to explore the complete lifecycle of ML model deployment—from training to serving predictions through APIs and capturing feedback for automated retraining.

## Project Structure

```
├── app
│   ├── core               # Configuration files
│   ├── resources          # Trained models and encoders
│   ├── routers            # API route definitions
│   ├── schemas            # Pydantic schemas
│   ├── services           # Inference logic
│   ├── main.py            # FastAPI application entry point
│   ├── Dockerfile         # Backend Dockerfile
│   └── requirements.txt
├── frontend
│   ├── main.py            # Streamlit frontend entry point
│   ├── Dockerfile         # Frontend Dockerfile
│   └── requirements.txt
├── notebooks              # Model training notebooks
├── docker-compose.yaml    # Multi-container deployment configuration
└── README.md
```

## Backend

The backend is implemented with FastAPI to expose RESTful endpoints for model inference. It is containerized with Docker and deployed on Render.

Deployment link: [Backend Service](https://backend-gdx3.onrender.com/)

> **Note:** The backend service may enter a sleep state after periods of inactivity. It will resume automatically within a few minutes upon receiving a new request.

## Frontend

The frontend uses Streamlit to provide an interactive interface for testing models and submitting feedback.

Live demo: [Live Instance](https://frontend-2iq8.onrender.com/)

> **Note:** The frontend service may enter a sleep state after periods of inactivity. It will resume automatically within a few minutes upon opening.

## Available Models

### Rice Type Classifier

Classifies rice grain types based on geometric and shape-based features.

**Sample Input (JSON)**

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

### Animal Image Classifier

Classifies animals from an image URL. The API accepts a JSON payload with an image URL, downloads the image using `requests`, and returns the predicted label.

**Sample Input (JSON)**

```json
{
  "url": "https://example.com/path/to/image.jpg"
}
```

## Future Plans

* Integrate additional models across various domains
* Implement a user feedback loop: after each prediction, users can confirm correctness or submit the correct label
* Store feedback data and trigger automated retraining pipelines
* Add model versioning, logging, and performance monitoring
* Enhance packaging, scalability, and deployment automation

Contributions and feedback are welcome.
