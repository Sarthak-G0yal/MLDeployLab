import os
from datetime import date

import requests
import streamlit as st
from dotenv import load_dotenv
from get_schema import get_schema

# Load environment
load_dotenv()
BACKEND_API_URL = os.getenv("BACKEND_API_URL")

# Define your classifiers
CLASSIFIERS = {
    "Rice": {"schema": "/api/classify/rice/schema", "predict": "/api/classify/rice"},
    # More will be add here.
}

st.set_page_config(page_title="General Classifier", layout="wide")
st.title("General Classifier App")
st.sidebar.header("Configuration")

# Sidebar: pick the classifier
classifier_key = st.sidebar.selectbox("Choose classifier", list(CLASSIFIERS.keys()))

if classifier_key:
    cfg = CLASSIFIERS[classifier_key]
    schema_url = f"{BACKEND_API_URL}{cfg['schema']}"
    try:
        Schema = get_schema(url=schema_url)
    except Exception as e:
        st.error(f"Unable to load schema: {e}")
        st.stop()

    st.markdown(f"**Session started:** {date.today()}")
    st.subheader(f"{classifier_key} – Input Features")

    with st.form("feature_form"):
        inputs = {
            name: st.number_input(name, format="%.4f", value=None)
            for name in Schema.model_fields
        }
        submitted = st.form_submit_button("Classify")

    if submitted:
        st.json(inputs)
        predict_url = f"{BACKEND_API_URL}{cfg['predict']}"
        try:
            resp = requests.post(predict_url, json=inputs)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            st.error(f"API request failed: {e}")
        else:
            pred = data.get("prediction")
            if pred:
                st.success(f"Predicted class: {pred.upper()}")
            else:
                st.warning("No prediction returned.")
                st.json(data)
