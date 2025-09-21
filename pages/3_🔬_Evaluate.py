import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Evaluate", layout="wide")
st.title("🔬 Evaluate a Resume")
st.info("Select a job and a resume from the database to run the AI analysis.")

# --- Fetch Data for Dropdown Menus ---
try:
    jobs_response = requests.get(f"{API_URL}/jobs")
    resumes_response = requests.get(f"{API_URL}/resumes")

    if jobs_response.status_code == 200 and resumes_response.status_code == 200:
        jobs_data = jobs_response.json()
        resumes_data = resumes_response.json()

        if not jobs_data or not resumes_data:
            st.warning("No jobs or resumes found in the database. Please add some on the 'Upload' page first.")
        else:
            jobs_df = pd.DataFrame(jobs_data)
            resumes_df = pd.DataFrame(resumes_data)

            # Format the display names for the dropdowns
            jobs_df['display'] = jobs_df['title'] + " at " + jobs_df['company']
            resumes_df['display'] = resumes_df['name']

            # --- Selection Form ---
            col1, col2 = st.columns(2)
            with col1:
                selected_job_display = st.selectbox(
                    "1. Select a Job Description",
                    jobs_df['display']
                )
            with col2:
                selected_resume_display = st.selectbox(
                    "2. Select a Resume to Evaluate",
                    resumes_df['display']
                )

            if st.button("Start Evaluation ✨", use_container_width=True, type="primary"):
                # Find the corresponding IDs for the selected items
                selected_job_id = jobs_df[jobs_df['display'] == selected_job_display]['id'].iloc[0]
                selected_resume_id = resumes_df[resumes_df['display'] == selected_resume_display]['id'].iloc[0]

                with st.spinner("The AI is analyzing the match... This may take a moment."):
                    payload = {
                        "job_id": int(selected_job_id),
                        "resume_id": int(selected_resume_id)
                    }
                    try:
                        response = requests.post(f"{API_URL}/analyze", json=payload)
                        if response.status_code == 200:
                            result = response.json()
                            st.divider()
                            st.subheader("📊 Evaluation Result")
                            st.markdown(result.get('analysis', "No analysis returned."))
                        else:
                            st.error(f"API Error: {response.status_code} - {response.text}")
                    except requests.exceptions.ConnectionError:
                        st.error("Connection Error: Could not connect to the backend server.")

    else:
        st.error("Failed to fetch data from the server. Ensure the backend is running.")

except requests.exceptions.ConnectionError:
    st.error("Connection Error: Could not connect to the backend server. Please ensure it is running.")