import os
import streamlit as st
from dotenv import load_dotenv
from config import CLASSIFIERS
import importlib

# Load environment
load_dotenv()
BACKEND_API_URL = os.getenv("BACKEND_API_URL")

st.set_page_config(page_title="General Classifier", layout="wide")
st.title("General Classifier App")
st.sidebar.header("Configuration")

classifier_key = st.sidebar.selectbox("Choose classifier", list(CLASSIFIERS.keys()))

if classifier_key:
    cfg = CLASSIFIERS[classifier_key]
    module = importlib.import_module(f"classifiers.{cfg['module']}")
    module.render(BACKEND_API_URL, cfg)
