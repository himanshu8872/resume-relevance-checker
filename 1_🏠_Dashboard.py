import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📊 Dashboard Overview")

# Initialize DataFrames as None to ensure they always exist
jobs_df = None
resumes_df = None

try:
    # --- Key Metrics ---
    stats_response = requests.get(f"{API_URL}/stats")
    if stats_response.status_code == 200:
        stats = stats_response.json()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Jobs", stats.get('total_jobs', 0))
        col2.metric("Total Resumes", stats.get('total_resumes', 0))
        col3.metric("Total Evaluations", stats.get('total_evaluations', 0))
        
        avg_score_val = stats.get('average_score', 0)
        col4.metric("Average Score", f"{avg_score_val:.1f}%")

    else:
        st.error("Could not fetch stats from the server.")

    st.divider()

    # --- Recent Items Tables ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📄 Recent Job Descriptions")
        jobs_response = requests.get(f"{API_URL}/jobs")
        if jobs_response.status_code == 200:
            jobs_data = jobs_response.json()
            if jobs_data:
                jobs_df = pd.DataFrame(jobs_data)
                jobs_df['display'] = jobs_df['title'] + " at " + jobs_df.get('company', '')
                st.dataframe(jobs_df.head(), use_container_width=True)
            else:
                st.info("No jobs have been added yet.")
        else:
            st.warning("Could not fetch recent jobs.")

    with col2:
        st.subheader("👤 Recent Resumes")
        resumes_response = requests.get(f"{API_URL}/resumes")
        if resumes_response.status_code == 200:
            resumes_data = resumes_response.json()
            if resumes_data:
                resumes_df = pd.DataFrame(resumes_data)
                resumes_df['display'] = resumes_df['name']
                st.dataframe(resumes_df.head(), use_container_width=True)
            else:
                st.info("No resumes have been added yet.")
        else:
            st.warning("Could not fetch recent resumes.")
            
    # --- Danger Zone ---
    st.divider()
    st.subheader("⚠️ Danger Zone")

    col1, col2 = st.columns(2)
    with col1:
        # Check if jobs_df was successfully created before showing the delete option
        if jobs_df is not None and not jobs_df.empty:
            st.write("Delete a Job Description")
            job_to_delete = st.selectbox("Select Job", options=jobs_df['display'], index=None, placeholder="Choose a job to delete...")
            if st.button("Delete Job"):
                if job_to_delete:
                    job_id = jobs_df[jobs_df['display'] == job_to_delete]['id'].iloc[0]
                    response = requests.delete(f"{API_URL}/jobs/{job_id}")
                    if response.status_code == 200:
                        st.success(f"Deleted '{job_to_delete}' successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to delete job.")
    
    with col2:
        # Check if resumes_df was successfully created
        if resumes_df is not None and not resumes_df.empty:
            st.write("Delete a Resume")
            resume_to_delete = st.selectbox("Select Resume", options=resumes_df['display'], index=None, placeholder="Choose a resume to delete...")
            if st.button("Delete Resume"):
                if resume_to_delete:
                    resume_id = resumes_df[resumes_df['display'] == resume_to_delete]['id'].iloc[0]
                    response = requests.delete(f"{API_URL}/resumes/{resume_id}")
                    if response.status_code == 200:
                        st.success(f"Deleted '{resume_to_delete}' successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to delete resume.")

except requests.exceptions.ConnectionError:
    st.error("Connection Error: Could not connect to the backend server. Please ensure it's running.")