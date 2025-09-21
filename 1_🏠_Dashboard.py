import streamlit as st
import pandas as pd
import sqlite3
from database import init_db

# Initialize the database and create tables if they don't exist
init_db()

DB_NAME = 'hackathon.db'

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📊 Dashboard Overview")

def get_dashboard_data():
    """Fetches all necessary data for the dashboard in one go, ensuring connections are closed."""
    with sqlite3.connect(DB_NAME) as conn:
        job_count = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
        resume_count = conn.execute("SELECT COUNT(*) FROM resumes").fetchone()[0]
        evaluation_count = conn.execute("SELECT COUNT(*) FROM evaluations").fetchone()[0]
        avg_score_result = conn.execute("SELECT AVG(score) FROM evaluations").fetchone()
        avg_score = avg_score_result[0] if avg_score_result and avg_score_result[0] is not None else 0

        jobs_data = conn.execute("SELECT id, title, company FROM jobs ORDER BY id DESC").fetchall()
        jobs_df = pd.DataFrame(jobs_data, columns=['id', 'title', 'company'])
        if not jobs_df.empty:
            jobs_df['display'] = jobs_df['title'] + " at " + jobs_df['company']

        resumes_data = conn.execute("SELECT id, candidate_name, email FROM resumes ORDER BY id DESC").fetchall()
        resumes_df = pd.DataFrame(resumes_data, columns=['id', 'name', 'email'])
        if not resumes_df.empty:
            resumes_df['display'] = resumes_df['name']

    stats = {
        "total_jobs": job_count, "total_resumes": resume_count,
        "total_evaluations": evaluation_count, "average_score": avg_score
    }
    return stats, jobs_df, resumes_df

try:
    stats, jobs_df, resumes_df = get_dashboard_data()

    # --- Key Metrics ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Jobs", stats['total_jobs'])
    col2.metric("Total Resumes", stats['total_resumes'])
    col3.metric("Total Evaluations", stats['total_evaluations'])
    col4.metric("Average Score", f"{stats['average_score']:.1f}%")
    st.divider()

    # --- Recent Items Tables ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📄 Recent Job Descriptions")
        st.dataframe(jobs_df[['id', 'title', 'company']], use_container_width=True) # Hide 'display' column from view
    with col2:
        st.subheader("👤 Recent Resumes")
        st.dataframe(resumes_df[['id', 'name', 'email']], use_container_width=True) # Hide 'display' column from view
    
except Exception as e:
    st.error(f"An error occurred while loading the dashboard: {e}")