import streamlit as st
from datetime import date
from get_schema import get_schema
from dotenv import load_dotenv
import os
import requests

load_dotenv()

BACKEND_API_URL = os.getenv("BACKEND_API_URL")
schema_url = f"{BACKEND_API_URL}/api/classify/rice/schema"
RiceFeatures = get_schema(url=schema_url)

st.title("Classifier App")
st.subheader("Classify rice grains.")

if "started" not in st.session_state:
    st.session_state.started = False


def start_classification():
    st.session_state.started = True


if not st.session_state.started:
    st.button("Get Started", on_click=start_classification)

if st.session_state.started:
    st.write("Classification started on:", date.today())

    st.subheader("Enter Rice Grain Features")
    with st.form("rice_form"):
        input_features = {}
        for feature in RiceFeatures.model_fields.keys():
            input_features[feature] = st.number_input(feature, value=0.0, format="%.4f")

        submitted = st.form_submit_button("Classify Rice")
        if submitted:
            st.write("Received features :")
            st.json(input_features)

            model_url = f"{BACKEND_API_URL}/api/classify/rice"
            prediction = requests.post(model_url, json=input_features).json()
            if prediction["prediction"]:
                st.success(f"The predicted class is {prediction['prediction'].upper()}.")
            else:
                st.write("Prediction object:", prediction)
