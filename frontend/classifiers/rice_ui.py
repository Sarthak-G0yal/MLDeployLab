import streamlit as st
import requests
from get_schema import get_schema

def render(backend_url, endpoints):
    schema_url = f"{backend_url}{endpoints['schema']}"
    try:
        Schema = get_schema(schema_url)
    except Exception as e:
        st.error(f"Unable to load schema: {e}")
        st.stop()

    st.subheader("Rice - Input Features")

    with st.form("rice_form"):
        inputs = {
            name: st.number_input(name, format="%.4f", value=None)
            for name in Schema.model_fields
        }
        submitted = st.form_submit_button("Classify")

    if submitted:
        predict_url = f"{backend_url}{endpoints['predict']}"
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
