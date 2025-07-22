import streamlit as st
import requests
from get_schema import get_schema


def render(backend_url, config):
    schema_url = f"{backend_url}{config['schema']}"
    try:
        Schema = get_schema(schema_url)
    except Exception as e:
        st.error(f"Unable to load schema: {e}")
        st.stop()
    st.caption("Please enter the following features to classify:")
    with st.form("rice_form"):
        inputs = {
            name: st.number_input(name, format="%.4f", value=None)
            for name in Schema.model_fields
        }
        submitted = st.form_submit_button("Classify")

    if submitted:
        predict_url = f"{backend_url}{config['predict']}"
        try:
            resp = requests.post(predict_url, json=inputs)
            if resp.status_code != 200:
                error_detail = resp.json().get("detail", "Unknown error")
                st.error("Prediction failed!!")
                st.write("Error detail:")
                st.json(error_detail)
                return
            data = resp.json()
        except requests.RequestException as e:
            st.error(f"API request failed: {e}")

        st.session_state.prediction_result = data.get("prediction", "N/A").upper()
        st.session_state.feedback_given = False
        st.session_state.feedback_type = None
        st.session_state.correct_class = None
        st.session_state.correct_class_confirmed = False
        st.session_state.feedback_submitted = False

    if st.session_state.get("feedback_submitted"):
        st.session_state.clear()

    if "prediction_result" in st.session_state:
        _, center_col, _ = st.columns([2.4, 1, 2.4])
        with center_col:
            st.success(f"Prediction: {st.session_state.prediction_result}")

        if not st.session_state.get("feedback_given", False):
            st.divider()
            st.write("Is the result correct?")
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Yes", key="yes_button"):
                    st.session_state.feedback_given = True
                    st.session_state.feedback_type = "yes"

            with col2:
                if st.button("No", key="no_button"):
                    st.session_state.feedback_given = True
                    st.session_state.feedback_type = "no"

    if st.session_state.get("feedback_type") == "yes":
        try:
            resp = requests.post(
                f"{backend_url}{config['feedback']}",
                json={
                    "features": inputs,
                    "correct_class": st.session_state.prediction_result.lower(),
                },
            )
            if resp.status_code != 200:
                st.error("Feedback submission failed:")
                try:
                    st.json(resp.json())
                except ValueError:
                    st.code(resp.text)
                return
            st.session_state.correct_class_confirmed = True
            st.session_state.feedback_submitted = True
            st.success("Thanks for your feedback!")

        except requests.RequestException as e:
            st.error(f"Failed to submit feedback: {e}")

    elif st.session_state.get("feedback_type") == "no":
        st.write(
            "Sorry, please help us improve the model by providing the correct class."
        )

        if not st.session_state.get("correct_class_confirmed", False):
            st.radio(
                "Select the correct class",
                options=config["classes"],
                index=None,
                key="correct_class",
            )

            if st.session_state.get("correct_class"):
                if st.button("Confirm and Submit", key="confirm_button"):
                    try:
                        resp = requests.post(
                            f"{backend_url}{config['feedback']}",
                            json={
                                "features": inputs,
                                "correct_class": st.session_state.correct_class.lower(),
                            },
                        )
                        resp.raise_for_status()
                        st.session_state.correct_class_confirmed = True
                        st.session_state.feedback_submitted = True
                        st.success("Thanks for your feedback!")
                    except requests.RequestException as e:
                        st.error(f"Failed to submit feedback: {e}")
        else:
            st.info(
                f"Feedback submitted. Correct class: {st.session_state.correct_class.upper()}"
            )
