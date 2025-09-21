import streamlit as st
import pandas as pd
import sqlite3

DB_NAME = 'hackathon.db'

st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📊 Dashboard Overview")

try:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # --- Key Metrics ---
    job_count = cursor.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
    resume_count = cursor.execute("SELECT COUNT(*) FROM resumes").fetchone()[0]
    evaluation_count = cursor.execute("SELECT COUNT(*) FROM evaluations").fetchone()[0]
    avg_score = cursor.execute("SELECT AVG(score) FROM evaluations").fetchone()[0]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Jobs", job_count)
    col2.metric("Total Resumes", resume_count)
    col3.metric("Total Evaluations", evaluation_count)
    col4.metric("Average Score", f"{avg_score if avg_score else 0:.1f}%")

    st.divider()

    # --- Recent Items Tables ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📄 Recent Job Descriptions")
        jobs_data = cursor.execute("SELECT id, title, company FROM jobs ORDER BY id DESC LIMIT 5").fetchall()
        if jobs_data:
            jobs_df = pd.DataFrame(jobs_data, columns=['id', 'title', 'company'])
            st.dataframe(jobs_df, use_container_width=True)
        else:
            st.info("No jobs have been added yet.")

    with col2:
        st.subheader("👤 Recent Resumes")
        resumes_data = cursor.execute("SELECT id, candidate_name, email FROM resumes ORDER BY id DESC LIMIT 5").fetchall()
        if resumes_data:
            resumes_df = pd.DataFrame(resumes_data, columns=['id', 'name', 'email'])
            st.dataframe(resumes_df, use_container_width=True)
        else:
            st.info("No resumes have been added yet.")

    conn.close()

except sqlite3.OperationalError as e:
    st.error(f"Database error: {e}. It's possible the database file doesn't exist yet. Please go to the 'Upload' page to add data.")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")