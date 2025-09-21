import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Leaderboard", layout="wide")
st.title("🏆 Candidate Leaderboard")
st.info("Select a job to see all evaluated candidates ranked by their relevance score.")

try:
    # --- Dropdown to Select a Job ---
    jobs_response = requests.get(f"{API_URL}/jobs")
    if jobs_response.status_code == 200:
        jobs_data = jobs_response.json()
        if not jobs_data:
            st.warning("No jobs found in the database. Please add a job on the 'Upload' page first.")
        else:
            jobs_df = pd.DataFrame(jobs_data)
            jobs_df['display'] = jobs_df['title'] + " at " + jobs_df.get('company', '')

            selected_job_display = st.selectbox(
                "Select a Job to see the candidate ranking:",
                jobs_df['display']
            )

            if selected_job_display:
                selected_job_id = jobs_df[jobs_df['display'] == selected_job_display]['id'].iloc[0]

                st.divider()
                st.subheader(f"Showing top candidates for: {selected_job_display}")

                # --- Fetch and Display Leaderboard ---
                evaluations_response = requests.get(f"{API_URL}/evaluations/job/{selected_job_id}")

                if evaluations_response.status_code == 200:
                    evaluations_data = evaluations_response.json()

                    if not evaluations_data:
                        st.info("No evaluations have been run for this job yet. Go to the 'Evaluate' page to analyze some resumes for this role.")
                    else:
                        leaderboard_df = pd.DataFrame(evaluations_data)
                        leaderboard_df.index = leaderboard_df.index + 1
                        leaderboard_df.rename_axis('Rank', inplace=True)
                        st.dataframe(leaderboard_df, use_container_width=True)
                else:
                    st.error("Failed to fetch evaluation data for this job.")

except requests.exceptions.ConnectionError:
    st.error("Connection Error: Could not connect to the backend server.")

    # In 4_🏆_Leaderboard.py, add this at the end

if 'leaderboard_df' in locals() and not leaderboard_df.empty:
    st.write("---")
    st.subheader("Delete an Evaluation")

    # We need the original resumes_df to find the ID from the name
    resumes_response = requests.get(f"{API_URL}/resumes")
    if resumes_response.status_code == 200:
        resumes_df = pd.DataFrame(resumes_response.json())

        eval_to_delete = st.selectbox("Select a candidate evaluation to remove from this list:", options=leaderboard_df['candidate_name'], index=None, placeholder="Choose candidate...")
        if st.button("Delete Evaluation"):
            if eval_to_delete:
                resume_id_to_delete = resumes_df[resumes_df['name'] == eval_to_delete]['id'].iloc[0]
                response = requests.delete(f"{API_URL}/evaluations/job/{selected_job_id}/resume/{resume_id_to_delete}")
                if response.status_code == 200:
                    st.success(f"Deleted evaluation for '{eval_to_delete}' successfully!")
                    st.rerun()
                else:
                    st.error("Failed to delete evaluation.")