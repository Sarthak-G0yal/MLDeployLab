import streamlit as st
import requests


def render(backend_url, endpoints):
    st.subheader("Animal Face Image Classification")

    image_url = st.text_input("Enter image URL")

    if image_url:
        _, center_col, _ = st.columns([1, 3, 1])
        with center_col:
            st.image(image_url, caption="Input Image", use_container_width=True)

    if st.button("Classify") and image_url:
        try:
            resp = requests.post(
                f"{backend_url}{endpoints['predict']}", json={"image_url": image_url}
            )
            if resp.status_code != 200:
                st.error("Prediction failed:")
                try:
                    st.json(resp.json())
                except ValueError:
                    st.code(resp.text)
                return
            result = resp.json()
        except requests.RequestException as e:
            st.error(f"API request failed: {e}")
            return

        st.session_state.prediction_result = result.get("prediction", "N/A").upper()
        st.session_state.feedback_given = False
        st.session_state.feedback_type = None
        st.session_state.correct_class = None
        st.session_state.correct_class_confirmed = False
        st.session_state.feedback_submitted = False

    if st.session_state.get("feedback_submitted"):
        st.session_state.clear()

    if "prediction_result" in st.session_state:
        _, center_col, _ = st.columns([3, 1, 3])
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
                f"{backend_url}{endpoints['feedback']}",
                json={
                    "image_url": image_url,
                    "animal_class": st.session_state.prediction_result.lower(),
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
                options=["Dog", "Cat", "Wild"],
                index=None,
                key="correct_class",
            )

            if st.session_state.get("correct_class"):
                if st.button("Confirm and Submit", key="confirm_button"):
                    try:
                        resp = requests.post(
                            f"{backend_url}{endpoints['feedback']}",
                            json={
                                "image_url": image_url,
                                "animal_class": st.session_state.correct_class.lower(),
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
