import streamlit as st
import pandas as pd
import sqlite3

DB_NAME = 'hackathon.db'

st.set_page_config(page_title="Leaderboard", layout="wide")
st.title("🏆 Candidate Leaderboard")
st.info("Select a job to see all evaluated candidates ranked by their relevance score.")

try:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    jobs_data = cursor.execute("SELECT id, title, company FROM jobs").fetchall()
    if not jobs_data:
        st.warning("No jobs found. Please add a job on the 'Upload' page first.")
    else:
        jobs_df = pd.DataFrame(jobs_data, columns=['id', 'title', 'company'])
        jobs_df['display'] = jobs_df['title'] + " at " + jobs_df.get('company', '')
        
        selected_job_display = st.selectbox("Select a Job to see the candidate ranking:", jobs_df['display'])
        
        if selected_job_display:
            selected_job_id = jobs_df[jobs_df['display'] == selected_job_display]['id'].iloc[0]
            
            st.divider()
            st.subheader(f"Showing top candidates for: {selected_job_display}")

            query = """
                SELECT r.candidate_name, r.email, e.score, e.verdict
                FROM evaluations e JOIN resumes r ON e.resume_id = r.id
                WHERE e.job_id = ? ORDER BY e.score DESC
            """
            evaluations_data = cursor.execute(query, (int(selected_job_id),)).fetchall()

            if not evaluations_data:
                st.info("No evaluations have been run for this job yet.")
            else:
                leaderboard_df = pd.DataFrame(evaluations_data, columns=['candidate_name', 'email', 'score', 'verdict'])
                leaderboard_df['score'] = leaderboard_df['score'].map('{:.1f}%'.format)
                leaderboard_df.index = leaderboard_df.index + 1
                leaderboard_df.rename_axis('Rank', inplace=True)
                st.dataframe(leaderboard_df, use_container_width=True)
    conn.close()

except Exception as e:
    st.error(f"An error occurred: {e}")