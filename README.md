# Model Deployment with FastAPI and Docker

This repository contains machine learning models that I’ve built and deployed using **FastAPI** and **Docker**. The goal is to provide a scalable and efficient way to serve ML models via RESTful APIs.

The current deployment is based on a **rice classification model** trained using a dataset from Kaggle (linked below). More models will be added to this project in the near future.

---

## 📁 Project Structure

```
├── app
│   ├── rice_classification_model.pt
│   └── server.py
├── dataset
│   └── riceClassification.csv
├── Dockerfile
├── README.md
├── requirements.txt
└── RicePredicationModel.ipynb
```

---

## 🚀 Current Model: Rice Type Classification

The model is trained to classify rice grain types based on various geometric and shape-based features. It uses the dataset available here:
🔗 [Rice Type Classification - Kaggle](https://www.kaggle.com/datasets/mssmartypants/rice-type-classification)

### Sample Input Format (JSON)

```json
{
  "Area": 2872,
  "MajorAxisLength": 74.69188071,
  "MinorAxisLength": 51.40045446,
  "Eccentricity": 0.7255527468,
  "ConvexArea": 3015,
  "EquivDiameter": 60.47101762,
  "Extent": 0.7130089374,
  "Perimeter": 208.317,
  "Roundness": 0.8316582009,
  "AspectRatio": 1.453136582
}
```

---

## 🐳 Deployment Overview

* **FastAPI** is used to build a lightweight and fast REST API for model inference.
* The API is containerized using **Docker** for easy deployment and scalability.

---

## 📌 Future Plans

* Add support for additional models across different domains.
* Implement versioning and logging for deployed APIs.
* Improve model packaging and inference performance.

---

Feel free to explore, clone, or contribute to this project!