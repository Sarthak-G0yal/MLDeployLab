import streamlit as st
import requests

def render(backend_url, endpoints):
    st.subheader("Animal Image Classification")

    image_url = st.text_input("Enter image URL")

    if image_url:
        _, center_co,_ = st.columns([1, 3, 1])
        with center_co:
            st.image(image_url, caption="Input Image", use_container_width=True)

    if st.button("Classify") and image_url:
        try:
            resp = requests.post(
                f"{backend_url}{endpoints['predict']}",
                params={"image_url": image_url}
            )
            resp.raise_for_status()
            result = resp.json()
        except requests.RequestException as e:
            st.error(f"API request failed: {e}")
        else:
            st.success(f"Prediction: {result.get('prediction', 'N/A')}")
