import os
import streamlit as st
from dotenv import load_dotenv
from config import CLASSIFIERS
import importlib
from PIL import Image
from pathlib import Path

# Load environment
load_dotenv()

logo_path = Path("assets/logo.png")
BACKEND_API_URL = os.getenv("BACKEND_API_URL")

logo = None
if logo_path.exists():
    logo = Image.open(logo_path)
    st.logo(logo, size="large")

st.set_page_config(page_title="General Classifier", page_icon=logo, layout="wide")
st.title("General Classifier App")
st.sidebar.header("Classifier Selection")
classifier_key = st.sidebar.selectbox("Choose classifier", list(CLASSIFIERS.keys()))

if classifier_key:
    cfg = CLASSIFIERS[classifier_key]
    st.subheader(cfg["title"])
    st.caption(cfg["description"])
    st.divider()
    module = importlib.import_module(f"classifiers.{cfg['module']}")
    module.render(BACKEND_API_URL, cfg)
