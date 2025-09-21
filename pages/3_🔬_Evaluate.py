import streamlit as st
import pandas as pd
import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from analyzer import get_gemini_response, parse_analysis

DB_NAME = 'hackathon.db'

st.set_page_config(page_title="Evaluate", layout="wide")
st.title("🔬 Evaluate a Resume")
st.info("Select a job and a resume from the database to run the AI analysis.")

try:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    jobs_data = cursor.execute("SELECT id, title, company FROM jobs").fetchall()
    resumes_data = cursor.execute("SELECT id, candidate_name FROM resumes").fetchall()

    if not jobs_data or not resumes_data:
        st.warning("No jobs or resumes found. Please add some on the 'Upload' page first.")
    else:
        jobs_df = pd.DataFrame(jobs_data, columns=['id', 'title', 'company'])
        resumes_df = pd.DataFrame(resumes_data, columns=['id', 'name'])
        
        jobs_df['display'] = jobs_df['title'] + " at " + jobs_df.get('company', '')
        
        col1, col2 = st.columns(2)
        with col1:
            selected_job_display = st.selectbox("1. Select a Job Description", jobs_df['display'])
        with col2:
            selected_resume_display = st.selectbox("2. Select a Resume to Evaluate", resumes_df['name'])

        if st.button("Start Evaluation ✨", use_container_width=True, type="primary"):
            selected_job_id = jobs_df[jobs_df['display'] == selected_job_display]['id'].iloc[0]
            selected_resume_id = resumes_df[resumes_df['name'] == selected_resume_display]['id'].iloc[0]

            with st.spinner("The AI is analyzing the match... This may take a moment."):
                job_text = cursor.execute("SELECT description_text FROM jobs WHERE id = ?", (int(selected_job_id),)).fetchone()[0]
                resume_text = cursor.execute("SELECT text_content FROM resumes WHERE id = ?", (int(selected_resume_id),)).fetchone()[0]

                analysis = get_gemini_response(resume_text, job_text)
                score, verdict = parse_analysis(analysis)

                cursor.execute(
                    "INSERT INTO evaluations (resume_id, job_id, score, verdict, analysis_text) VALUES (?, ?, ?, ?, ?)",
                    (int(selected_resume_id), int(selected_job_id), score, verdict, analysis)
                )
                conn.commit()
                
                st.divider()
                st.subheader("📊 Evaluation Result")
                st.markdown(analysis)
    conn.close()

except Exception as e:
    st.error(f"An error occurred: {e}")