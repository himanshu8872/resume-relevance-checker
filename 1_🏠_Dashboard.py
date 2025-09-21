import streamlit as st
import pandas as pd
import sqlite3

# At the top of 1_🏠_Dashboard.py
from database import init_db

# This will create the tables if they don't exist when the app starts
init_db()

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
            # ADD THIS LINE BACK IN
            jobs_df['display'] = jobs_df['title'] + " at " + jobs_df.get('company', '')
            st.dataframe(jobs_df, use_container_width=True)
        else:
            st.info("No jobs have been added yet.")

    with col2:
        st.subheader("👤 Recent Resumes")
        resumes_data = cursor.execute("SELECT id, candidate_name, email FROM resumes ORDER BY id DESC LIMIT 5").fetchall()
        if resumes_data:
            resumes_df = pd.DataFrame(resumes_data, columns=['id', 'name', 'email'])
            # AND ADD THIS LINE BACK IN
            resumes_df['display'] = resumes_df['name']
            st.dataframe(resumes_df, use_container_width=True)
        else:
            st.info("No resumes have been added yet.")

    conn.close()

except sqlite3.OperationalError as e:
    st.error(f"Database error: {e}. It's possible the database file doesn't exist yet. Please go to the 'Upload' page to add data.")
except Exception as e:
    st.error(f"An unexpected error occurred: {e}")

# In 1_🏠_Dashboard.py, add this at the very end

st.divider()
st.subheader("⚠️ Danger Zone")

col1, col2 = st.columns(2)
with col1:
    # Check if jobs_df exists and is not empty
    if 'jobs_df' in locals() and jobs_df is not None and not jobs_df.empty:
        st.write("Delete a Job Description")
        job_to_delete = st.selectbox("Select Job", options=jobs_df['display'], index=None, placeholder="Choose a job to delete...")
        if st.button("Delete Job"):
            if job_to_delete:
                job_id = jobs_df[jobs_df['display'] == job_to_delete]['id'].iloc[0]
                try:
                    conn = sqlite3.connect(DB_NAME)
                    conn.execute("PRAGMA foreign_keys = ON")
                    conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
                    conn.commit()
                    conn.close()
                    st.success(f"Deleted '{job_to_delete}' successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to delete job: {e}")

with col2:
    # Check if resumes_df exists and is not empty
    if 'resumes_df' in locals() and resumes_df is not None and not resumes_df.empty:
        st.write("Delete a Resume")
        resume_to_delete = st.selectbox("Select Resume", options=resumes_df['display'], index=None, placeholder="Choose a resume to delete...")
        if st.button("Delete Resume"):
            if resume_to_delete:
                resume_id = resumes_df[resumes_df['display'] == resume_to_delete]['id'].iloc[0]
                try:
                    conn = sqlite3.connect(DB_NAME)
                    conn.execute("PRAGMA foreign_keys = ON")
                    conn.execute("DELETE FROM resumes WHERE id = ?", (resume_id,))
                    conn.commit()
                    conn.close()
                    st.success(f"Deleted '{resume_to_delete}' successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to delete resume: {e}")